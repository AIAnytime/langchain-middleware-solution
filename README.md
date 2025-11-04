# LangChain v1.0 Middleware Solution

A comprehensive demonstration of the middleware architecture introduced in LangChain v1.0 for systematic AI agent context control.

## Overview

This project demonstrates how middleware transforms ad-hoc agent context management into a systematic, production-ready engineering practice. The middleware pattern, borrowed from web frameworks like FastAPI, provides standardized intervention points throughout the agent execution lifecycle.

## Key Concepts

### What is Middleware?

Middleware acts as an information coordination layer that processes data before it reaches the AI model and after it returns. It enables:

- Standardized input formatting
- Context injection and management
- Security filtering
- Cost control
- Tool access permissions
- Runtime monitoring

### Execution Flow

```
User Input → Middleware Stack → AI Model → Middleware Stack → Response
```

Each middleware in the stack can intercept and modify the flow at specific points:
- `before_model`: Pre-process inputs
- `wrap_model_call`: Modify model parameters
- `wrap_tool_call`: Control tool access
- `after_model`: Post-process outputs

![Graphviz Diagram](./graphviz%20%2815%29.svg)

## Project Structure

```
langchain-middleware-solution/
├── .env                          # API keys (OpenAI, Gemini)
├── streamlit_app.py              # Streamlit web interface (recommended)
├── streamlit_pages.py            # Streamlit page components
├── main.py                       # CLI entry point
├── demo_examples.py              # 7 comprehensive demos
├── middleware/
│   ├── __init__.py
│   └── custom_middleware.py      # Custom middleware implementations
├── pyproject.toml                # Project dependencies
└── README.md                     # This file
```

## Setup

### Prerequisites

- Python 3.11+
- uv package manager
- OpenAI API key or Google Gemini API key

### Installation

1. Clone or navigate to this directory:
```bash
cd langchain-middleware-solution
```

2. Create virtual environment:
```bash
uv venv
```

3. Activate virtual environment:
```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

4. Install dependencies:
```bash
uv add langchain langchain-openai langchain-google-genai python-dotenv
```

5. Configure API keys in `.env`:
```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Running the Demo

### Streamlit Web Interface (Recommended)

```bash
uv run streamlit run streamlit_app.py
```

This launches an interactive web interface at `http://localhost:8501` with:
- Visual demonstrations of all middleware
- Interactive configuration options
- Real-time testing playground
- Side-by-side comparisons

### CLI Interface

```bash
python main.py
```

This launches an interactive CLI menu with 7 demonstration scenarios.

### Demo Scenarios

1. **Logging Middleware**
   - Tracks all agent interactions for debugging
   - Provides complete visibility into decision-making
   - Essential for production monitoring

2. **Token Budget Control**
   - Enforces token limits to prevent cost overruns
   - Tracks cumulative usage across requests
   - Automatic budget enforcement

3. **Context Summarization**
   - Automatically manages long conversation histories
   - Prevents context window overflow
   - Maintains key information while condensing

4. **Security Filtering**
   - Redacts PII (emails, phone numbers, API keys)
   - GDPR/HIPAA compliance support
   - Transparent filtering without model changes

5. **Expertise-Based Personalization**
   - Adjusts responses based on user skill level
   - Experts get advanced details, beginners get guidance
   - Dynamic behavior modification

6. **Middleware Stack**
   - Combines multiple middleware for production use
   - Shows composability and layered controls
   - Real-world production pattern

7. **Old vs New Architecture**
   - Compares manual approach with middleware pattern
   - Highlights architectural improvements
   - Demonstrates systematic engineering benefits

## Middleware Implementations

### Built-in Demonstrations

#### LoggingMiddleware
```python
logging_mw = LoggingMiddleware(verbose=True)
# Logs all inputs, outputs, and timestamps
```

#### TokenBudgetMiddleware
```python
budget_mw = TokenBudgetMiddleware(max_tokens=10000, max_requests=50)
# Enforces cost controls automatically
```

#### ContextSummarizationMiddleware
```python
summarization_mw = ContextSummarizationMiddleware(max_messages=10)
# Auto-summarizes when conversation gets too long
```

#### SecurityFilterMiddleware
```python
security_mw = SecurityFilterMiddleware()
# Redacts emails, phone numbers, API keys
```

#### ExpertiseBasedMiddleware
```python
context = UserContext(user_id="user_001", expertise_level="expert")
expertise_mw = ExpertiseBasedMiddleware(context)
# Adjusts behavior based on user expertise
```

### Creating Custom Middleware

Extend the base middleware pattern:

```python
class CustomMiddleware:
    def before_model(self, messages: list) -> list:
        # Process messages before model call
        return modified_messages
    
    def after_model(self, response: Any) -> Any:
        # Process response after model call
        return modified_response
```

## Architecture Benefits

### Old Way (Pre v1.0)
- Manual context management
- Tightly coupled logic
- Hard to test
- Non-reusable
- Poor maintainability

### New Way (v1.0 Middleware)
- Separation of concerns
- Independently testable
- Highly reusable
- Easy to maintain
- Composable like building blocks
- Community-driven patterns

## Production Patterns

Typical production middleware stack:

```python
middleware_stack = [
    LoggingMiddleware(),                      # Track everything
    SecurityFilterMiddleware(),               # Protect PII
    TokenBudgetMiddleware(max_tokens=50000),  # Cost control
    ContextSummarizationMiddleware(),         # Manage context
    ExpertiseBasedMiddleware(context),        # Personalize
    CachingMiddleware(),                      # Performance
]
```

## Use Cases

### For AI Engineers
- Understand middleware architecture patterns
- Learn systematic context management
- See production-ready implementations
- Compare old vs new approaches

### For Production Systems
- Cost control and budget enforcement
- Privacy and compliance (PII protection)
- Performance optimization (caching)
- User personalization
- Monitoring and debugging

## Technical Details

### Supported Models
- OpenAI GPT-3.5/GPT-4
- Google Gemini 1.5 Flash
- Any LangChain-compatible LLM

### Middleware Execution Order
Middleware executes in stack order:
1. `before_model`: Forward through stack (first to last)
2. Model invocation
3. `after_model`: Backward through stack (last to first)

### Context Management
The `UserContext` dataclass tracks user state across middleware:
```python
@dataclass
class UserContext:
    user_id: str = "unknown"
    expertise_level: str = "beginner"
    session_start: str = ""
    token_count: int = 0
    request_count: int = 0
```

## Best Practices

1. **Single Responsibility**: Each middleware should handle one concern
2. **Order Matters**: Security and logging should come first
3. **Error Handling**: Middleware should fail gracefully
4. **Testing**: Test each middleware independently
5. **Documentation**: Document middleware behavior clearly
6. **Performance**: Keep middleware lightweight

## Troubleshooting

### API Key Errors
Ensure `.env` file contains valid API keys:
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

### Import Errors
Activate virtual environment:
```bash
source .venv/bin/activate
```

### Token Limit Errors
Adjust budget in middleware:
```python
TokenBudgetMiddleware(max_tokens=20000)
```

**Built with LangChain v1.0 | Demonstrating Middleware Architecture | For AI Engineers**
