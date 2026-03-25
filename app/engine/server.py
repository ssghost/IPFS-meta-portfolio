import json
import chromadb
import os
import requests
from chromadb.utils import embedding_functions
from groq import Groq

class PortfolioRAG:
    def __init__(self, data_path="data/metadata.json", db_path="chroma_db", model_name="gpt-oss:20b-cloud"):
        self.data_path = data_path
        self.db_path = db_path
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
        else:
            print("WARNING: GROQ_API_KEY environment variable not set!")
        self.collection = None
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        print("Initializing Local Vector Database (ChromaDB)...")
        client = chromadb.PersistentClient(path=self.db_path)
        default_ef = embedding_functions.DefaultEmbeddingFunction()

        self.collection = client.get_or_create_collection(
            name="meta_portfolio",
            embedding_function=default_ef
        )
        
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
            meta_dict = {
                "project": project_name, 
                "domain": domain,
                "category": category,
                "link": link,
                "key_achievement": achievement,
                "challenge": challenge
            }

            if item.get("language"):
                meta_dict["language"] = ", ".join(item["language"])  
            if item.get("tech_stack"):
                meta_dict["tech_stack"] = ", ".join(item["tech_stack"])
            if item.get("abstract"):
                meta_dict["abstract"] = item["abstract"]

            metadatas.append(meta_dict)
            ids.append(f"doc_{i}")
            
        self.collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Knowledge Base ready! ({len(documents)} items stored)\n")

    def retrieve_context(self, query, n_results=2):
        if not self.collection:
            return "", []
            
        print("Retrieving relevant context from ChromaDB...")
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )        
        context_text = ""
        source_metadata = []
        
        if results and results["documents"] and results["documents"][0]:
            context_text = "\n\n".join(results["documents"][0])
            if "metadatas" in results and results["metadatas"][0]:
                source_metadata = results["metadatas"][0]
                
        return context_text, source_metadata

    def generate_response(self, query, context):
        print(f"Asking local Ollama ({self.ollama_model})...")
        
        prompt = f"""You are an AI assistant representing the portfolio of Edmond Song, a Senior DeFi and AI Research Engineer.
        Based ONLY on the following context about Edmond's projects and articles, answer the user's question clearly and professionally.

        Context:
        {context}

        Question:
        {query}

        Answer:"""

        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192", 
                temperature=0.3, 
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Groq API: {str(e)}"

    def chat(self, query):
        context_text, source_metadata = self.retrieve_context(query)
        if context_text:
            ai_response = self.generate_response(query, context_text)
            return {
                "answer": ai_response,
                "metadata": source_metadata
            }
        
        return {
            "answer": "I don't have enough context to answer that.",
            "metadata": []
        }