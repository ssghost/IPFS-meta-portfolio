import json
import chromadb
import os
import requests

class PortfolioRAG:
    def __init__(self, data_path="data/metadata.json", db_path="chroma_db", model_name="gpt-oss:20b-cloud"):
        self.data_path = data_path
        self.db_path = db_path
        self.ollama_model = model_name
        self.ollama_api_url = "http://localhost:11434/api/generate"
        self.collection = None
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        print("Initializing Local Vector Database (ChromaDB)...")
        client = chromadb.PersistentClient(path=self.db_path)
        self.collection = client.get_or_create_collection(name="meta_portfolio")
        
        if not os.path.exists(self.data_path):
            print(f"Error: {self.data_path} not found.")
            return
            
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            data = [data]
            
        documents = []
        metadatas = []
        ids = []
        
        for i, item in enumerate(data):
            project_name = item.get("project", f"Project_{i}")
            category = item.get("category", "Unknown")
            domain = item.get("domain", "Unknown Domain")
            link = item.get("link", "No link provided")
            achievement = item.get("key_achievement", "")
            challenge = item.get("challenge", "")
            
            extra_info = ""
            if category.lower() == "project" or "language" in item:
                language = ", ".join(item.get("language", []))
                tech_stack = ", ".join(item.get("tech_stack", []))
                extra_info = (
                    f"Languages: {language}\n"
                    f"Tech Stack: {tech_stack}"
                )
            elif category.lower() == "article" or "abstract" in item:
                abstract = item.get("abstract", "")
                extra_info = f"Abstract: {abstract}"
            
            doc_text = (
                f"Project Name: {project_name}\n"
                f"Domain: {domain}\n"
                f"Category: {category}\n"
                f"Link: {link}\n"
                f"{extra_info}\n"
                f"Key Achievement: {achievement}\n"
                f"Technical Challenge: {challenge}"
            )
            
            documents.append(doc_text)
            metadatas.append({"project": project_name, "category": category})
            ids.append(f"doc_{i}")
            
        self.collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Knowledge Base ready! ({len(documents)} items stored)\n")

    def retrieve_context(self, query, n_results=2):
        if not self.collection:
            return ""
            
        print("Retrieving relevant context from ChromaDB...")
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if results and results["documents"] and results["documents"][0]:
            return "\n\n".join(results["documents"][0])
        return ""

    def generate_response(self, query, context):
        print(f"Asking local Ollama ({self.ollama_model})...")
        
        prompt = f"""You are an AI assistant representing the portfolio of Edmond Song, a Senior DeFi and AI Research Engineer.
        Based ONLY on the following context about Edmond's projects and articles, answer the user's question clearly and professionally.

        Context:
        {context}

        Question:
        {query}

        Answer:"""

        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_api_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

    def chat(self, query):
        context = self.retrieve_context(query)
        if context:
            return self.generate_response(query, context)
        return "I don't have enough context to answer that."