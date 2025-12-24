import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from sklearn.neighbors import NearestNeighbors
from typing import List, Dict

class SemanticCoverageEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print("Loading Model...")
        self.model = SentenceTransformer(model_name)
    
    def analyze(self, docs: List[str], queries: List[str]) -> Dict:
        """
        Core pipeline: Embed -> UMAP -> Cluster -> Measure Gaps
        """
        # 1. Embed
        doc_embs = self.model.encode(docs)
        query_embs = self.model.encode(queries)
        
        # 2. UMAP Projection (2D)
        # We handle the case where data is too small for UMAP default
        n_neighbors = min(15, len(docs) - 1)
        all_embs = np.vstack([doc_embs, query_embs])
        
        reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=0.1, metric='cosine', random_state=42)
        embedding_2d = reducer.fit_transform(all_embs)
        
        # Split back
        docs_2d = embedding_2d[:len(docs)]
        queries_2d = embedding_2d[len(docs):]
        
        # 3. Clustering Queries
        # If dataset is tiny, we force smaller cluster sizes
        min_cluster_size = max(2, int(len(queries) * 0.05))
        clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=1)
        query_labels = clusterer.fit_predict(queries_2d)
        
        # 4. Gap Detection
        nn = NearestNeighbors(n_neighbors=1).fit(docs_2d)
        
        results = []
        unique_labels = set(query_labels)
        if -1 in unique_labels: unique_labels.remove(-1) # Ignore noise
        
        for label in unique_labels:
            indices = [i for i, x in enumerate(query_labels) if x == label]
            cluster_points = queries_2d[indices]
            
            # Distance to nearest document
            distances, _ = nn.kneighbors(cluster_points)
            avg_dist = float(np.mean(distances))
            
            # Heuristic for status
            status = "covered" if avg_dist < 0.7 else "blind_spot"
            
            # Representative Query (Just take the first one for now)
            sample_query = queries[indices[0]]
            
            results.append({
                "cluster_id": int(label),
                "status": status,
                "distance_score": round(avg_dist, 2),
                "sample_query": sample_query,
                "query_count": len(indices)
            })
            
        return {
            "meta": {
                "total_docs": len(docs),
                "total_queries": len(queries)
            },
            "clusters": results,
            # We return coordinates so the Frontend can plot them later
            "plot_data": {
                "docs_x": docs_2d[:, 0].tolist(),
                "docs_y": docs_2d[:, 1].tolist(),
                "queries_x": queries_2d[:, 0].tolist(),
                "queries_y": queries_2d[:, 1].tolist(),
                "query_labels": query_labels.tolist()
            }
        }