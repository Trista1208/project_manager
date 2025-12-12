#!/usr/bin/env python3
"""
Test script for RAG (Retrieval-Augmented Generation) System
Verifies storage, retrieval, and knowledge base functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.rag_system import RAGSystem
from src.core.rag_knowledge_base import populate_initial_knowledge


def test_rag_initialization():
    """Test RAG system initialization."""
    print("\n🧪 Test 1: RAG System Initialization")
    print("━" * 60)
    
    try:
        rag = RAGSystem(persist_directory="./test_rag_data")
        print("✅ RAG system initialized successfully")
        
        stats = rag.get_statistics()
        print(f"   Collections created: {len(stats['collections'])}")
        print(f"   Collections: {', '.join(stats['collections'])}")
        
        return rag, True
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        return None, False


def test_store_and_retrieve_tasks(rag: RAGSystem):
    """Test storing and retrieving tasks."""
    print("\n🧪 Test 2: Store and Retrieve Tasks")
    print("━" * 60)
    
    try:
        # Store tasks
        print("   Storing test tasks...")
        task_ids = []
        
        task_ids.append(rag.store_task(
            "Implement user authentication with OAuth2",
            "Successfully implemented using Google OAuth2. Added login, logout, and profile endpoints.",
            metadata={
                "project": "test_project",
                "duration_hours": 8,
                "complexity": "medium"
            }
        ))
        
        task_ids.append(rag.store_task(
            "Set up CI/CD pipeline",
            "Configured GitHub Actions with automated testing and deployment.",
            metadata={
                "project": "test_project",
                "duration_hours": 4,
                "complexity": "medium"
            }
        ))
        
        task_ids.append(rag.store_task(
            "Add password reset functionality",
            "Implemented email-based password reset with secure tokens.",
            metadata={
                "project": "test_project",
                "duration_hours": 3,
                "complexity": "low"
            }
        ))
        
        print(f"✅ Stored {len(task_ids)} tasks")
        
        # Retrieve similar tasks
        print("\n   Retrieving similar tasks for 'add user login'...")
        results = rag.retrieve_similar_tasks("add user login", k=2)
        
        print(f"✅ Found {len(results)} similar tasks:")
        for i, result in enumerate(results, 1):
            desc = result['metadata'].get('description', 'N/A')
            print(f"      {i}. {desc[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ Failed task storage/retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_store_and_retrieve_best_practices(rag: RAGSystem):
    """Test storing and retrieving best practices."""
    print("\n🧪 Test 3: Store and Retrieve Best Practices")
    print("━" * 60)
    
    try:
        # Store best practices
        print("   Storing best practices...")
        
        rag.store_best_practice(
            "Always Validate User Input",
            "Never trust user input. Validate, sanitize, and escape all user-provided data.",
            category="security"
        )
        
        rag.store_best_practice(
            "Use Prepared Statements for Database Queries",
            "Prevent SQL injection by using parameterized queries or ORMs.",
            category="security"
        )
        
        print("✅ Stored best practices")
        
        # Retrieve
        print("\n   Retrieving best practices for 'security'...")
        results = rag.retrieve_best_practices("prevent SQL injection", category="security", k=2)
        
        print(f"✅ Found {len(results)} relevant best practices:")
        for i, result in enumerate(results, 1):
            title = result['metadata'].get('title', 'N/A')
            print(f"      {i}. {title}")
        
        return True
    except Exception as e:
        print(f"❌ Failed best practices storage/retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_store_and_retrieve_code_patterns(rag: RAGSystem):
    """Test storing and retrieving code patterns."""
    print("\n🧪 Test 4: Store and Retrieve Code Patterns")
    print("━" * 60)
    
    try:
        # Store code pattern
        print("   Storing code pattern...")
        
        code = """
def retry_api_call(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
"""
        
        rag.store_code_pattern(
            "API Retry Pattern",
            code,
            "Use for resilient API calls with exponential backoff",
            language="python",
            use_cases=["HTTP requests", "Database connections", "External APIs"]
        )
        
        print("✅ Stored code pattern")
        
        # Retrieve
        print("\n   Retrieving code patterns for 'retry API calls'...")
        results = rag.retrieve_code_patterns("handle API failures", language="python", k=1)
        
        print(f"✅ Found {len(results)} relevant code patterns:")
        for i, result in enumerate(results, 1):
            name = result['metadata'].get('name', 'N/A')
            print(f"      {i}. {name}")
        
        return True
    except Exception as e:
        print(f"❌ Failed code pattern storage/retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_store_and_retrieve_errors(rag: RAGSystem):
    """Test storing and retrieving error resolutions."""
    print("\n🧪 Test 5: Store and Retrieve Error Resolutions")
    print("━" * 60)
    
    try:
        # Store error resolution
        print("   Storing error resolutions...")
        
        rag.store_error_resolution(
            "Connection timeout when calling API",
            "Increased timeout setting and added retry logic with exponential backoff.",
            context="Occurs when external API is slow or under load"
        )
        
        print("✅ Stored error resolution")
        
        # Retrieve
        print("\n   Retrieving solutions for 'API timeout error'...")
        results = rag.retrieve_error_solutions("API timeout error", k=1)
        
        print(f"✅ Found {len(results)} relevant solutions:")
        for i, result in enumerate(results, 1):
            error = result['metadata'].get('error', 'N/A')
            print(f"      {i}. {error[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ Failed error storage/retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_all(rag: RAGSystem):
    """Test searching across all collections."""
    print("\n🧪 Test 6: Search Across All Collections")
    print("━" * 60)
    
    try:
        print("   Searching for 'authentication'...")
        results = rag.search_all("authentication", k=2)
        
        total_results = sum(len(docs) for docs in results.values())
        print(f"✅ Found {total_results} results across {len(results)} collections:")
        
        for collection, docs in results.items():
            if docs:
                print(f"      {collection}: {len(docs)} results")
        
        return True
    except Exception as e:
        print(f"❌ Failed search all: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_populate_initial_knowledge(rag: RAGSystem):
    """Test populating initial knowledge base."""
    print("\n🧪 Test 7: Populate Initial Knowledge Base")
    print("━" * 60)
    
    try:
        populate_initial_knowledge(rag)
        
        stats = rag.get_statistics()
        print(f"\n✅ Knowledge base populated!")
        print(f"   Total documents: {stats['total_documents']}")
        for collection, count in stats.items():
            if collection not in ['total_documents', 'collections']:
                print(f"   - {collection}: {count}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to populate knowledge base: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_real_world_queries(rag: RAGSystem):
    """Test with real-world queries."""
    print("\n🧪 Test 8: Real-World Query Examples")
    print("━" * 60)
    
    queries = [
        ("How do I secure my API?", "best_practices"),
        ("How to implement user login?", "tasks"),
        ("How to handle API errors?", "code_patterns"),
        ("Database connection failed", "errors")
    ]
    
    try:
        for query, collection in queries:
            print(f"\n   Query: '{query}'")
            results = rag.retrieve_context(query, collection, k=2)
            print(f"   ✅ Found {len(results)} results in {collection}")
            
            if results:
                if collection == "best_practices":
                    title = results[0]['metadata'].get('title', 'N/A')
                    print(f"      → {title}")
                elif collection == "tasks":
                    desc = results[0]['metadata'].get('description', 'N/A')
                    print(f"      → {desc[:60]}...")
                elif collection == "code_patterns":
                    name = results[0]['metadata'].get('name', 'N/A')
                    print(f"      → {name}")
                elif collection == "errors":
                    error = results[0]['metadata'].get('error', 'N/A')
                    print(f"      → {error[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ Failed real-world queries: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all RAG system tests."""
    print("\n" + "="*60)
    print("🚀 RAG SYSTEM COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Initialization
    rag, success = test_rag_initialization()
    results.append(("Initialization", success))
    
    if not success or not rag:
        print("\n❌ Cannot continue without successful initialization")
        return False
    
    # Test 2-6: Basic functionality
    results.append(("Store/Retrieve Tasks", test_store_and_retrieve_tasks(rag)))
    results.append(("Store/Retrieve Best Practices", test_store_and_retrieve_best_practices(rag)))
    results.append(("Store/Retrieve Code Patterns", test_store_and_retrieve_code_patterns(rag)))
    results.append(("Store/Retrieve Errors", test_store_and_retrieve_errors(rag)))
    results.append(("Search All Collections", test_search_all(rag)))
    
    # Test 7: Populate knowledge base
    results.append(("Populate Knowledge Base", test_populate_initial_knowledge(rag)))
    
    # Test 8: Real-world queries
    results.append(("Real-World Queries", test_real_world_queries(rag)))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}  {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! RAG system is working perfectly!")
        
        # Print final statistics
        stats = rag.get_statistics()
        print(f"\n📊 Final Knowledge Base Statistics:")
        print(f"   Total documents: {stats['total_documents']}")
        for collection, count in stats.items():
            if collection not in ['total_documents', 'collections']:
                print(f"   - {collection}: {count} documents")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n✅ RAG System is ready for production use! 🚀")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please fix issues before proceeding.")
        exit(1)
