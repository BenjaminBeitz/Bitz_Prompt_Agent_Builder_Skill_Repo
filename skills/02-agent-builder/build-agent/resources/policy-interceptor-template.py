#!/usr/bin/env python3
"""
Policy & Blast Radius Safety Interceptor
Provides deterministic pre-execution inspection against destructive patterns and leaks.
"""

import re
import sys
import json
from typing import Tuple, Dict, Any

PROHIBITED_COMMAND_PATTERNS = [
    r"rm\s+-rf\s+[/~]",
    r"git\s+push\s+.*--force",
    r"drop\s+database",
    r"drop\s+table",
    r"mkfs\.",
    r":\(\)\{\s*:\|:&\s*\};:",
]

CREDENTIAL_PATTERNS = [
    (r"(sk-[a-zA-Z0-9_-]{20,})", "[REDACTED_OPENAI_KEY]"),
    (r"(rk_live_[a-zA-Z0-9_-]{20,})", "[REDACTED_STRIPE_KEY]"),
    (r"(ghp_[a-zA-Z0-9]{20,})", "[REDACTED_GITHUB_TOKEN]"),
    (r"(AIzaSy[a-zA-Z0-9_-]{33})", "[REDACTED_GEMINI_KEY]"),
    (r"(bearer\s+[a-zA-Z0-9_\-\.]{20,})", "[REDACTED_BEARER_TOKEN]"),
]

class PolicyInterceptor:
    @staticmethod
    def validate_command(command: str) -> Tuple[bool, str]:
        """
        Validates a command against prohibited safety patterns.
        Returns: (is_safe, error_message_if_any)
        """
        for pattern in PROHIBITED_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"POLICY VIOLATION: Command matches prohibited destructive signature: {pattern}"
        return True, ""

    @staticmethod
    def sanitize_payload(text: str) -> str:
        """
        Scrubs sensitive credentials and tokens from text streams.
        """
        sanitized = text
        for pattern, replacement in CREDENTIAL_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        return sanitized

    @staticmethod
    def wrap_untrusted_content(content: str, source: str = "external") -> str:
        """
        Encloses untrusted external content in semantic XML delimiters for prompt injection defense.
        """
        return f"<<<EXTERNAL_UNTRUSTED_CONTENT source=\"{source}\">>>\n{content}\n<<<END_UNTRUSTED_CONTENT>>>"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_cmd = sys.argv[1]
        safe, msg = PolicyInterceptor.validate_command(test_cmd)
        print(json.dumps({"safe": safe, "message": msg}, indent=2))
    else:
        print("Usage: python policy-interceptor-template.py <command>")
