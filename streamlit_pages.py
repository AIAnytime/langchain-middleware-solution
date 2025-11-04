"""
Streamlit page components for middleware demonstrations
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def check_api_keys():
    """Check if API keys are configured"""
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    has_openai = openai_key and len(openai_key) > 10
    has_gemini = gemini_key and len(gemini_key) > 10
    
    return has_openai, has_gemini


def home_page():
    """Main home page"""
    st.markdown('<div class="main-header">LangChain v1.0 Middleware Demo</div>', unsafe_allow_html=True)
    st.markdown("### Systematic Context Control for AI Agents")
    
    st.markdown("""
    <div class="info-box">
    <strong>What is Middleware?</strong><br>
    Middleware acts as an information coordination layer that processes data before it reaches 
    the AI model and after it returns. It enables systematic control over context, security, 
    costs, and agent behavior.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">Execution Flow</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.code("""
User Input
    ↓
[Middleware Stack]
    ├─ Logging
    ├─ Security Filter
    ├─ Token Budget
    └─ Expertise Level
    ↓
AI Model
    ↓
Response
        """, language="text")
    
    st.markdown('<div class="sub-header">Key Benefits</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card"><strong>Separation of Concerns</strong><br>Each middleware handles one responsibility</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><strong>Composability</strong><br>Mix and match like building blocks</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><strong>Testability</strong><br>Test each component independently</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><strong>Reusability</strong><br>Write once, use everywhere</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card"><strong>Production-Ready</strong><br>Built-in security and monitoring</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-card"><strong>Standard Patterns</strong><br>Community-driven best practices</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">Environment Status</div>', unsafe_allow_html=True)
    
    has_openai, has_gemini = check_api_keys()
    
    col1, col2 = st.columns(2)
    with col1:
        if has_openai:
            st.success("OpenAI API Key: Configured")
        else:
            st.warning("OpenAI API Key: Not configured")
    
    with col2:
        if has_gemini:
            st.success("Gemini API Key: Configured")
        else:
            st.warning("Gemini API Key: Not configured")


def logging_demo_page():
    """Logging middleware demonstration"""
    st.markdown('<div class="main-header">Logging Middleware</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Use Case:</strong> Track all agent interactions for debugging and monitoring<br>
    <strong>Benefit:</strong> Complete visibility into agent decision-making process
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
from middleware import LoggingMiddleware

logging_mw = LoggingMiddleware(verbose=True)
# Tracks timestamps, input/output, call counts
    """, language="python")
    
    user_input = st.text_area("Enter your message:", value="What is the capital of France?", height=100)
    
    if st.button("Run Demo", type="primary"):
        from middleware import LoggingMiddleware
        
        logging_mw = LoggingMiddleware(verbose=True)
        messages = [
            {'role': 'system', 'content': 'You are a helpful AI assistant.'},
            {'role': 'user', 'content': user_input}
        ]
        
        with st.expander("View Detailed Logs", expanded=True):
            st.code(f"""[MIDDLEWARE] LoggingMiddleware - Call #1
[TIMESTAMP] {datetime.now().isoformat()}
[INPUT] Processing {len(messages)} message(s)
  Message 1: You are a helpful AI assistant.
  Message 2: {user_input}""")
        
        result = logging_mw.before_model(messages)
        st.success(f"Processed {len(result)} messages successfully")
        st.metric("Call Count", logging_mw.call_count)


def token_budget_page():
    """Token budget middleware demonstration"""
    st.markdown('<div class="main-header">Token Budget Middleware</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Use Case:</strong> Prevent excessive API costs by enforcing token limits<br>
    <strong>Benefit:</strong> Predictable costs and protection against budget overruns
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        max_tokens = st.number_input("Max Tokens", value=1000, min_value=100, step=100)
    with col2:
        max_requests = st.number_input("Max Requests", value=10, min_value=1, step=1)
    
    if 'budget_mw' not in st.session_state:
        from middleware import TokenBudgetMiddleware
        st.session_state.budget_mw = TokenBudgetMiddleware(max_tokens=max_tokens, max_requests=max_requests)
    
    user_input = st.text_area("Enter your message:", value="Explain quantum computing in simple terms.", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Send Request", type="primary"):
            messages = [{'role': 'user', 'content': user_input}]
            try:
                st.session_state.budget_mw.before_model(messages)
                st.success("Request approved")
            except Exception as e:
                st.error(f"Request blocked: {str(e)}")
    
    with col2:
        if st.button("Reset Budget"):
            from middleware import TokenBudgetMiddleware
            st.session_state.budget_mw = TokenBudgetMiddleware(max_tokens=max_tokens, max_requests=max_requests)
            st.success("Budget reset")
    
    st.markdown('<div class="sub-header">Budget Status</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tokens Used", st.session_state.budget_mw.total_tokens_used, f"of {max_tokens}")
    with col2:
        st.metric("Requests Made", st.session_state.budget_mw.request_count, f"of {max_requests}")
    with col3:
        remaining = max_tokens - st.session_state.budget_mw.total_tokens_used
        st.metric("Tokens Remaining", remaining)
    
    progress = min(st.session_state.budget_mw.total_tokens_used / max_tokens, 1.0)
    st.progress(progress, text=f"Budget Usage: {progress*100:.1f}%")


def security_filter_page():
    """Security filter middleware demonstration"""
    st.markdown('<div class="main-header">Security Filter Middleware</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Use Case:</strong> Protect sensitive information (PII) from being sent to the model<br>
    <strong>Benefit:</strong> Compliance with privacy regulations (GDPR, HIPAA, etc.)
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><strong>Email Addresses</strong><br>john@example.com → [REDACTED_EMAIL]</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><strong>Phone Numbers</strong><br>555-123-4567 → [REDACTED_PHONE]</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><strong>API Keys</strong><br>sk_test_123... → [REDACTED_API_KEY]</div>', unsafe_allow_html=True)
    
    user_input = st.text_area(
        "Enter text with sensitive information:",
        value="My email is john.doe@example.com and my phone is 555-123-4567. Can you help me?",
        height=100
    )
    
    if st.button("Filter Sensitive Data", type="primary"):
        from middleware import SecurityFilterMiddleware
        
        security_mw = SecurityFilterMiddleware()
        messages = [{'role': 'user', 'content': user_input}]
        result = security_mw.before_model(messages)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original Text:**")
            st.code(user_input, language="text")
        with col2:
            st.markdown("**Filtered Text:**")
            st.code(result[0]['content'], language="text")
        
        if security_mw.redaction_count > 0:
            st.success(f"Redacted {security_mw.redaction_count} sensitive items")


def context_summarization_page():
    """Context summarization middleware demonstration"""
    st.markdown('<div class="main-header">Context Summarization Middleware</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Use Case:</strong> Manage long conversation histories by automatic summarization<br>
    <strong>Benefit:</strong> Maintain context without hitting token limits
    </div>
    """, unsafe_allow_html=True)
    
    max_messages = st.slider("Maximum Messages", min_value=3, max_value=20, value=5)
    num_messages = st.number_input("Number of messages in conversation", min_value=1, max_value=30, value=12)
    
    if st.button("Simulate Conversation", type="primary"):
        from middleware import ContextSummarizationMiddleware
        
        summarization_mw = ContextSummarizationMiddleware(max_messages=max_messages)
        
        messages = [{'role': 'system', 'content': 'You are a helpful AI assistant.'}]
        topics = ['Python', 'JavaScript', 'Go', 'Rust', 'Java', 'C++', 'Ruby', 'Swift']
        
        for i in range(num_messages - 1):
            if i % 2 == 0:
                messages.append({'role': 'user', 'content': f'Tell me about {topics[i // 2 % len(topics)]}'})
            else:
                messages.append({'role': 'assistant', 'content': f'{topics[i // 2 % len(topics)]} is a programming language...'})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Original Messages", len(messages))
        
        result = summarization_mw.before_model(messages)
        
        with col2:
            st.metric("After Summarization", len(result))
        
        if summarization_mw.summarization_count > 0:
            reduction = ((len(messages) - len(result)) / len(messages)) * 100
            st.success(f"Reduced message count by {reduction:.1f}%")


def expertise_based_page():
    """Expertise-based middleware demonstration"""
    st.markdown('<div class="main-header">Expertise-Based Middleware</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Use Case:</strong> Adjust agent behavior based on user expertise level<br>
    <strong>Benefit:</strong> Personalized experience for different user skill levels
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        user_id = st.text_input("User ID", value="user_001")
    with col2:
        expertise_level = st.selectbox("Expertise Level", options=["beginner", "intermediate", "expert"], index=0)
    
    question = st.text_area("Enter your question:", value="What is a REST API?", height=100)
    
    if st.button("Compare Responses", type="primary"):
        from middleware import ExpertiseBasedMiddleware, UserContext
        
        st.markdown("---")
        st.markdown("**Beginner Mode:**")
        beginner_context = UserContext(user_id=user_id, expertise_level="beginner")
        beginner_mw = ExpertiseBasedMiddleware(beginner_context)
        
        messages = [{'role': 'user', 'content': question}]
        beginner_result = beginner_mw.before_model(messages)
        
        with st.expander("System Prompt for Beginner"):
            for msg in beginner_result:
                if msg.get('role') == 'system':
                    st.code(msg['content'], language="text")
        
        st.info("Response style: Simple language, step-by-step explanations, helpful examples")
        
        st.markdown("---")
        st.markdown("**Expert Mode:**")
        expert_context = UserContext(user_id=user_id, expertise_level="expert")
        expert_mw = ExpertiseBasedMiddleware(expert_context)
        expert_result = expert_mw.before_model(messages)
        
        with st.expander("System Prompt for Expert"):
            for msg in expert_result:
                if msg.get('role') == 'system':
                    st.code(msg['content'], language="text")
        
        st.info("Response style: Technical terminology, detailed explanations, advanced options")


def middleware_stack_page():
    """Middleware stack demonstration"""
    st.markdown('<div class="main-header">Middleware Stack</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>Use Case:</strong> Combine multiple middleware for production-grade agent<br>
    <strong>Benefit:</strong> Layered controls - logging, security, cost control, personalization
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Select middleware to include:")
    
    col1, col2 = st.columns(2)
    with col1:
        use_logging = st.checkbox("Logging Middleware", value=True)
        use_security = st.checkbox("Security Filter", value=True)
        use_budget = st.checkbox("Token Budget", value=True)
    with col2:
        use_summarization = st.checkbox("Context Summarization", value=False)
        use_expertise = st.checkbox("Expertise-Based", value=True)
    
    stack_items = []
    if use_logging:
        stack_items.append("LoggingMiddleware()")
    if use_security:
        stack_items.append("SecurityFilterMiddleware()")
    if use_budget:
        stack_items.append("TokenBudgetMiddleware(max_tokens=2000)")
    if use_summarization:
        stack_items.append("ContextSummarizationMiddleware()")
    if use_expertise:
        stack_items.append("ExpertiseBasedMiddleware(context)")
    
    if stack_items:
        stack_code = "middleware_stack = [\n"
        for item in stack_items:
            stack_code += f"    {item},\n"
        stack_code += "]"
        
        st.code(stack_code, language="python")
        st.metric("Stack Size", len(stack_items), "middleware layers")
    
    user_input = st.text_area("Enter test message:", value="Contact me at test@example.com", height=100)
    
    if st.button("Process Through Stack", type="primary") and stack_items:
        from middleware import (
            LoggingMiddleware, SecurityFilterMiddleware,
            TokenBudgetMiddleware, ExpertiseBasedMiddleware, UserContext
        )
        
        messages = [{'role': 'user', 'content': user_input}]
        middleware_stack = []
        
        if use_logging:
            middleware_stack.append(LoggingMiddleware(verbose=False))
        if use_security:
            middleware_stack.append(SecurityFilterMiddleware())
        if use_budget:
            middleware_stack.append(TokenBudgetMiddleware(max_tokens=2000))
        if use_expertise:
            context = UserContext(expertise_level="expert")
            middleware_stack.append(ExpertiseBasedMiddleware(context))
        
        processed = messages.copy()
        for i, mw in enumerate(middleware_stack):
            st.text(f"Step {i+1}: {mw.__class__.__name__}")
            if hasattr(mw, 'before_model'):
                result = mw.before_model(processed)
                processed = result if not isinstance(result, tuple) else result[0]
        
        st.success(f"Processed through {len(middleware_stack)} middleware layers")


def comparison_page():
    """Old vs New architecture comparison"""
    st.markdown('<div class="main-header">Architecture Comparison</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Old Way (Pre v1.0)")
        st.code("""
def custom_agent_loop(user_input):
    messages = [{"role": "user", "content": user_input}]
    
    for iteration in range(10):
        # Manual everything
        if len(messages) > 20:
            messages = summarize_history(messages)
        
        messages = redact_sensitive_data(messages)
        available_tools = select_tools(messages, tools)
        
        if token_count > budget:
            raise Exception("Budget exceeded")
        
        response = llm.invoke(messages)
        """, language="python")
        
        st.markdown("""
        <div class="warning-box">
        <strong>Problems:</strong><br>
        • Tightly coupled<br>
        • Hard to test<br>
        • Not reusable<br>
        • Poor maintainability
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### New Way (v1.0)")
        st.code("""
middleware_stack = [
    LoggingMiddleware(),
    SecurityFilterMiddleware(),
    TokenBudgetMiddleware(max_tokens=10000),
    ContextSummarizationMiddleware(),
    ExpertiseBasedMiddleware(context),
]

agent = create_agent(
    model="gpt-4",
    tools=tools,
    middleware=middleware_stack
)

response = agent.invoke(user_input)
        """, language="python")
        
        st.markdown("""
        <div class="success-box">
        <strong>Benefits:</strong><br>
        • Separation of concerns<br>
        • Easy to test<br>
        • Highly reusable<br>
        • Maintainable
        </div>
        """, unsafe_allow_html=True)


def playground_page():
    """Interactive playground for testing middleware"""
    st.markdown('<div class="main-header">Middleware Playground</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    Test middleware with real API calls. Configure API keys in your .env file.
    </div>
    """, unsafe_allow_html=True)
    
    has_openai, has_gemini = check_api_keys()
    
    if not (has_openai or has_gemini):
        st.warning("Please configure API keys in .env file to use the playground")
        return
    
    model_choice = st.selectbox("Select Model", options=["OpenAI GPT-3.5", "Google Gemini"] if has_gemini else ["OpenAI GPT-3.5"])
    
    st.markdown("### Configure Middleware")
    use_logging = st.checkbox("Enable Logging", value=True)
    use_security = st.checkbox("Enable Security Filter", value=True)
    
    user_prompt = st.text_area("Enter your prompt:", value="What is machine learning?", height=150)
    
    if st.button("Run with Middleware", type="primary"):
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        from middleware import LoggingMiddleware, SecurityFilterMiddleware
        
        middleware_stack = []
        if use_logging:
            middleware_stack.append(LoggingMiddleware(verbose=False))
        if use_security:
            middleware_stack.append(SecurityFilterMiddleware())
        
        messages = [
            {'role': 'system', 'content': 'You are a helpful AI assistant.'},
            {'role': 'user', 'content': user_prompt}
        ]
        
        # Apply middleware
        processed = messages.copy()
        for mw in middleware_stack:
            if hasattr(mw, 'before_model'):
                processed = mw.before_model(processed)
        
        with st.spinner("Calling AI model..."):
            try:
                model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
                formatted_messages = [
                    SystemMessage(content=msg['content']) if msg['role'] == 'system'
                    else HumanMessage(content=msg['content'])
                    for msg in processed
                ]
                response = model.invoke(formatted_messages)
                
                st.success("Response received!")
                st.markdown("### AI Response")
                st.write(response.content)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
