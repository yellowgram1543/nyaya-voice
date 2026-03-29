import chromadb

def retrieve_cases(query: str, category: str = None, top_k: int = 2) -> str:
    """Takes the user's specific complaint and searches the vector database for the top 2 legal precedents.
    Includes a category filter and a confidence (distance) check."""
    try:
        # Connect to the offline database
        client = chromadb.PersistentClient(path="./library_db")
        collection = client.get_collection(name="indian_consumer_cases")
        
        # Build the query filter if a category is provided
        where_filter = {"category": category} if category else None
        
        # Perform the Semantic Search
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )
        
        # Extract documents and distances (similarity scores)
        documents = results.get('documents', [[]])[0]
        distances = results.get('distances', [[]])[0]
        
        if not documents:
            return ""
            
        formatted_cases = "SUPPORTING LEGAL PRECEDENTS (Incorporate these actual case laws into Para 4):\n"
        cases_added = 0
        
        for idx, (doc, dist) in enumerate(zip(documents, distances)):
            # Distances in ChromaDB (using default L2) mean: lower is better. 
            # 1.5 is a safe "relevance" threshold.
            if dist < 1.5:
                formatted_cases += f"Precedent {idx+1}: {doc}\n"
                cases_added += 1
        
        return formatted_cases if cases_added > 0 else ""
        
    except Exception as e:
        print(f"RAG Error: {e}")
        return ""
