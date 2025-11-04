"""
LangChain v1.0 Middleware Demo Examples

Demonstrates various middleware patterns for AI agent context control.
Each example showcases a specific middleware use case from the article.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from middleware import (
    LoggingMiddleware,
    TokenBudgetMiddleware,
    ContextSummarizationMiddleware,
    SecurityFilterMiddleware,
    ExpertiseBasedMiddleware,
    CachingMiddleware,
    UserContext,
)

# Load environment variables
load_dotenv()


class MiddlewareDemo:
    """Base class for running middleware demonstrations"""
    
    def __init__(self, use_openai: bool = True):
        """
        Initialize the demo with either OpenAI or Gemini
        
        Args:
            use_openai: If True, use OpenAI; otherwise use Gemini
        """
        if use_openai:
            self.model = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            print(f"\nUsing Model: OpenAI GPT-3.5-Turbo")
        else:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.7,
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
            print(f"\nUsing Model: Google Gemini 1.5 Flash")
    
    def simulate_call_with_middleware(self, messages, middleware_list):
        """
        Simulate an agent call passing through middleware stack
        
        Args:
            messages: List of message dictionaries
            middleware_list: List of middleware instances to apply
        """
        # Convert to proper message format
        formatted_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                formatted_messages.append(SystemMessage(content=msg['content']))
            elif msg['role'] == 'user':
                formatted_messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                formatted_messages.append(AIMessage(content=msg['content']))
        
        # Apply before_model middleware in order
        processed_messages = messages.copy()
        for middleware in middleware_list:
            if hasattr(middleware, 'before_model'):
                result = middleware.before_model(processed_messages)
                # Handle tuple return (for caching)
                if isinstance(result, tuple):
                    processed_messages, cache_info = result
                else:
                    processed_messages = result
        
        # Make the actual model call
        try:
            response = self.model.invoke(formatted_messages)
            
            # Apply after_model middleware in reverse order
            for middleware in reversed(middleware_list):
                if hasattr(middleware, 'after_model'):
                    response = middleware.after_model(response)
            
            return response
        except Exception as e:
            print(f"\n[ERROR] Model call failed: {str(e)}")
            return None


def demo_1_logging_middleware():
    """
    Demo 1: Logging Middleware
    
    Shows how to track all agent interactions for debugging and monitoring.
    Essential for production environments to understand agent behavior.
    """
    print("\n" + "="*80)
    print("DEMO 1: LOGGING MIDDLEWARE")
    print("="*80)
    print("\nUse Case: Track all agent interactions for debugging and audit trails")
    print("Benefit: Complete visibility into agent decision-making process\n")
    
    demo = MiddlewareDemo(use_openai=True)
    logging_mw = LoggingMiddleware(verbose=True)
    
    messages = [
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {'role': 'user', 'content': 'What is the capital of France?'}
    ]
    
    response = demo.simulate_call_with_middleware(messages, [logging_mw])
    
    if response:
        print(f"\n[FINAL RESPONSE] {response.content}\n")
    
    print("\nKey Insight: Logging middleware provides transparency without changing agent behavior")


def demo_2_token_budget():
    """
    Demo 2: Token Budget Middleware
    
    Demonstrates cost control by enforcing token limits.
    Prevents runaway API costs in production.
    """
    print("\n" + "="*80)
    print("DEMO 2: TOKEN BUDGET MIDDLEWARE")
    print("="*80)
    print("\nUse Case: Prevent excessive API costs by enforcing token limits")
    print("Benefit: Predictable costs and protection against budget overruns\n")
    
    demo = MiddlewareDemo(use_openai=True)
    
    # Set a low limit to demonstrate budget enforcement
    budget_mw = TokenBudgetMiddleware(max_tokens=500, max_requests=3)
    
    messages = [
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {'role': 'user', 'content': 'Explain quantum computing in simple terms.'}
    ]
    
    # First call - should succeed
    print("\n--- Request 1 (within budget) ---")
    response1 = demo.simulate_call_with_middleware(messages, [budget_mw])
    if response1:
        print(f"\n[RESPONSE] {response1.content[:100]}...")
    
    # Second call - might succeed
    print("\n--- Request 2 (approaching limit) ---")
    messages2 = [
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {'role': 'user', 'content': 'What is machine learning?'}
    ]
    response2 = demo.simulate_call_with_middleware(messages2, [budget_mw])
    if response2:
        print(f"\n[RESPONSE] {response2.content[:100]}...")
    
    print("\nKey Insight: Token budget middleware prevents cost overruns automatically")


def demo_3_context_summarization():
    """
    Demo 3: Context Summarization Middleware
    
    Shows automatic conversation history management.
    Critical for long-running conversations to prevent context window overflow.
    """
    print("\n" + "="*80)
    print("DEMO 3: CONTEXT SUMMARIZATION MIDDLEWARE")
    print("="*80)
    print("\nUse Case: Manage long conversation histories by automatic summarization")
    print("Benefit: Maintain context without hitting token limits\n")
    
    demo = MiddlewareDemo(use_openai=True)
    summarization_mw = ContextSummarizationMiddleware(max_messages=5)
    
    # Simulate a long conversation
    messages = [
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {'role': 'user', 'content': 'Tell me about Python'},
        {'role': 'assistant', 'content': 'Python is a programming language...'},
        {'role': 'user', 'content': 'What about JavaScript?'},
        {'role': 'assistant', 'content': 'JavaScript is used for web development...'},
        {'role': 'user', 'content': 'Compare them'},
        {'role': 'assistant', 'content': 'Python is better for data science...'},
        {'role': 'user', 'content': 'What about Go?'},
        {'role': 'assistant', 'content': 'Go is great for concurrent systems...'},
        {'role': 'user', 'content': 'Which should I learn first?'},
    ]
    
    print(f"\nOriginal conversation: {len(messages)} messages")
    response = demo.simulate_call_with_middleware(messages, [summarization_mw])
    
    if response:
        print(f"\n[RESPONSE] {response.content[:150]}...")
    
    print("\nKey Insight: Summarization maintains conversation flow while preventing context overflow")


def demo_4_security_filter():
    """
    Demo 4: Security Filter Middleware
    
    Demonstrates PII protection by redacting sensitive information.
    Essential for compliance and privacy in production systems.
    """
    print("\n" + "="*80)
    print("DEMO 4: SECURITY FILTER MIDDLEWARE")
    print("="*80)
    print("\nUse Case: Protect sensitive information (PII) from being sent to the model")
    print("Benefit: Compliance with privacy regulations (GDPR, HIPAA, etc.)\n")
    
    demo = MiddlewareDemo(use_openai=True)
    security_mw = SecurityFilterMiddleware()
    
    # Message containing sensitive information
    messages = [
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {
            'role': 'user',
            'content': 'My email is john.doe@example.com and my phone is 555-123-4567. '
                      'Can you help me with my account?'
        }
    ]
    
    print("\nOriginal message contains:")
    print("  - Email address: john.doe@example.com")
    print("  - Phone number: 555-123-4567\n")
    
    response = demo.simulate_call_with_middleware(messages, [security_mw])
    
    if response:
        print(f"\n[RESPONSE] {response.content[:150]}...")
    
    print("\nKey Insight: Security filter protects PII without requiring model-level changes")


def demo_5_expertise_based():
    """
    Demo 5: Expertise-Based Middleware
    
    Shows dynamic behavior adjustment based on user skill level.
    Provides personalized experiences for different user segments.
    """
    print("\n" + "="*80)
    print("DEMO 5: EXPERTISE-BASED MIDDLEWARE")
    print("="*80)
    print("\nUse Case: Adjust agent behavior based on user expertise level")
    print("Benefit: Personalized experience - experts get advanced features, beginners get guidance\n")
    
    demo = MiddlewareDemo(use_openai=True)
    
    # Test with beginner user
    print("\n--- Scenario 1: Beginner User ---")
    beginner_context = UserContext(user_id="user_001", expertise_level="beginner")
    expertise_mw_beginner = ExpertiseBasedMiddleware(beginner_context)
    
    messages = [
        {'role': 'user', 'content': 'What is a REST API?'}
    ]
    
    response1 = demo.simulate_call_with_middleware(messages, [expertise_mw_beginner])
    if response1:
        print(f"\n[RESPONSE FOR BEGINNER] {response1.content[:200]}...")
    
    # Test with expert user
    print("\n--- Scenario 2: Expert User ---")
    expert_context = UserContext(user_id="user_002", expertise_level="expert")
    expertise_mw_expert = ExpertiseBasedMiddleware(expert_context)
    
    response2 = demo.simulate_call_with_middleware(messages, [expertise_mw_expert])
    if response2:
        print(f"\n[RESPONSE FOR EXPERT] {response2.content[:200]}...")
    
    print("\nKey Insight: Same input, different expertise levels = different response styles")


def demo_6_middleware_stack():
    """
    Demo 6: Combining Multiple Middleware (The Stack)
    
    Shows the real power of middleware - composing multiple behaviors.
    This is how production systems leverage middleware architecture.
    """
    print("\n" + "="*80)
    print("DEMO 6: MIDDLEWARE STACK (COMBINING MULTIPLE MIDDLEWARE)")
    print("="*80)
    print("\nUse Case: Combine multiple middleware for production-grade agent")
    print("Benefit: Layered controls - logging, security, cost control, personalization all at once\n")
    
    demo = MiddlewareDemo(use_openai=True)
    
    # Create middleware stack
    context = UserContext(user_id="user_003", expertise_level="expert")
    
    middleware_stack = [
        LoggingMiddleware(verbose=True),           # Log everything
        SecurityFilterMiddleware(),                 # Filter PII
        TokenBudgetMiddleware(max_tokens=2000),    # Control costs
        ExpertiseBasedMiddleware(context),          # Personalize
    ]
    
    print("\nMiddleware Stack (execution order):")
    for i, mw in enumerate(middleware_stack, 1):
        print(f"  {i}. {mw.__class__.__name__}")
    
    messages = [
        {
            'role': 'user',
            'content': 'My email is contact@company.com. Explain microservices architecture.'
        }
    ]
    
    print("\n--- Processing through middleware stack ---")
    response = demo.simulate_call_with_middleware(messages, middleware_stack)
    
    if response:
        print(f"\n[FINAL RESPONSE] {response.content[:200]}...")
    
    print("\nKey Insight: Middleware stack = modular, composable, production-ready architecture")


def demo_7_comparison_old_vs_new():
    """
    Demo 7: Old Way vs New Way
    
    Compares the old manual approach with the new middleware approach.
    Highlights the architectural improvement.
    """
    print("\n" + "="*80)
    print("DEMO 7: OLD WAY VS NEW WAY - ARCHITECTURAL COMPARISON")
    print("="*80)
    
    print("\n--- OLD WAY (Pre v1.0): Manual Context Management ---")
    print("""
    def old_agent_loop(user_input, tools, llm):
        messages = [{"role": "user", "content": user_input}]
        
        for iteration in range(10):
            # Manually check message length
            if len(messages) > 20:
                messages = summarize_history(messages)
            
            # Manually filter PII
            messages = redact_sensitive_data(messages)
            
            # Manually select tools
            available_tools = select_tools(messages, tools)
            
            # Manually adjust prompt
            system_prompt = generate_prompt(iteration)
            
            # Manually track costs
            if token_count > budget:
                raise Exception("Budget exceeded")
            
            response = llm.invoke(messages, tools=available_tools)
            # ... more manual work
    
    Problems:
    - Tightly coupled logic
    - Hard to test individual components
    - Difficult to reuse across projects
    - Poor maintainability
    - No standard patterns
    """)
    
    print("\n--- NEW WAY (v1.0): Middleware Architecture ---")
    print("""
    middleware_stack = [
        LoggingMiddleware(),
        SecurityFilterMiddleware(),
        TokenBudgetMiddleware(max_tokens=10000),
        ContextSummarizationMiddleware(max_messages=10),
        ExpertiseBasedMiddleware(context),
    ]
    
    agent = create_agent(
        model="gpt-4",
        tools=[read_email, send_email],
        middleware=middleware_stack
    )
    
    Benefits:
    - Separation of concerns (each middleware = one responsibility)
    - Easy to test (test each middleware independently)
    - Reusable (same middleware across projects)
    - Maintainable (add/remove middleware without touching core)
    - Standard patterns (community-driven best practices)
    - Composable (mix and match like building blocks)
    """)
    
    print("\nKey Insight: Middleware architecture transforms ad-hoc code into systematic engineering")


def main():
    """Run all demo examples"""
    print("\n" + "="*80)
    print("LANGCHAIN V1.0 MIDDLEWARE DEMONSTRATIONS")
    print("Context Control for Production AI Agents")
    print("="*80)
    
    demos = [
        ("Logging Middleware", demo_1_logging_middleware),
        ("Token Budget Control", demo_2_token_budget),
        ("Context Summarization", demo_3_context_summarization),
        ("Security Filtering", demo_4_security_filter),
        ("Expertise-Based Personalization", demo_5_expertise_based),
        ("Middleware Stack", demo_6_middleware_stack),
        ("Old vs New Architecture", demo_7_comparison_old_vs_new),
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos) + 1}. Run All Demos")
    print("  0. Exit")
    
    while True:
        try:
            choice = input("\nSelect demo number (0 to exit): ").strip()
            
            if choice == "0":
                print("\nExiting demo. Thank you!")
                break
            
            choice_num = int(choice)
            
            if choice_num == len(demos) + 1:
                # Run all demos
                for name, demo_func in demos:
                    demo_func()
                    input("\nPress Enter to continue to next demo...")
            elif 1 <= choice_num <= len(demos):
                demos[choice_num - 1][1]()
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nError running demo: {str(e)}")


if __name__ == "__main__":
    main()
