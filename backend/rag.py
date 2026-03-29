import chromadb

def retrieve_cases(query: str, category: str = None, top_k: int = 4) -> str:
    """Takes the user's complaint and searches for relevant legal precedents AND statutory law (CPA 2019)."""
    try:
        client = chromadb.PersistentClient(path="./library_db")
        collection = client.get_collection(name="indian_consumer_cases")
        
        # Build the filter: Get the specific category AND the 'general' statutory sections
        if category and category != "general":
            where_filter = {"$or": [
                {"category": category},
                {"category": "general"}
            ]}
        else:
            where_filter = None
        
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )
        
        documents = results.get('documents', [[]])[0]
        distances = results.get('distances', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not documents:
            return ""
            
        statutory_output = "STATUTORY LAW (Quote these Sections in Para 4):\n"
        precedent_output = "LEGAL PRECEDENTS (Cite these Cases in Para 4):\n"
        
        stats_added = 0
        cases_added = 0
        
        for doc, dist, meta in zip(documents, distances, metadatas):
            if dist < 1.6: # Slightly wider threshold for statutory relevance
                if meta.get('category') == 'general':
                    statutory_output += f"- {doc}\n"
                    stats_added += 1
                else:
                    precedent_output += f"- {doc}\n"
                    cases_added += 1
        
        final_output = ""
        if stats_added > 0:
            final_output += statutory_output + "\n"
        if cases_added > 0:
            final_output += precedent_output
            
        return final_output
        
    except Exception as e:
        print(f"RAG Error: {e}")
        return ""

