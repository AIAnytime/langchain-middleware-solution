# LangChain v1.0 Middleware: Presentation Outline

## Presentation Flow for AI Engineers

### Duration: 15-20 minutes

---

## Part 1: The Problem (3 minutes)

### Slide 1: Pre-v1.0 Reality
"Anyone who built AI agents has faced these challenges..."

**Show code example from `project.md`:**
```python
def custom_agent_loop(user_input, tools, llm):
    messages = [{"role": "user", "content": user_input}]
    
    for iteration in range(10):
        if len(messages) > 20:
            messages = summarize_history(messages)  # Manual
        
        available_tools = select_tools(messages, tools)  # Manual
        system_prompt = generate_prompt(iteration)  # Manual
        
        if token_count > budget:  # Manual
            raise Exception("Budget exceeded")
        
        response = llm.invoke(messages, tools=available_tools)
```

**Problems:**
- Everything is manual
- Tightly coupled
- Hard to test
- Non-reusable
- Production nightmare

### Slide 2: The Core Issue
"Context Management is Information Management"

- Too much info → Model confusion
- Too little info → Task incomplete
- Security concerns → PII leakage
- Cost concerns → Budget overruns

**Before v1.0**: No systematic solution

---

## Part 2: The Solution (4 minutes)

### Slide 3: Enter Middleware
"Borrowed from FastAPI, adapted for AI agents"

**Execution Flow:**
```
User Input → Middleware Stack → AI Model → Middleware Stack → Response
```

**Familiar Pattern:**
- FastAPI: Request → Middleware → Handler → Response
- LangChain: Input → Middleware → Model → Response

Same concept, different domain.

### Slide 4: Intervention Points

**Four hooks:**
1. `before_model`: Pre-process inputs
2. `wrap_model_call`: Modify model parameters
3. `wrap_tool_call`: Control tool access
4. `after_model`: Post-process outputs

**Live Demo**: Run Demo 1 (Logging Middleware)
- Show complete visibility
- Explain before/after hooks

---

## Part 3: Core Middleware Types (5 minutes)

### Slide 5: Security - PII Protection

**Problem**: Sensitive data reaching the model

**Solution**: SecurityFilterMiddleware

**Live Demo**: Run Demo 4
- Input: "My email is john@example.com"
- Output: "My email is [REDACTED_EMAIL]"

**Production Use**: GDPR/HIPAA compliance

### Slide 6: Cost Control - Token Budget

**Problem**: Runaway API costs

**Solution**: TokenBudgetMiddleware

**Live Demo**: Run Demo 2
- Show token tracking
- Demonstrate budget enforcement
- Explain fail-fast protection

**Production Use**: Predictable costs

### Slide 7: Context Management - Summarization

**Problem**: Long conversations exceed context window

**Solution**: ContextSummarizationMiddleware

**Live Demo**: Run Demo 3
- Show 11 messages → 6 messages
- Explain how summary preserves key info
- Discuss token optimization

**Production Use**: Long-running conversations

---

## Part 4: Advanced Patterns (4 minutes)

### Slide 8: Personalization

**Problem**: One-size-fits-all responses

**Solution**: ExpertiseBasedMiddleware

**Live Demo**: Run Demo 5
- Same question, different expertise levels
- Beginner: Simple language, examples
- Expert: Technical depth, jargon

**Show Code:**
```python
context = UserContext(expertise_level="expert")
middleware = ExpertiseBasedMiddleware(context)
```

**Production Use**: User segmentation

### Slide 9: The Power - Middleware Stacks

**Concept**: Composability

**Live Demo**: Run Demo 6

**Show Stack:**
```python
middleware_stack = [
    LoggingMiddleware(),           # Track everything
    SecurityFilterMiddleware(),     # Protect PII
    TokenBudgetMiddleware(),       # Control costs
    ExpertiseBasedMiddleware(),    # Personalize
]
```

**Key Point**: Each middleware is independent but works together

---

## Part 5: Architecture Comparison (3 minutes)

### Slide 10: Old vs New

**Live Demo**: Run Demo 7

**Old Way:**
- Manual context management
- Tightly coupled logic
- Hard to test
- Non-reusable

**New Way:**
- Separation of concerns
- Independent modules
- Easy to test
- Highly reusable

**Architectural Shift:**
- From ad-hoc → systematic
- From code → engineering
- From custom → patterns

### Slide 11: Production Benefits

**Real-world advantages:**

1. **Reusability**: Write once, use everywhere
2. **Testability**: Test each middleware independently
3. **Maintainability**: Clear responsibilities
4. **Composability**: Mix and match
5. **Standards**: Community-driven patterns

**Cost Reduction:**
- Less dev time
- Fewer bugs
- Easier onboarding
- Faster iteration

---

## Part 6: Wrap-up (2 minutes)

### Slide 12: Key Takeaways

1. **Middleware = Systematic Context Control**
   - No more manual management
   
2. **Composable Architecture**
   - Build complex behavior from simple parts
   
3. **Production-Ready**
   - Security, costs, monitoring built-in
   
4. **Standard Patterns**
   - Community best practices
   
5. **Testable & Maintainable**
   - Software engineering principles

### Slide 13: Getting Started

**Try it yourself:**
```bash
git clone [repo]
cd langchain-middleware-solution
uv venv && source .venv/bin/activate
uv run python main.py
```

**Resources:**
- Full README with 7 demos
- Test suite included
- Custom middleware examples
- Production patterns

**Next Steps:**
1. Run all 7 demos
2. Study middleware implementations
3. Create custom middleware
4. Apply to your agents

---

## Q&A Preparation

### Expected Questions

**Q: Does this work with other LLMs besides OpenAI?**
A: Yes, any LangChain-compatible LLM. Demo includes Gemini support.

**Q: Can I create my own middleware?**
A: Absolutely. Extend base pattern with `before_model` and `after_model` methods.

**Q: What's the performance overhead?**
A: Minimal. Middleware is lightweight. Caching can actually improve performance.

**Q: How do I test middleware?**
A: Each middleware is independent. Unit test each one separately. See `test_demo.py`.

**Q: Is this production-ready?**
A: The pattern is. These are demonstration implementations. Add error handling and monitoring for production.

**Q: Does order matter in the stack?**
A: Yes. Security and logging typically go first. Order affects processing sequence.

---

## Demo Execution Tips

### Before Presentation
1. Test all demos work
2. Have API keys configured
3. Practice demo flow
4. Note timing for each demo

### During Presentation
1. Show code first, then run
2. Explain what you expect, then verify
3. Highlight middleware console output
4. Point out architectural patterns

### Demos to Prioritize
- **Demo 1** (Logging): Shows basic flow
- **Demo 4** (Security): Impressive visual
- **Demo 6** (Stack): Shows power
- **Demo 7** (Comparison): Architecture shift

### Time Management
- 2 min per demo maximum
- Focus on concepts, not output
- Skip Demo 2 or 3 if time-constrained
- Always show Demo 6 (stack)

---

## Backup Slides (If Time)

### Technical Deep-Dive: Message Flow

```python
# Input
messages = [{"role": "user", "content": "Hello"}]

# After Logging
# [LOG] Processing message...

# After Security  
messages = [{"role": "user", "content": "Hello"}]  # No PII to filter

# After Budget
# [BUDGET] Tokens: 5/1000

# After Expertise
messages = [
    {"role": "system", "content": "Expert mode..."},
    {"role": "user", "content": "Hello"}
]

# Model Call
response = model.invoke(messages)

# After Model (reverse order)
# All validation passed
```

### Custom Middleware Example

```python
class CustomMiddleware:
    def before_model(self, messages: list) -> list:
        # Your preprocessing logic
        return modified_messages
    
    def after_model(self, response: Any) -> Any:
        # Your postprocessing logic
        return modified_response
```

---

## Presentation Success Metrics

**Audience should leave understanding:**
1. What middleware is
2. Why it matters
3. How to use it
4. Where to apply it

**Audience should be able to:**
1. Explain the middleware pattern
2. Identify use cases
3. Create basic middleware
4. Compose middleware stacks

---

## Follow-up Resources

**Share with audience:**
- GitHub repository link
- README with full documentation
- QUICK_START guide
- Test suite for practice

**Additional Learning:**
- LangChain v1.0 docs
- FastAPI middleware (pattern origin)
- Production AI agent patterns
- Context engineering principles

---

**Presentation prepared for AI Engineers and Developers**
**Focus: Practical understanding + hands-on demonstration**
**Style: Professional, technical, example-driven**
