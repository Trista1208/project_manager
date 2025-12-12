#!/usr/bin/env python3
"""
Populate RAG System with Initial Knowledge
Run this script once to populate the RAG database with code patterns and best practices.
"""
from rag_system import RAGSystem
from knowledge_base import CODE_PATTERNS, BEST_PRACTICES, EXAMPLE_PROJECTS


def populate_rag_database():
    """Populate RAG system with initial knowledge."""
    
    print("=" * 70)
    print("🚀 POPULATING RAG KNOWLEDGE BASE")
    print("=" * 70)
    print()
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Check if already populated
    stats = rag.get_stats()
    if stats['total'] > 0:
        print(f"⚠️  Database already contains {stats['total']} documents.")
        response = input("Do you want to clear and repopulate? (yes/no): ")
        if response.lower() == 'yes':
            rag.clear_all()
            print("✅ Database cleared!")
        else:
            print("❌ Aborting. Use existing data.")
            return
    
    print()
    print("📝 Populating knowledge base...")
    print()
    
    # Populate code patterns
    print("💻 Adding Code Patterns...")
    for pattern in CODE_PATTERNS:
        rag.store_code_pattern(
            pattern_name=pattern['name'],
            pattern_type=pattern['type'],
            code=pattern['code'],
            description=pattern['description'],
            use_cases=pattern['use_cases']
        )
    print(f"✅ Added {len(CODE_PATTERNS)} code patterns")
    print()
    
    # Populate best practices
    print("📖 Adding Best Practices...")
    for practice in BEST_PRACTICES:
        rag.store_best_practice(
            title=practice['title'],
            category=practice['category'],
            content=practice['content'],
            tags=practice['tags']
        )
    print(f"✅ Added {len(BEST_PRACTICES)} best practices")
    print()
    
    # Populate example projects
    print("📂 Adding Example Projects...")
    for project in EXAMPLE_PROJECTS:
        rag.store_project(
            project_description=project['description'],
            tasks=project['tasks'],
            outcome=project['outcome'],
            metadata=project.get('metadata', {})
        )
    print(f"✅ Added {len(EXAMPLE_PROJECTS)} example projects")
    print()
    
    # Show final stats
    print("=" * 70)
    print("✅ RAG KNOWLEDGE BASE POPULATED SUCCESSFULLY!")
    print("=" * 70)
    
    stats = rag.get_stats()
    print()
    print("📊 Final Statistics:")
    print(f"   • Code Patterns: {stats['code_patterns']}")
    print(f"   • Best Practices: {stats['best_practices']}")
    print(f"   • Past Projects: {stats['projects']}")
    print(f"   • Total Documents: {stats['total']}")
    print()
    
    print("🎉 Your RAG system is ready to use!")
    print()


if __name__ == "__main__":
    populate_rag_database()

