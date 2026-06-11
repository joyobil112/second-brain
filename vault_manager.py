import chromadb
import datetime
import ollama
import os
import re
import config

class VaultManager:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        # Initialize a local vector database hidden in your project folder
        self.db_path = config.BASE_DIR / ".chroma_db"
        self.client = chromadb.PersistentClient(path=str(self.db_path))

    def _clean_pdf_text(self, text: str) -> str:
        """Smartly rebuilds paragraphs and removes PDF physical line breaks."""
        # 1. Fix broken hyphenated words at the end of physical lines (e.g., "infor-\nmation")
        text = re.sub(r'-\n\s*', '', text)
        
        # 2. If a newline follows a punctuation mark and precedes a Capital letter or bullet, it's a paragraph break.
        text = re.sub(r'([.?!:])\s*\n(?=[A-Z0-9•●])', r'\1\n\n', text)
        
        # 3. Replace all remaining single newlines with a space
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        
        # 4. Force bullet points to explicitly start on their own new line
        text = re.sub(r'(\s*[•●○]\s+)', r'\n\n\1', text)
        
        # 5. Clean up any excessive spaces or excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()

    def process_and_save(self, document: dict):
        category = document['metadata']['category']
        filename = document['filename']
        content = document['content']
        
        if category == "Uncategorized":
            self._write_markdown(document, category, "No connections found. Error in classification.")
            return

        # 1. INTRA-SEGMENT LINKING: Create a distinct database collection for EACH category.
        collection_name = category.lower().replace(" ", "_")
        collection = self.client.get_or_create_collection(name=collection_name)

        # 2. Query for related past notes in THIS category
        print(f"   🔍 Searching existing '{category}' notes for connections...")
        related_docs = collection.query(
            query_texts=[content[:1500]], 
            n_results=2 
        )

        connection_text = "> *No prior notes found in this segment to connect with yet.*"
        
        # 3. If past notes exist, have the LLM synthesize a connection
        if related_docs['documents'] and related_docs['documents'][0]:
            print(f"   🔗 Found {len(related_docs['documents'][0])} related note(s)!")
            
            related_texts = "\n\n".join(related_docs['documents'][0])
            related_filenames = [m['filename'] for m in related_docs['metadatas'][0]]
            
            prompt = f"""
            You are an analytical Second Brain. I am adding a new note to my '{category}' segment. 
            
            New Note Snippet:
            {content[:1000]}
            
            Past Related Notes:
            {related_texts[:2000]}
            
            Write a sharp, 2-3 sentence summary connecting the core ideas of the new note with the past notes. If no clear connection exists, say so. 
            Focus on insights and relationships, not just surface-level similarities. Do not force a connection if it doesn't exist.
            """
            
            print("   🧠 Synthesizing connections...")
            response = ollama.chat(model=self.model_name, messages=[{'role': 'user', 'content': prompt}])
            synthesis = response['message']['content'].strip()
            
            links = "\n".join([f"- [[{fname.replace('.md', '')}]]" for fname in related_filenames])
            connection_text = f"### 🧠 AI Synthesis\n{synthesis}\n\n### 🔗 Related Notes\n{links}"

        # 4. Generate the final Obsidian Markdown Note
        self._write_markdown(document, category, connection_text)

        # 5. Embed and save the new document into the Vector DB
        note_id = filename + "_" + str(datetime.datetime.now().timestamp())
        collection.add(
            documents=[content],
            metadatas=[{"filename": filename}],
            ids=[note_id]
        )
        print(f"   💾 Saved to Vector DB and Obsidian Vault!")

    def _write_markdown(self, document: dict, category: str, connections: str):
        """Formats and writes the actual .md file to the Obsidian Vault."""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        safe_title = document['filename'].replace('.txt', '').replace('.pdf', '')
        
        # Apply our new smart text cleaner
        cleaned_content = self._clean_pdf_text(document['content'])
        
        md_content = f"""---
date: {date_str}
category: {category}
confidence: {document['metadata']['confidence_score']}
---
# {safe_title}

> **AI Reasoning for Classification:** {document['metadata']['reasoning']}

{connections}

---
### Source Content
{cleaned_content}
"""
        
        target_folder = config.VAULT_DIR / category if category != "Uncategorized" else config.VAULT_DIR
        file_path = target_folder / f"{safe_title}.md"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)