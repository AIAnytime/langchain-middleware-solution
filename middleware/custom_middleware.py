"""
Custom Middleware Implementations for LangChain v1.0

This module demonstrates various middleware patterns for AI agent context control.
Each middleware intercepts agent execution at different points to manage context,
security, and behavior.
"""

from dataclasses import dataclass
from typing import Callable, Any, Dict
from datetime import datetime
import json


@dataclass
class UserContext:
    """Context schema for tracking user information across middleware"""
    user_id: str = "unknown"
    expertise_level: str = "beginner"
    session_start: str = ""
    token_count: int = 0
    request_count: int = 0


class LoggingMiddleware:
    """
    Logs all agent interactions for debugging and monitoring.
    Intercepts both input and output to track the complete flow.
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.call_count = 0
    
    def before_model(self, messages: list) -> list:
        """Log incoming messages before they reach the model"""
        self.call_count += 1
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"[MIDDLEWARE] LoggingMiddleware - Call #{self.call_count}")
            print(f"[TIMESTAMP] {datetime.now().isoformat()}")
            print(f"[INPUT] Processing {len(messages)} message(s)")
            for i, msg in enumerate(messages):
                content = msg.get('content', '') if isinstance(msg, dict) else str(msg)
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"  Message {i+1}: {preview}")
            print(f"{'='*60}")
        
        return messages
    
    def after_model(self, response: Any) -> Any:
        """Log model response after generation"""
        if self.verbose:
            print(f"\n[MIDDLEWARE] LoggingMiddleware - Response received")
            response_preview = str(response)[:150] + "..." if len(str(response)) > 150 else str(response)
            print(f"[OUTPUT] {response_preview}")
            print(f"{'='*60}\n")
        
        return response


class TokenBudgetMiddleware:
    """
    Enforces token limits to prevent excessive API costs.
    Tracks cumulative token usage and blocks requests exceeding budget.
    """
    
    def __init__(self, max_tokens: int = 10000, max_requests: int = 50):
        self.max_tokens = max_tokens
        self.max_requests = max_requests
        self.total_tokens_used = 0
        self.request_count = 0
    
    def before_model(self, messages: list) -> list:
        """Check token budget before allowing model call"""
        self.request_count += 1
        
        # Rough token estimation (avg 4 chars per token)
        estimated_tokens = sum(len(str(msg)) for msg in messages) // 4
        
        print(f"\n[TOKEN BUDGET] Request #{self.request_count}")
        print(f"  Estimated tokens: {estimated_tokens}")
        print(f"  Used so far: {self.total_tokens_used}/{self.max_tokens}")
        print(f"  Requests: {self.request_count}/{self.max_requests}")
        
        if self.total_tokens_used + estimated_tokens > self.max_tokens:
            raise Exception(
                f"Token budget exceeded! Limit: {self.max_tokens}, "
                f"Would use: {self.total_tokens_used + estimated_tokens}"
            )
        
        if self.request_count > self.max_requests:
            raise Exception(
                f"Request limit exceeded! Maximum {self.max_requests} requests allowed."
            )
        
        self.total_tokens_used += estimated_tokens
        return messages


class ContextSummarizationMiddleware:
    """
    Automatically summarizes conversation history when it gets too long.
    Prevents context window overflow while preserving key information.
    """
    
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.summarization_count = 0
    
    def before_model(self, messages: list) -> list:
        """Summarize messages if conversation history is too long"""
        if len(messages) <= self.max_messages:
            return messages
        
        self.summarization_count += 1
        print(f"\n[SUMMARIZATION] Context too long ({len(messages)} messages)")
        print(f"  Condensing to most recent {self.max_messages} messages")
        print(f"  Summarization event #{self.summarization_count}")
        
        # Keep system message and recent messages
        system_messages = [msg for msg in messages if msg.get('role') == 'system']
        recent_messages = messages[-(self.max_messages - len(system_messages)):]
        
        # Create summary of older messages
        old_messages = messages[len(system_messages):-(self.max_messages - len(system_messages))]
        if old_messages:
            summary = {
                'role': 'system',
                'content': f"[Summary of {len(old_messages)} previous messages: Context about earlier conversation]"
            }
            return system_messages + [summary] + recent_messages
        
        return system_messages + recent_messages


class SecurityFilterMiddleware:
    """
    Filters sensitive information from inputs and outputs.
    Prevents PII (emails, phone numbers, API keys) from being sent to the model.
    """
    
    def __init__(self):
        self.redaction_count = 0
        import re
        # Regex patterns for common sensitive data
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'api_key': re.compile(r'\b[A-Za-z0-9_-]{20,}\b(?=.*key)', re.IGNORECASE),
        }
    
    def before_model(self, messages: list) -> list:
        """Redact sensitive information before sending to model"""
        filtered_messages = []
        redacted_this_call = False
        
        for msg in messages:
            if isinstance(msg, dict) and 'content' in msg:
                content = msg['content']
                original_content = content
                
                # Apply all redaction patterns
                for data_type, pattern in self.patterns.items():
                    content = pattern.sub(f'[REDACTED_{data_type.upper()}]', content)
                
                if content != original_content:
                    redacted_this_call = True
                    self.redaction_count += 1
                
                filtered_messages.append({**msg, 'content': content})
            else:
                filtered_messages.append(msg)
        
        if redacted_this_call:
            print(f"\n[SECURITY] Sensitive data redacted (Total: {self.redaction_count} instances)")
        
        return filtered_messages


class ExpertiseBasedMiddleware:
    """
    Dynamically adjusts model behavior based on user expertise level.
    Experts get more powerful models and tools, beginners get simplified versions.
    """
    
    def __init__(self, context: UserContext):
        self.context = context
    
    def before_model(self, messages: list) -> list:
        """Inject expertise-level context into system prompt"""
        expertise = self.context.expertise_level
        
        print(f"\n[EXPERTISE] User level: {expertise.upper()}")
        
        # Add expertise-specific system message
        if expertise == "expert":
            system_msg = {
                'role': 'system',
                'content': (
                    "You are assisting an expert user. Provide detailed technical explanations, "
                    "use domain-specific terminology, and offer advanced options. "
                    "Assume deep knowledge of the subject matter."
                )
            }
            print("  Mode: Advanced explanations, full technical details")
        else:
            system_msg = {
                'role': 'system',
                'content': (
                    "You are assisting a beginner. Use simple language, provide step-by-step "
                    "explanations, avoid jargon, and include helpful examples. "
                    "Be patient and educational."
                )
            }
            print("  Mode: Simplified explanations, beginner-friendly")
        
        # Insert after any existing system messages or at the start
        system_count = sum(1 for msg in messages if msg.get('role') == 'system')
        messages.insert(system_count, system_msg)
        
        return messages


class ToolAccessControlMiddleware:
    """
    Controls which tools the agent can access based on user permissions.
    Implements role-based access control (RBAC) for agent tools.
    """
    
    def __init__(self, allowed_tools: list[str], context: UserContext):
        self.allowed_tools = allowed_tools
        self.context = context
        self.blocked_attempts = 0
    
    def wrap_tool_call(self, tool_name: str, tool_args: dict) -> tuple[bool, str]:
        """Check if tool access is allowed before execution"""
        if tool_name in self.allowed_tools:
            print(f"\n[ACCESS CONTROL] Tool '{tool_name}' - ALLOWED")
            return True, ""
        else:
            self.blocked_attempts += 1
            print(f"\n[ACCESS CONTROL] Tool '{tool_name}' - BLOCKED")
            print(f"  User: {self.context.user_id}")
            print(f"  Allowed tools: {', '.join(self.allowed_tools)}")
            print(f"  Total blocked attempts: {self.blocked_attempts}")
            return False, f"Access denied: Tool '{tool_name}' not permitted for user '{self.context.user_id}'"


class CachingMiddleware:
    """
    Caches model responses to avoid redundant API calls.
    Uses message content hash as cache key for fast lookups.
    """
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.hit_count = 0
        self.miss_count = 0
    
    def _get_cache_key(self, messages: list) -> str:
        """Generate cache key from messages"""
        import hashlib
        content = json.dumps(messages, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    def before_model(self, messages: list) -> tuple[list, str]:
        """Check cache before making API call"""
        cache_key = self._get_cache_key(messages)
        
        if cache_key in self.cache:
            self.hit_count += 1
            hit_rate = self.hit_count / (self.hit_count + self.miss_count) * 100
            print(f"\n[CACHE] HIT - Returning cached response")
            print(f"  Hit rate: {hit_rate:.1f}% ({self.hit_count}/{self.hit_count + self.miss_count})")
            return self.cache[cache_key], cache_key
        else:
            self.miss_count += 1
            print(f"\n[CACHE] MISS - Making new API call")
            print(f"  Cache size: {len(self.cache)} entries")
            return messages, cache_key
    
    def after_model(self, cache_key: str, response: Any) -> Any:
        """Store response in cache"""
        self.cache[cache_key] = response
        return response
