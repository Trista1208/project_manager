#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) System
Stores and retrieves project knowledge for intelligent context-aware assistance.
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class RAGSystem:
    """
    Retrieval-Augmented Generation System for DevOps project knowledge.
    
    Stores:
    - Past project tasks and outcomes
    - Code templates and patterns
    - Best practices and conventions
    - Error resolutions and learnings
    - Team documentation
    
    Retrieves:
    - Relevant context for new tasks
    - Similar past projects
    - Applicable best practices
    - Successful implementation patterns
    """
    
    def __init__(self, persist_directory: str = "./rag_data"):
        """
        Initialize RAG system with vector database.
        
        Args:
            persist_directory: Directory to store vector database
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model (free, runs locally!)
        print("🔄 Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")
        
        # Create or get collections
        self.collections = {
            'tasks': self._get_or_create_collection('tasks', 
                "Past project tasks and their outcomes"),
            'best_practices': self._get_or_create_collection('best_practices',
                "DevOps best practices and conventions"),
            'code_patterns': self._get_or_create_collection('code_patterns',
                "Code templates and successful patterns"),
            'errors': self._get_or_create_collection('errors',
                "Error resolutions and troubleshooting"),
            'documentation': self._get_or_create_collection('documentation',
                "Project documentation and guides")
        }
    
    def _get_or_create_collection(self, name: str, description: str):
        """Get or create a collection in ChromaDB."""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(
                name=name,
                metadata={"description": description}
            )
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text."""
        return self.embedding_model.encode(text).tolist()
    
    def store_task(
        self,
        task_description: str,
        outcome: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a completed task and its outcome.
        
        Args:
            task_description: Description of the task
            outcome: How the task was completed (success/failure/learnings)
            metadata: Additional metadata (project, date, cost, etc.)
        
        Returns:
            Document ID
        """
        doc_id = f"task_{datetime.now().timestamp()}"
        
        full_text = f"{task_description}\nOutcome: {outcome}"
        embedding = self._generate_embedding(full_text)
        
        meta = metadata or {}
        meta.update({
            "type": "task",
            "timestamp": datetime.now().isoformat(),
            "description": task_description,
            "outcome": outcome
        })
        
        self.collections['tasks'].add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[full_text],
            metadatas=[meta]
        )
        
        return doc_id
    
    def store_best_practice(
        self,
        title: str,
        content: str,
        category: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a best practice or convention.
        
        Args:
            title: Title of the best practice
            content: Detailed content
            category: Category (e.g., "security", "testing", "deployment")
            metadata: Additional metadata
        
        Returns:
            Document ID
        """
        doc_id = f"best_practice_{datetime.now().timestamp()}"
        
        full_text = f"{title}\n{content}"
        embedding = self._generate_embedding(full_text)
        
        meta = metadata or {}
        meta.update({
            "type": "best_practice",
            "title": title,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        
        self.collections['best_practices'].add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[full_text],
            metadatas=[meta]
        )
        
        return doc_id
    
    def store_code_pattern(
        self,
        name: str,
        code: str,
        description: str,
        language: str = "python",
        use_cases: List[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a code template or pattern.
        
        Args:
            name: Name of the pattern
            code: The actual code
            description: When/how to use this pattern
            language: Programming language
            use_cases: List of applicable use cases
            metadata: Additional metadata
        
        Returns:
            Document ID
        """
        doc_id = f"code_{datetime.now().timestamp()}"
        
        use_cases_text = "\n".join(use_cases) if use_cases else ""
        full_text = f"{name}\n{description}\n{use_cases_text}\nCode:\n{code}"
        embedding = self._generate_embedding(full_text)
        
        meta = metadata or {}
        meta.update({
            "type": "code_pattern",
            "name": name,
            "language": language,
            "timestamp": datetime.now().isoformat()
        })
        
        self.collections['code_patterns'].add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[full_text],
            metadatas=[meta]
        )
        
        return doc_id
    
    def store_error_resolution(
        self,
        error_message: str,
        solution: str,
        context: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store an error and its resolution.
        
        Args:
            error_message: The error message/description
            solution: How the error was resolved
            context: Additional context about when this error occurs
            metadata: Additional metadata
        
        Returns:
            Document ID
        """
        doc_id = f"error_{datetime.now().timestamp()}"
        
        full_text = f"Error: {error_message}\nContext: {context}\nSolution: {solution}"
        embedding = self._generate_embedding(full_text)
        
        meta = metadata or {}
        meta.update({
            "type": "error_resolution",
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        })
        
        self.collections['errors'].add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[full_text],
            metadatas=[meta]
        )
        
        return doc_id
    
    def retrieve_context(
        self,
        query: str,
        collection_name: str = 'tasks',
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: Search query
            collection_name: Which collection to search
            k: Number of results to return
            filters: Optional metadata filters
        
        Returns:
            List of relevant documents with metadata
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection {collection_name} not found")
        
        query_embedding = self._generate_embedding(query)
        
        results = self.collections[collection_name].query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filters
        )
        
        # Format results
        documents = []
        if results['ids'] and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                documents.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return documents
    
    def retrieve_similar_tasks(
        self,
        task_description: str,
        k: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieve similar past tasks."""
        return self.retrieve_context(task_description, 'tasks', k)
    
    def retrieve_best_practices(
        self,
        topic: str,
        category: Optional[str] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant best practices."""
        filters = {"category": category} if category else None
        return self.retrieve_context(topic, 'best_practices', k, filters)
    
    def retrieve_code_patterns(
        self,
        description: str,
        language: Optional[str] = None,
        k: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant code patterns."""
        filters = {"language": language} if language else None
        return self.retrieve_context(description, 'code_patterns', k, filters)
    
    def retrieve_error_solutions(
        self,
        error_message: str,
        k: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieve solutions for similar errors."""
        return self.retrieve_context(error_message, 'errors', k)
    
    def search_all(
        self,
        query: str,
        k: int = 3
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across all collections.
        
        Args:
            query: Search query
            k: Number of results per collection
        
        Returns:
            Dictionary with results from each collection
        """
        results = {}
        for collection_name in self.collections.keys():
            results[collection_name] = self.retrieve_context(query, collection_name, k)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored knowledge."""
        stats = {}
        for name, collection in self.collections.items():
            stats[name] = collection.count()
        
        stats['total_documents'] = sum(stats.values())
        stats['collections'] = list(self.collections.keys())
        
        return stats
    
    def export_knowledge(self, output_file: str):
        """Export all knowledge to a JSON file."""
        knowledge = {}
        
        for name, collection in self.collections.items():
            results = collection.get()
            knowledge[name] = {
                'ids': results['ids'],
                'documents': results['documents'],
                'metadatas': results['metadatas']
            }
        
        with open(output_file, 'w') as f:
            json.dump(knowledge, f, indent=2)
        
        print(f"✅ Knowledge exported to {output_file}")
    
    def reset(self):
        """Reset all collections (delete all data)."""
        for name in self.collections.keys():
            self.client.delete_collection(name)
        
        # Recreate collections
        self.collections = {
            'tasks': self._get_or_create_collection('tasks', 
                "Past project tasks and their outcomes"),
            'best_practices': self._get_or_create_collection('best_practices',
                "DevOps best practices and conventions"),
            'code_patterns': self._get_or_create_collection('code_patterns',
                "Code templates and successful patterns"),
            'errors': self._get_or_create_collection('errors',
                "Error resolutions and troubleshooting"),
            'documentation': self._get_or_create_collection('documentation',
                "Project documentation and guides")
        }
        
        print("✅ RAG system reset")


if __name__ == "__main__":
    # Quick test
    print("🧪 Testing RAG System...")
    
    rag = RAGSystem()
    
    # Store some test data
    rag.store_task(
        "Implement user authentication",
        "Successfully implemented using OAuth2 with JWT tokens",
        metadata={"project": "test", "duration_hours": 8}
    )
    
    rag.store_best_practice(
        "Always Use Environment Variables for Secrets",
        "Never hardcode API keys or secrets. Use .env files and environment variables.",
        category="security"
    )
    
    # Retrieve
    results = rag.retrieve_similar_tasks("Add login feature", k=1)
    print(f"\n✅ Found {len(results)} similar tasks")
    
    if results:
        print(f"   Similar task: {results[0]['metadata']['description']}")
    
    stats = rag.get_statistics()
    print(f"\n📊 Statistics: {stats}")
    
    print("\n✅ RAG System working!")
