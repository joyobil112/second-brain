from ingestion import DocumentParser
from agent import TextClassifier
from vault_manager import VaultManager
import config
import os

def main():
    print("🚀 Starting Local Second Brain Pipeline...\n")
    
    # Initialize our tools
    parser = DocumentParser()
    classifier = TextClassifier(model_name="llama3") 
    vault = VaultManager(model_name="llama3")
    
    # Create a processed folder for cleanup
    processed_dir = config.BASE_DIR / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    # Phase 1: Ingestion
    print("Scanning Inbox...")
    documents = parser.scan_inbox()
    
    if not documents:
        print("Inbox is empty. Nothing to process.")
        return

    # Phase 2 & 3: Classification and Storage
    print(f"\n🧠 Beginning AI Processing for {len(documents)} document(s)...")
    
    for doc in documents:
        print(f"\nAnalyzing: {doc['filename']}...")
        
        # Classify the document
        classification = classifier.categorize_text(doc['content'])
        doc['metadata'] = classification
        
        print(f"   ➡️ Assigned Category: {classification['category']}")
        
        # Save to Vault and build connections
        vault.process_and_save(doc)
        
        # Cleanup: Move file out of inbox
        os.rename(doc['original_path'], processed_dir / doc['filename'])
        print(f"   🧹 Moved original file to /processed directory.")

    print("\n✅ All documents successfully processed and vaulted.")

if __name__ == "__main__":
    main()