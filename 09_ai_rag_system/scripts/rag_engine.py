"""
AI RAG Engine
Simulates the Retrieval-Augmented Generation lifecycle.
1. Retrieves relevant context from the knowledge base.
2. Augments the query with detailed context.
3. Generates high-fidelity business insights (simulated LLM).
"""

import pandas as pd
import sqlite3
import os
import json

class RAGEngine:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.base_path, 'data', 'warehouse.db')
        self.csv_path = os.path.join(self.base_path, 'data', 'knowledge_base.csv')

    def retrieve_context(self, query):
        """Keyword-based search simulator"""
        df = pd.read_csv(self.csv_path)
        keywords = [k.lower() for k in query.split() if len(k) > 3]
        
        if not keywords:
            keywords = [query.lower()]
            
        # Search across topic, category, and content for ANY keyword
        mask = df['topic'].str.lower().apply(lambda x: any(k in x for k in keywords)) | \
               df['category'].str.lower().apply(lambda x: any(k in x for k in keywords)) | \
               df['content'].str.lower().apply(lambda x: any(k in x for k in keywords))
        
        results = df[mask]
        return results.to_dict('records')

    def generate_insight(self, query):
        """Simulated LLM Generation based on retrieved context"""
        context = self.retrieve_context(query)
        
        if not context:
            return {
                "query": query,
                "answer": "I don't have specific data on that topic in my current knowledge base.",
                "sources": []
            }
        
        # Simulated LLM Logic based on retrieved values
        source_topics = [c['topic'] for c in context]
        main_topic = context[0]
        
        # Custom insight based on the first retrieved match
        answer = f"Based on the analysis of {main_topic['topic']}, {main_topic['content']} "
        
        if main_topic['category'] == 'Clinical' and 'readmission' in main_topic['topic'].lower():
            answer += " This exceeds the safety benchmark and suggests immediate review of post-discharge protocols is required."
        elif main_topic['category'] == 'Finance':
            answer += f" This reflects a healthy ROI and supports further investment in current digital channels."
        elif main_topic['category'] == 'Customer' and 'churn' in main_topic['topic'].lower():
            answer += " Low engagement is a leading indicator; the customer success team should trigger an automated outreach campaign for this segment."

        return {
            "query": query,
            "answer": answer,
            "retrieved_data": context,
            "sources": source_topics,
            "category": main_topic['category']
        }

def main():
    print("🤖 AI RAG Engine Test Drive...")
    rag = RAGEngine()
    
    # Pre-baked demonstration queries
    test_queries = [
        "Tell me about revenue growth",
        "What is the status of readmission rates?",
        "What drives customer churn?"
    ]
    
    demonstration_results = []
    for q in test_queries:
        print(f"\nUser: {q}")
        result = rag.generate_insight(q)
        print(f"AI: {result['answer']}")
        demonstration_results.append(result)
        
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'sample_queries.json'), 'w') as f:
        json.dump(demonstration_results, f, indent=4)
        
    print(f"\n✅ Demonstration results saved to 'outputs/sample_queries.json'")

if __name__ == '__main__':
    main()
