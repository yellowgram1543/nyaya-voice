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
    
    # Statutory Sections of the Consumer Protection Act, 2019
    statutory_docs = [
        "Section 2(7) of the Consumer Protection Act, 2019 defines a 'Consumer' as any person who buys any goods or hires any services for a consideration. This includes offline and online transactions, and electronic means, ensuring wide protection for individuals against commercial exploitation.",
        "Section 2(11) of the Consumer Protection Act, 2019 defines 'Deficiency' as any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance which is required to be maintained by or under any law for the time being in force or has been undertaken to be performed by a person in pursuance of a contract or otherwise in relation to any service.",
        "Section 2(47) of the Consumer Protection Act, 2019 defines 'Unfair Trade Practice' as a trade practice which, for the purpose of promoting the sale, use or supply of any goods or for the provision of any service, adopts any unfair method or unfair or deceptive practice including (i) making false or misleading representations about the standard, quality, quantity, grade, composition, style or model of goods or services.",
        "Section 35 of the Consumer Protection Act, 2019 provides the procedure for filing a complaint before the District Commission. It mandates that a complaint may be filed by a consumer to whom such goods are sold or delivered, or any service is provided or agreed to be provided.",
        "Section 39 of the Consumer Protection Act, 2019 outlines the findings and orders that the District Commission can pass, including directing the opposite party to remove the defect, replace the goods, return the price, or pay compensation to the consumer for any loss or injury suffered due to negligence.",
        "Section 2(1) of the Consumer Protection Act, 2019 defines 'Adulterant' and 'Advertisement', establishing that misleading advertisements which give false descriptions of a product or service are strictly prohibited and punishable under the Act."
    ]
    
    statutory_ids = [f"statute_{i}" for i in range(len(statutory_docs))]
    statutory_metadatas = [
        {"category": "general"},
        {"category": "general"},
        {"category": "general"},
        {"category": "general"},
        {"category": "general"},
        {"category": "general"}
    ]

    print("Injecting Landmark Cases into Vector Space...")
    collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    print("Injecting Statutory Law (CPA 2019 Sections) into Vector Space...")
    collection.upsert(
        documents=statutory_docs,
        ids=statutory_ids,
        metadatas=statutory_metadatas
    )
    
    print("Database Seeded Successfully! The Library is now fully armed with both Supreme Court Precedents and Statutory Laws.")

if __name__ == "__main__":
    setup_precedents()
