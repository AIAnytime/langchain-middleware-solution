# Quick Start Guide

## Setup in 3 Steps

### 1. Environment Setup
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Dependencies already installed via uv add
```

### 2. Configure API Keys
Ensure `.env` contains:
```env
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### 3. Run Demo

**Option A: Streamlit Web Interface (Recommended)**
```bash
uv run streamlit run streamlit_app.py
```
Opens at `http://localhost:8501` with visual, interactive demos.

**Option B: CLI Interface**
```bash
python main.py
```
Text-based interactive menu.

## Demo Menu

When you run the demo, you'll see an interactive menu:

```
Available Demos:
  1. Logging Middleware
  2. Token Budget Control
  3. Context Summarization
  4. Security Filtering
  5. Expertise-Based Personalization
  6. Middleware Stack
  7. Old vs New Architecture
  8. Run All Demos
  0. Exit
```

## Recommended Demo Sequence

For AI engineers new to middleware concepts:

1. **Demo 1**: Understand basic middleware flow and logging
2. **Demo 4**: See security filtering in action
3. **Demo 2**: Learn cost control mechanisms
4. **Demo 5**: Explore dynamic personalization
5. **Demo 6**: See production stack composition
6. **Demo 7**: Compare old vs new architecture

## What Each Demo Shows

### Demo 1: Logging Middleware
**What**: Tracks all inputs/outputs with timestamps  
**Why**: Essential for debugging and monitoring  
**Output**: Detailed logs of agent execution flow

### Demo 2: Token Budget Control
**What**: Enforces token limits and request counts  
**Why**: Prevents runaway API costs  
**Output**: Budget tracking and automatic enforcement

### Demo 3: Context Summarization
**What**: Auto-condenses long conversations  
**Why**: Prevents context window overflow  
**Output**: Before/after message counts with summarization

### Demo 4: Security Filtering
**What**: Redacts PII (emails, phones, API keys)  
**Why**: GDPR/HIPAA compliance  
**Output**: Original vs filtered messages

### Demo 5: Expertise-Based Personalization
**What**: Adjusts responses for beginner vs expert users  
**Why**: Personalized user experience  
**Output**: Different response styles for different users

### Demo 6: Middleware Stack
**What**: Combines multiple middleware (logging + security + budget + personalization)  
**Why**: Real-world production pattern  
**Output**: Layered processing with all controls active

### Demo 7: Old vs New Architecture
**What**: Compares manual code vs middleware approach  
**Why**: Shows architectural evolution  
**Output**: Code comparison and benefits explanation

## Expected Behavior

Each demo will:
1. Print a header explaining the use case
2. Show middleware processing in action
3. Make an actual API call to OpenAI/Gemini
4. Display the final response
5. Summarize key insights

## Troubleshooting

### "No module named 'middleware'"
```bash
# Make sure you're in the project directory
pwd
# Should show: .../langchain-middleware-solution
```

### "Invalid API key"
```bash
# Check your .env file
cat .env
# Keys should start with:
# OPENAI_API_KEY=sk-...
# GEMINI_API_KEY=AIza...
```

### "Import error: langchain"
```bash
# Reinstall dependencies
uv add langchain langchain-openai langchain-google-genai python-dotenv
```

## Key Concepts to Observe

While running demos, watch for:

1. **Middleware Execution Order**
   - `before_model` runs first to last
   - `after_model` runs last to first

2. **Context Modification**
   - Messages are transformed at each layer
   - Original input vs final input to model

3. **Composability**
   - Multiple middleware work together seamlessly
   - No tight coupling between layers

4. **Separation of Concerns**
   - Each middleware has one clear responsibility
   - Easy to add/remove without breaking others

## Next Steps

After running demos:

1. **Read the Code**: Check `middleware/custom_middleware.py` to see implementations
2. **Modify Parameters**: Adjust token budgets, message limits, etc.
3. **Create Custom Middleware**: Extend the base pattern for your use case
4. **Combine Differently**: Create your own middleware stacks

## Quick Reference: Middleware Classes

```python
# Logging
LoggingMiddleware(verbose=True)

# Cost Control
TokenBudgetMiddleware(max_tokens=10000, max_requests=50)

# Context Management
ContextSummarizationMiddleware(max_messages=10)

# Security
SecurityFilterMiddleware()

# Personalization
context = UserContext(expertise_level="expert")
ExpertiseBasedMiddleware(context)

# Performance
CachingMiddleware()
```

## Production Checklist

When building production agents:

- [ ] Logging middleware for monitoring
- [ ] Security filter for PII protection
- [ ] Token budget for cost control
- [ ] Context summarization for long conversations
- [ ] Error handling middleware
- [ ] Caching for performance
- [ ] User personalization if needed
- [ ] Tool access control if using external tools

## Resources

- Full README: `README.md`
- Original article: `project.md`
- Middleware code: `middleware/custom_middleware.py`
- Demo examples: `demo_examples.py`

---

**Ready to start? Run:** `python main.py`
