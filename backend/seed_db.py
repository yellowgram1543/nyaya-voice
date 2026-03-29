import chromadb

def setup_precedents():
    print("Initializing offline ChromaDB Database...")
    client = chromadb.PersistentClient(path="./library_db")
    
    # Create a vector collection for Indian legal judgments
    collection = client.get_or_create_collection(name="indian_consumer_cases")
    
    # 5 Famous landmark Indian Consumer Protection cases
    documents = [
        "In 'C.N. Anantharam V. Fiat India Ltd.' (2010), the Supreme Court held that if a brand-new vehicle or electronic appliance suffers from recurrent, severe manufacturing defects shortly after purchase, the manufacturer is absolutely liable to replace the entire unit or provide a full refund, rather than forcing the consumer into constant patchwork repairs.",
        "In 'Experion Developers Pvt. Ltd. v. Sushma Ashok Shiroor' (2022), the Supreme Court ruled that a consumer has an absolute, indefeasible right to claim a full refund along with heavy compensation if the service provider completely fails to deliver the promised outcome or service within the stipulated and reasonable timeframe.",
        "In 'Air France Vs. O.P. Srivastava' (2018), the National Consumer Commission stated that severe negligence by an airline or logistics company resulting in heavy delays, property loss/damage, or arbitrary denial of service strictly amounts to an egregious deficiency in service, warranting punitive financial compensation for mental agony and harassment.",
        "In 'Bunga Daniel Babu Vs. Sri Vasudeva Constructions' (2016), it was established that individual consumers entering into agreements for housing, personal livelihood, or massive financial investments strictly fall under the definition of 'Consumer' under Section 2(7) and are protected against Unfair Trade Practices.",
        "In 'Samira Kohli Vs. Dr. Prabha Manchanda' (2008), regarding severe service negligence, the Supreme Court mandated that the fundamental failure to provide adequate, explicitly promised care, or ignoring vital client instructions constitutes a severe deficiency in service under Section 2(11) of the Act."
    ]
    
    ids = ["case_defective_goods", "case_service_delay", "case_airline_negligence", "case_housing_unfair_trade", "case_general_negligence"]
    metadatas = [
        {"category": "goods"},
        {"category": "service"},
        {"category": "airline"},
        {"category": "housing"},
        {"category": "medical"}
    ]
    
    print("Injecting Landmark Cases into Vector Space (Converting text into Mathematical Coordinates)...")
    collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )
    
    print("Database Seeded Successfully! The Library is now fully armed with Supreme Court Precedents.")

if __name__ == "__main__":
    setup_precedents()
