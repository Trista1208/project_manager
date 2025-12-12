# 📚 RAG System Documentation

## Retrieval-Augmented Generation for DevOps Automation

The RAG (Retrieval-Augmented Generation) system enables your AI agents to learn from past projects and provide context-aware assistance.

---

## 🎯 What is RAG?

**RAG combines:**
- **Vector Database** (ChromaDB) - Stores knowledge as searchable embeddings
- **Semantic Search** - Finds relevant information based on meaning, not keywords  
- **Context Enhancement** - Enriches AI prompts with relevant past knowledge

**Benefits:**
- ✅ **Learn from Experience** - AI gets smarter over time
- ✅ **Context-Aware** - Retrieves relevant past solutions
- ✅ **Cost Reduction** - Reuses past knowledge instead of re-analyzing
- ✅ **Consistency** - Follows team conventions and best practices
- ✅ **Knowledge Preservation** - Captures team expertise

---

## 🏗️ Architecture

```
User Query: "How do I implement user login?"
       │
       ▼
┌─────────────────────────────────────────┐
│  RAG System                             │
│  1. Generate query embedding            │
│  2. Search vector database              │
│  3. Return relevant context             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Similar Past Tasks Found:              │
│  • "Implement OAuth2 authentication"    │
│  • "Add JWT token validation"           │
│  • "Password reset functionality"       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  AI Agent (with context)                │
│  Uses retrieved knowledge to generate   │
│  more accurate and consistent response  │
└─────────────────────────────────────────┘
```

---

## 📦 What's Stored

### 1. **Tasks** (`tasks` collection)
Past project tasks and their outcomes:
- Task description
- How it was completed
- Duration and complexity
- Technologies used
- Success/failure learnings

### 2. **Best Practices** (`best_practices` collection)
DevOps conventions and standards:
- Security practices
- Testing guidelines
- API design patterns
- Database best practices
- CI/CD workflows

### 3. **Code Patterns** (`code_patterns` collection)
Reusable code templates:
- API retry logic
- Error handling patterns
- Configuration loaders
- Common utilities

### 4. **Error Resolutions** (`errors` collection)
Past errors and solutions:
- Error messages
- Root causes
- Solutions that worked
- Prevention strategies

### 5. **Documentation** (`documentation` collection)
Project documentation and guides

---

## 🚀 Quick Start

### Initialize RAG System

```python
from src.core.rag_system import RAGSystem
from src.core.rag_knowledge_base import populate_initial_knowledge

# Create RAG system
rag = RAGSystem(persist_directory="./rag_data")

# Populate with initial DevOps knowledge
populate_initial_knowledge(rag)

# Check statistics
stats = rag.get_statistics()
print(f"Total knowledge: {stats['total_documents']} documents")
```

### Store Knowledge

```python
# Store a completed task
rag.store_task(
    "Implement CI/CD pipeline",
    "Successfully set up GitHub Actions with automated testing",
    metadata={
        "project": "myproject",
        "duration_hours": 4,
        "complexity": "medium"
    }
)

# Store a best practice
rag.store_best_practice(
    "Use Environment Variables",
    "Never hardcode secrets. Always use env vars and .env files.",
    category="security"
)

# Store a code pattern
rag.store_code_pattern(
    "API Retry Logic",
    "def retry_api(func, max_retries=3): ...",
    "Use for resilient API calls",
    language="python",
    use_cases=["HTTP requests", "External APIs"]
)

# Store error resolution
rag.store_error_resolution(
    "Connection timeout",
    "Increased timeout and added retry with exponential backoff",
    context="Occurs when API is slow or under load"
)
```

### Retrieve Context

```python
# Find similar past tasks
similar = rag.retrieve_similar_tasks("add user login", k=3)
for task in similar:
    print(f"Similar: {task['metadata']['description']}")

# Get best practices
practices = rag.retrieve_best_practices("API security", k=5)
for practice in practices:
    print(f"Practice: {practice['metadata']['title']}")

# Find code patterns
patterns = rag.retrieve_code_patterns("handle API errors", k=3)
for pattern in patterns:
    print(f"Pattern: {pattern['metadata']['name']}")

# Get error solutions
solutions = rag.retrieve_error_solutions("timeout error", k=3)
for solution in solutions:
    print(f"Solution: {solution['metadata']['error']}")

# Search all collections
all_results = rag.search_all("authentication", k=3)
for collection, docs in all_results.items():
    print(f"{collection}: {len(docs)} results")
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Activate environment
source test_venv/bin/activate

# Run RAG tests
python tests/test_rag_system.py
```

**Tests include:**
- ✅ System initialization
- ✅ Storage and retrieval (all types)
- ✅ Search across collections
- ✅ Knowledge base population
- ✅ Real-world query examples

---

## 💡 Use Cases

### 1. **Context-Aware Task Breakdown**

```python
# User request: "Implement user authentication"

# Retrieve similar past tasks
past_tasks = rag.retrieve_similar_tasks(
    "implement user authentication", 
    k=3
)

# Retrieve security best practices
security = rag.retrieve_best_practices(
    "authentication security", 
    k=5
)

# Build enriched prompt
prompt = f"""
Break down this task: "Implement user authentication"

Similar past tasks:
{past_tasks}

Relevant best practices:
{security}

Generate tasks following these patterns.
"""

# AI generates better, more consistent tasks
tasks = llm.generate(prompt)
```

### 2. **Error Resolution Assistant**

```python
# User encounters error: "401 Unauthorized"

# Find similar past errors
solutions = rag.retrieve_error_solutions(
    "401 Unauthorized API error", 
    k=3
)

# Show user how team solved it before
for solution in solutions:
    print(f"Solution: {solution['content']}")
```

### 3. **Code Pattern Suggestions**

```python
# User asks: "How do I handle API timeouts?"

# Retrieve relevant code patterns
patterns = rag.retrieve_code_patterns(
    "API timeout retry", 
    language="python", 
    k=2
)

# Show reusable code
for pattern in patterns:
    print(f"Pattern: {pattern['metadata']['name']}")
    print(pattern['content'])
```

### 4. **Continuous Learning**

```python
# After every successful task
rag.store_task(
    task_description="Implemented OAuth2 login",
    outcome="Success - completed in 6 hours",
    metadata={
        "complexity": "medium",
        "duration_hours": 6,
        "technologies": "OAuth2, JWT, Flask"
    }
)

# System gets smarter over time!
```

---

## 📊 Knowledge Base Statistics

View current knowledge:

```python
stats = rag.get_statistics()
print(f"""
Total Documents: {stats['total_documents']}
- Tasks: {stats['tasks']}
- Best Practices: {stats['best_practices']}
- Code Patterns: {stats['code_patterns']}
- Errors: {stats['errors']}
- Documentation: {stats['documentation']}
""")
```

---

## 🔧 Configuration

### Storage Location

```python
# Default: ./rag_data
rag = RAGSystem(persist_directory="./rag_data")

# Custom location
rag = RAGSystem(persist_directory="/path/to/knowledge")
```

### Embedding Model

The system uses `all-MiniLM-L6-v2` by default:
- ✅ **Free** - Runs locally, no API costs
- ✅ **Fast** - 120M parameters, very efficient
- ✅ **Accurate** - Good quality embeddings
- ✅ **Small** - ~80MB download

To use a different model:

```python
# In rag_system.py, modify:
self.embedding_model = SentenceTransformer('your-model-name')
```

### Search Results

Control number of results:

```python
# Get top 5 results
results = rag.retrieve_context(query, k=5)

# Get more results
results = rag.retrieve_context(query, k=10)
```

---

## 🎓 Advanced Usage

### Export Knowledge

```python
# Export to JSON
rag.export_knowledge("knowledge_backup.json")
```

### Reset System

```python
# Clear all data (careful!)
rag.reset()
```

### Filtered Search

```python
# Search with metadata filters
results = rag.retrieve_best_practices(
    "API design",
    category="security",  # Only security practices
    k=5
)

results = rag.retrieve_code_patterns(
    "error handling",
    language="python",  # Only Python patterns
    k=3
)
```

---

## 💰 Cost

**RAG system is 100% FREE!**

- ✅ **ChromaDB** - Free, open-source vector database
- ✅ **Sentence Transformers** - Free, runs locally
- ✅ **No API calls** - All processing is local
- ✅ **Storage** - Just disk space (minimal)

**Typical storage:**
- 100 documents ≈ 1MB
- 1,000 documents ≈ 10MB
- 10,000 documents ≈ 100MB

---

## 🔒 Privacy & Security

**Your data stays local:**
- ✅ No data sent to external services
- ✅ All embeddings generated locally
- ✅ Vector database stored on your machine
- ✅ Full control over your knowledge

---

## 🚀 Next Steps: Phase 2

**Phase 2 will add:**
- Reasoning Agent (uses DeepSeek R1)
- Autonomous Orchestrator
- Fully automated workflows
- One-prompt automation

See parent documentation for Phase 2 details.

---

## 📚 References

- **ChromaDB**: https://www.trychroma.com/
- **Sentence Transformers**: https://www.sbert.net/
- **all-MiniLM-L6-v2**: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

---

## ✅ Summary

The RAG system gives your AI agents:
- 📚 **Memory** - Learn from past projects
- 🎯 **Context** - Retrieve relevant knowledge
- 🚀 **Consistency** - Follow team standards
- 💰 **Efficiency** - Reuse instead of regenerate
- 🔒 **Privacy** - Everything stays local

**Your AI agents are now context-aware and continuously learning!** 🎉
