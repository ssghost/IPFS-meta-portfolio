from app.engine.server import PortfolioRAG

def run_test():
    print("--- Starting RAG Pipeline Test ---")
    
    rag = PortfolioRAG(
        data_path="data/metadata.json", 
        db_path="chroma_db", 
        model_name="gpt-oss:20b-cloud"
    )
    
    default_query = "What quantitative finance or trading bot projects has Edmond worked on? Please explain the tech stack."
    user_input = input().strip()
    test_query = test_query = user_input if user_input else default_query
    print(f"\nUser Query: '{test_query}'\n")
    final_answer = rag.chat(test_query)
    print("\n" + "="*50)
    print("LLM Response:")
    print("="*50)
    print(final_answer)
    print("="*50)

if __name__ == "__main__":
    run_test()