#!/usr/bin/env python3
"""
Quick Demo: RAG System in Action
Shows how the RAG system provides context-aware assistance.
"""

import sys
from src.core.rag_system import RAGSystem
from src.core.rag_knowledge_base import populate_initial_knowledge


def demo_rag_system():
    """Demonstrate RAG system capabilities."""
    
    print("\n" + "="*70)
    print("🤖 RAG SYSTEM DEMO - Context-Aware AI Assistant")
    print("="*70)
    
    # Initialize
    print("\n📚 Initializing RAG system...")
    rag = RAGSystem(persist_directory="./rag_data")
    
    # Populate knowledge base
    print("📖 Loading DevOps knowledge base...")
    populate_initial_knowledge(rag)
    
    # Show statistics
    stats = rag.get_statistics()
    print(f"\n✅ Knowledge base ready!")
    print(f"   Total documents: {stats['total_documents']}")
    print(f"   - Tasks: {stats['tasks']}")
    print(f"   - Best Practices: {stats['best_practices']}")
    print(f"   - Code Patterns: {stats['code_patterns']}")
    print(f"   - Error Solutions: {stats['errors']}")
    
    # Demo scenarios
    print("\n" + "="*70)
    print("🎯 DEMO SCENARIOS")
    print("="*70)
    
    # Scenario 1: Task Planning
    print("\n📋 Scenario 1: Context-Aware Task Planning")
    print("-" * 70)
    print("User Request: 'I need to add user login to my app'")
    print("\nRAG retrieves similar past tasks...")
    
    similar_tasks = rag.retrieve_similar_tasks("add user login", k=3)
    print(f"\n✅ Found {len(similar_tasks)} similar tasks:")
    for i, task in enumerate(similar_tasks, 1):
        desc = task['metadata'].get('description', 'N/A')
        outcome = task['metadata'].get('outcome', 'N/A')
        print(f"\n   {i}. {desc}")
        print(f"      Outcome: {outcome[:80]}...")
        if 'duration_hours' in task['metadata']:
            print(f"      Duration: {task['metadata']['duration_hours']} hours")
    
    # Scenario 2: Security Best Practices
    print("\n" + "-"*70)
    print("🔒 Scenario 2: Security Best Practices")
    print("-" * 70)
    print("User Question: 'How do I secure my API endpoints?'")
    print("\nRAG retrieves relevant best practices...")
    
    security_practices = rag.retrieve_best_practices("API security", category="security", k=3)
    print(f"\n✅ Found {len(security_practices)} relevant practices:")
    for i, practice in enumerate(security_practices, 1):
        title = practice['metadata'].get('title', 'N/A')
        print(f"\n   {i}. {title}")
        content_preview = practice['content'].split('\n')[1][:100]
        print(f"      {content_preview}...")
    
    # Scenario 3: Code Patterns
    print("\n" + "-"*70)
    print("💻 Scenario 3: Reusable Code Patterns")
    print("-" * 70)
    print("User Question: 'How do I handle API failures?'")
    print("\nRAG retrieves applicable code patterns...")
    
    code_patterns = rag.retrieve_code_patterns("API retry logic", language="python", k=2)
    print(f"\n✅ Found {len(code_patterns)} code patterns:")
    for i, pattern in enumerate(code_patterns, 1):
        name = pattern['metadata'].get('name', 'N/A')
        print(f"\n   {i}. {name}")
        print(f"      Language: {pattern['metadata'].get('language', 'N/A')}")
        print(f"      Use cases: {pattern['content'].split('Use cases:')[0] if 'Use cases:' in pattern['content'] else 'Multiple'}")
    
    # Scenario 4: Error Resolution
    print("\n" + "-"*70)
    print("🔧 Scenario 4: Error Resolution")
    print("-" * 70)
    print("User Error: 'Getting 401 Unauthorized from API'")
    print("\nRAG retrieves similar errors and solutions...")
    
    error_solutions = rag.retrieve_error_solutions("401 Unauthorized", k=2)
    print(f"\n✅ Found {len(error_solutions)} similar errors:")
    for i, solution in enumerate(error_solutions, 1):
        error = solution['metadata'].get('error', 'N/A')
        print(f"\n   {i}. {error}")
        # Safely extract solution text
        try:
            if 'Solution:' in solution['content']:
                parts = solution['content'].split('Solution:')
                if len(parts) > 1:
                    lines = parts[1].split('\n')
                    solution_text = next((line.strip() for line in lines if line.strip()), 'See details')
                else:
                    solution_text = 'See details'
            else:
                solution_text = solution['content'][:80]
            print(f"      Solution: {solution_text[:80]}...")
        except:
            print(f"      Solution: See full details in knowledge base")
    
    # Scenario 5: Search Everything
    print("\n" + "-"*70)
    print("🔍 Scenario 5: Search Across All Knowledge")
    print("-" * 70)
    print("User Query: 'authentication'")
    print("\nRAG searches all collections...")
    
    all_results = rag.search_all("authentication", k=2)
    total_results = sum(len(docs) for docs in all_results.values())
    print(f"\n✅ Found {total_results} total results across all collections:")
    
    for collection, docs in all_results.items():
        if docs:
            print(f"\n   📁 {collection}: {len(docs)} results")
            for doc in docs[:1]:  # Show first result
                if 'title' in doc['metadata']:
                    print(f"      → {doc['metadata']['title']}")
                elif 'description' in doc['metadata']:
                    print(f"      → {doc['metadata']['description'][:60]}...")
                elif 'name' in doc['metadata']:
                    print(f"      → {doc['metadata']['name']}")
                elif 'error' in doc['metadata']:
                    print(f"      → {doc['metadata']['error'][:60]}...")
    
    # Benefits Summary
    print("\n" + "="*70)
    print("✨ RAG SYSTEM BENEFITS")
    print("="*70)
    print("""
✅ Context-Aware: AI uses relevant past knowledge
✅ Consistent: Follows team patterns and conventions
✅ Efficient: Reuses solutions instead of regenerating
✅ Learning: Gets smarter with every project
✅ Cost-Free: 100% local processing, no API costs
✅ Private: All data stays on your machine
✅ Fast: Semantic search in milliseconds
    """)
    
    # Next Steps
    print("="*70)
    print("🚀 NEXT STEPS")
    print("="*70)
    print("""
1. Try queries yourself:
   python -c "from src.core.rag_system import RAGSystem; rag = RAGSystem(); ..."

2. Add your team's knowledge:
   rag.store_task("Your task", "How you solved it", {...})

3. Phase 2: Add Reasoning Agent for full automation
   - Autonomous decision-making
   - One-prompt task execution
   - Continuous learning

4. Read documentation:
   docs/RAG_SYSTEM.md
    """)
    
    print("="*70)
    print("✅ RAG SYSTEM DEMO COMPLETE!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo_rag_system()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

