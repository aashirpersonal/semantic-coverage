import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import umap
from sklearn.neighbors import KernelDensity

# --- 1. CONFIGURATION ---
MODEL_NAME = 'all-MiniLM-L6-v2'  # Small, fast model perfect for local dev
print(f"Loading model: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

# --- 2. GENERATE DUMMY DATA ---
# Scenario: Your docs are technical (AWS-style), but users are asking about billing.

# The "Knowledge Base" (Blue Dots)
docs = [
    "How to configure EC2 instance types",
    "Setting up S3 bucket policies for public access",
    "IAM role configuration for lambda functions",
    "Kubernetes pod auto-scaling settings",
    "Database migration service endpoints",
    "API Gateway throttling limits and quotas",
    "VPC peering connections between regions",
    "Linux kernel parameters for high performance",
    "Docker container networking modes",
    "Redis cluster sharding strategies"
] * 5  # Duplicate to simulate volume

# The "User Queries" (Red Dots) -> Notice the "Billing" drift
queries = [
    "How to configure EC2 instance",            # Covered
    "s3 bucket permission error",               # Covered
    "how to reduce my monthly aws bill",        # GAP!
    "pricing for reserved instances",           # GAP!
    "why is my invoice so high",                # GAP!
    "cost explorer api usage",                  # GAP!
    "lambda function timeout settings",         # Covered
    "credit card payment failure support",      # GAP!
    "free tier limits for rds",                 # GAP!
    "kubernetes pod crashing",                  # Covered
] * 5

print(f"Data Prep: {len(docs)} Docs, {len(queries)} Queries")

# --- 3. EMBEDDING (The "Heavy" Lifting) ---
print("Embedding data (this might take 10-20s on first run)...")
doc_embeddings = model.encode(docs)
query_embeddings = model.encode(queries)

# Stack them to project into the same 2D space
all_embeddings = np.vstack([doc_embeddings, query_embeddings])

# --- 4. DIMENSIONALITY REDUCTION (The "Map") ---
print("Running UMAP to map 384 dimensions -> 2 dimensions...")
reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='cosine', random_state=42)
embedding_2d = reducer.fit_transform(all_embeddings)

# Split back into Docs vs Queries
docs_2d = embedding_2d[:len(docs)]
queries_2d = embedding_2d[len(docs):]

# --- 5. VISUALIZATION (The Output) ---
plt.figure(figsize=(10, 8))
plt.title("Semantic Coverage: Knowledge Base (Blue) vs. User Intent (Red)")

# Plot Docs (Blue)
plt.scatter(docs_2d[:, 0], docs_2d[:, 1], c='blue', alpha=0.5, label='Existing Docs', s=100)

# Plot Queries (Red)
plt.scatter(queries_2d[:, 0], queries_2d[:, 1], c='red', alpha=0.6, label='User Queries', s=100, edgecolors='black')

plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()

print("✅ Analysis Complete. Displaying plot...")
plt.show()