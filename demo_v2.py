import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from sklearn.neighbors import NearestNeighbors

# --- 1. CONFIGURATION ---
MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

# --- 2. DATA (Same as before) ---
docs = [
    "How to configure EC2 instance types", "Setting up S3 bucket policies",
    "IAM role configuration", "Kubernetes pod auto-scaling",
    "Database migration endpoints", "API Gateway throttling",
    "VPC peering connections", "Linux kernel parameters",
    "Docker container networking", "Redis cluster sharding"
] * 10 

queries = [
    "How to configure EC2 instance", "s3 bucket permission error", # Covered
    "how to reduce my monthly aws bill", "pricing for reserved instances", # GAP
    "why is my invoice so high", "cost explorer api usage", # GAP
    "lambda function timeout settings", "credit card payment failure", # GAP
    "free tier limits for rds", "kubernetes pod crashing" # Covered
] * 10

print(f"Data Prep: {len(docs)} Docs, {len(queries)} Queries")

# --- 3. EMBEDDING & PROJECTION ---
print("Embedding...")
doc_embs = model.encode(docs)
query_embs = model.encode(queries)
all_embs = np.vstack([doc_embs, query_embs])

print("Running UMAP...")
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine', random_state=42)
embedding_2d = reducer.fit_transform(all_embs)

docs_2d = embedding_2d[:len(docs)]
queries_2d = embedding_2d[len(docs):]

# --- 4. THE MAGIC: AUTOMATED GAP DETECTION ---

# A. Cluster the Queries to find "Topics"
print("Clustering User Queries to find topics...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=2)
query_labels = clusterer.fit_predict(queries_2d)

# B. Check distances: Are these clusters near any documents?
# We train a NearestNeighbor index on the DOCUMENTS (Blue dots)
nn = NearestNeighbors(n_neighbors=1).fit(docs_2d)

print("\n--- ANALYSIS REPORT ---")
unique_labels = set(query_labels)
if -1 in unique_labels: unique_labels.remove(-1) # -1 is "noise" (random queries)

for label in unique_labels:
    # Get all queries in this cluster
    indices = [i for i, x in enumerate(query_labels) if x == label]
    cluster_points = queries_2d[indices]
    
    # Calculate distance from this cluster to the NEAREST Document
    distances, _ = nn.kneighbors(cluster_points)
    avg_distance = np.mean(distances)
    
    # If distance is high, it's a BLIND SPOT
    status = "✅ Covered"
    if avg_distance > 2.0: # Threshold (tuneable)
        status = "❌ BLIND SPOT (High Drift)"
    
    # Get a sample query to represent the topic
    sample_query = queries[indices[0]]
    
    print(f"Topic Cluster {label}: {status}")
    print(f"   Sample Query: '{sample_query}'")
    print(f"   Distance Score: {avg_distance:.2f}")
    print("-" * 30)

# --- 5. VISUALIZATION WITH CLUSTERS ---
plt.figure(figsize=(12, 8))
plt.scatter(docs_2d[:, 0], docs_2d[:, 1], c='lightgrey', label='Docs', alpha=0.5)
# Color queries by their cluster ID to show we identified them
scatter = plt.scatter(queries_2d[:, 0], queries_2d[:, 1], c=query_labels, cmap='Spectral', label='Queries', s=50, edgecolors='black')
plt.colorbar(scatter, label='Topic Cluster ID')
plt.title("Automated Gap Detection: Colored dots are distinct Query Topics")
plt.legend()
plt.show()