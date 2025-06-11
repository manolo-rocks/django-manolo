# myapp/middleware.py
import re
import logging
from django.http import HttpResponse
import urllib.parse

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # All dangerous patterns to block
        self.attack_patterns = [
            # Command injection
            r'\$\{.*\}',  # Shell variables ${IFS}
            r'nslookup|dig|host',  # DNS commands
            r'curl|wget|nc',  # Network commands
            r'ping|traceroute',  # Network tools
            r'\|\||&&',  # Command chaining
            r'bxss\.me',  # Known security testing domain

            # Previous attacks we've seen
            r'\x00',  # Null bytes
            r'\.\.[\\/]',  # Path traversal
            r'etc[\\/]passwd',  # System files
            r'<script',  # XSS
            r'javascript:',  # JS injection
            r'[\'";].*[\'";]',  # Multiple SQL injection chars
            r'http[s]?://.*\.(exe|bat|sh|php|jsp)',  # Malicious URLs
        ]

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')

        # Check URL path (this was missing!)
        url_path = urllib.parse.unquote(request.get_full_path())

        # Check if malicious patterns are in the URL path
        for pattern in self.attack_patterns:
            if re.search(pattern, url_path, re.IGNORECASE):
                attack_type = self._identify_attack_type(pattern, url_path)

                logger.critical(
                    f"SECURITY BLOCK: {attack_type} in URL from {ip} | "
                    f"URL: {url_path[:200]} | "
                    f"UA: {request.META.get('HTTP_USER_AGENT', 'Unknown')[:50]}"
                )

                return HttpResponse(
                    'Request blocked for security reasons',
                    status=403
                )

        # Check GET and POST parameters
        all_params = {}
        all_params.update(request.GET.dict())
        all_params.update(request.POST.dict())

        for param_name, param_value in all_params.items():
            for pattern in self.attack_patterns:
                if re.search(pattern, str(param_value), re.IGNORECASE):
                    attack_type = self._identify_attack_type(pattern, param_value)

                    logger.critical(
                        f"SECURITY BLOCK: {attack_type} in params from {ip} | "
                        f"Param: {param_name} | "
                        f"Value: {str(param_value)[:100]} | "
                        f"UA: {request.META.get('HTTP_USER_AGENT', 'Unknown')[:50]}"
                    )

                    return HttpResponse(
                        'Request blocked for security reasons',
                        status=403
                    )

        # If no malicious patterns found, continue normally
        response = self.get_response(request)
        return response

    def _identify_attack_type(self, pattern, value):
        value_lower = str(value).lower()

        if any(cmd in value_lower for cmd in ['nslookup', 'curl', 'wget', 'ping']):
            return "Command Injection"
        elif '\x00' in str(value):
            return "Null Byte Injection"
        elif '..' in value_lower and ('/' in value_lower or '\\' in value_lower):
            return "Path Traversal"
        elif 'script' in value_lower:
            return "XSS Attempt"
        elif 'http://' in value_lower or 'https://' in value_lower:
            return "SSRF/URL Injection"
        elif any(char in value_lower for char in ["'", '"', ';']):
            return "SQL Injection"
        elif 'bxss.me' in value_lower:
            return "Security Scanner"
        else:
            return "Malicious Pattern"