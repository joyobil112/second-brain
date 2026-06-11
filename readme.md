![Uploading Screenshot 2026-06-11 at 16.19.41.png…]()

# JoyBit: Autonomous Knowledge Ingestion & Synthesis Pipeline

A completely offline, privacy-first ingestion pipeline that automatically captures, cleans, categorizes, and links knowledge assets into an Obsidian Vault. Powered by a local Large Language Model (LLM) and an intra-segment vector database, this tool ensures your personal research, documentation, and clipped web articles remain 100% local and secure.

## 🌟 Features

* **Smart PDF Ingestion:** Natively parses PDFs, automatically cleaning physical line breaks, trailing hyphens, and structural artifacts into clean markdown paragraphs.
* **Web Clipper:** A built-in lightweight terminal utility that extracts pure content from any article URL, stripping ads, trackers, and navigation clutter.
* **Deterministic Semantic Routing:** Uses local LLM orchestration to evaluate document context and mathematically route them to specific knowledge segments.
* **Intra-Segment AI Synthesis:** Automatically queries a local vector database to find related past entries *within* that specific category, using the LLM to generate a sharp 2-3 sentence bidirectional concept synthesis.
* **Obsidian Integration:** Generates native Markdown files with clean frontmatter, AI classification reasoning, and semantic internal links (`[[Note Name]]`).

---

## 🛠️ The Architecture Stack

- **Orchestration Engine:** Python 3.10+
    
- **Local LLM:** Ollama (`llama3`)
    
- **Vector Database:** ChromaDB (Persistent local instance)
    
- **Parsing & Scraping:** BeautifulSoup4, PyPDF, Re

---
## 🧠 How It Works (Technical Deep Dive)

### 1. Clutter-Free Web Scraping

The `clipper.py` script leverages `BeautifulSoup` to target only the paragraph (`<p>`) tags containing substantial text blocks. This effectively ignores headers, sidebars, advertisement text, and footers, resulting in clean, markdown-ready prose right from the source.

### 2. Smart Formatting Recovery

When raw PDFs are parsed, physical page margins force artificial newlines (`\n`) within lines. The cleanup engine inside `vault_manager.py` utilizes precise regular expressions to:

- Stitch hyphenated words back together (e.g., `infor-\nmation` becomes `information`).
    
- Differentiate between standard sentence ends and structural paragraph breaks.
    
- Capture bullet points (such as `•` or `●`) and isolate them cleanly onto new lines.
    

### 3. Isolated Vector Collections

To maintain strict context boundaries, ChromaDB initializes separate semantic collections for every generated category. When processing a new note inside the "Machine Learning" vertical, the pipeline queries _only_ the machine learning vector pool, ensuring that unrelated topics (e.g., business management or finance) never pollute the semantic comparison space.

---
## 🚀 Getting Started

### 1. Prerequisites

Ensure you have [Ollama](https://ollama.com/) installed and running locally on your machine, then pull the default model:

Bash

```
ollama pull llama3
```

### 2. Installation

Clone this repository to your local machine:

Bash

```
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```

Create and activate a virtual environment:

Bash

```
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

Install the required dependencies:

Bash

```
pip install chromadb ollama beautifulsoup4 requests pypdf
```

### 3. Configuration

Create a `config.py` file in the root directory to define your local paths:

Python

```
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INBOX_DIR = BASE_DIR / "inbox"
PROCESSED_DIR = BASE_DIR / "processed"
VAULT_DIR = Path("/path/to/your/Obsidian/Vault") # Replace with your actual Obsidian Vault path

# Ensure folders exist
INBOX_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)
```

---
## 💻 Usage

### Step 1: Clip an Article or Add a Document

To clip a web article straight to your processing queue, run the clipper utility:

Bash

```
python clipper.py
```

_Paste the target URL when prompted. The cleaned text will be saved straight to your `/inbox` folder._ Alternatively, you can manually drop any raw text or PDF file directly into the `/inbox` directory.

### Step 2: Run the Pipeline

Execute the main script to process all documents waiting in your inbox:

Bash

```
python main.py
```

## 🔒 Privacy & Data Sovereignty

This project adheres strictly to local execution patterns. No text data, metadata, or browsing history is ever transmitted over the network. All embedding generation, vector distance calculations, and contextual inferences happen purely on your local CPU/GPU hardware.

---
## 📂 Project Directory Structure

```text
SecondBrain/
│
├── inbox/               # Drop raw PDFs and text files here
├── processed/           # Processed files are automatically archived here
│
├── config.py            # Local path configurations (ignored by git)
├── clipper.py           # Web scraping utility 
├── vault_manager.py     # Main processing, vector database, & markdown engine
└── main.py              # Pipeline orchestrator
