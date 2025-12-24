# 🏳️ semantic-coverage

> **The "Code Coverage" tool for RAG Knowledge Bases.**  
> *Automated detection of knowledge gaps, hallucination spots, and representation bias in Vector Databases.*

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Status](https://img.shields.io/badge/status-active-success)

## 🛑 The Problem

In software engineering, we track **Code Coverage** to prevent bugs.  
In AI engineering, we ship RAG (Retrieval Augmented Generation) systems without **Semantic Coverage**.

Engineers often don't know:
1. **Blind Spots:** What are users asking that our Vector DB has *zero* context for?
2. **Data Drift:** How is user intent shifting away from our indexed documentation over time?
3. **Hallucination Triggers:** Which clusters of queries systematically yield low-confidence retrieval?

## ⚡ The Solution: `semantic-coverage`

This tool provides semantic observability by projecting both **Documents** (Knowledge) and **User Queries** (Intent) into a shared latent space (using UMAP). It then uses density-based clustering (HDBSCAN) to identify "Red Zones"—areas of high user density but low document density.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Semantic+Coverage+Dashboard+Visualization)

## 🛠️ Tech Stack

* **Math Engine:** `Sentence-Transformers` (SBERT), `UMAP`, `HDBSCAN`, `Scikit-Learn`
* **Backend:** FastAPI (Async inference)
* **Frontend:** React + Vite, Plotly.js (Interactive Scatter Plots)
* **Extensibility:** Plugin architecture for Vector DBs

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/YOUR_USERNAME/semantic-coverage.git
cd semantic-coverage

# Backend Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend Setup
cd frontend
npm install
```

### 2. Run the Stack

```bash
# Terminal 1: Backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
npm run dev
```

### 3. Usage

Navigate to http://localhost:5173. Paste your JSON export of queries and documents. The system will auto-generate a "Gap Report" identifying missing topics.

## 🔌 Enterprise Connectors

semantic-coverage is designed to be database-agnostic. We support a plugin architecture for major Vector Stores:

```python
from app.core.connectors import get_connector

# Connect to Pinecone
db = get_connector("pinecone", api_key="...", index_name="knowledge-base-v1")
docs = db.fetch_documents(limit=5000)

# Connect to ChromaDB
db = get_connector("chroma", collection_name="support_tickets")
docs = db.fetch_documents()
```

## 🏗️ Architecture

1. **Ingestion:** Text is converted to 384-dim embeddings (all-MiniLM-L6-v2).
2. **Projection:** High-dimensional vectors are reduced to 2D via UMAP.
3. **Clustering:** User queries are clustered to find distinct "Topics."
4. **Gap Analysis:** For each query cluster, we calculate the Centroid Distance to the nearest Document neighbor.
5. **Scoring:** Clusters exceeding the distance threshold (0.7) are flagged as `blind_spot`.

## 📜 License

MIT

---

## 🚀 Launch It to GitHub

Now, let's put this live.

### 1. Go to GitHub.com and create a **New Repository**

* **Name:** `semantic-coverage`
* **Description:** *Automated detection of knowledge gaps and blind spots in RAG vector stores.*
* **Public:** Yes.
* **Do NOT** initialize with README (we already have one).

### 2. Push your Code

In your VS Code terminal (root folder):

```bash
# 1. Add your remote (Replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/semantic-coverage.git

# 2. Rename branch to main (best practice)
git branch -M main

# 3. Push
git push -u origin main
```

---
