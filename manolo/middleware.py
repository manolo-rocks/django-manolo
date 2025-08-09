# myapp/middleware.py
import re
import logging
from django.http import HttpResponse
import urllib.parse

log = logging.getLogger(__name__)


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # All dangerous patterns to block
        dns_commands_pattern = (
            r"\b(?:"
            r"nslookup|dig|host|whois|ping|traceroute|tracert|"
            r"nmap|netstat|arp|route|drill|kdig|delv|"
            r"curl|wget|nc|netcat|telnet|ssh"
            r")\b"
        )

        self.attack_patterns = [
            # Command injection
            r"\$\{.*\}",  # Shell variables ${IFS}
            dns_commands_pattern,
            r"curl|wget",  # Network commands
            r"ping|traceroute",  # Network tools
            r"\|\||&&",  # Command chaining
            r"bxss\.me",  # Known security testing domain
            # Previous attacks we've seen
            r"\x00",  # Null bytes
            r"\.\./\.\.",  # ../.. (actual path traversal)
            r"\.\./[^.]",  # ../ followed by non-dot (actual traversal)
            r"\.\.\\",  # ..\ (Windows path traversal)
            r"etc[\\/]passwd",  # System files
            r"<script",  # XSS
            r"javascript:",  # JS injection
            # Specific SQL injection patterns
            r"'.*OR.*'",  # ' OR ' attacks
            r"'.*UNION.*SELECT",  # UNION SELECT attacks
            r"'.*DROP.*TABLE",  # DROP TABLE attacks
            r"'.*INSERT.*INTO",  # INSERT attacks
            r"'.*DELETE.*FROM",  # DELETE attacks
            r"';.*--",  # Comment-based SQL injection
            r'".*OR.*"',  # Double quote OR attacks
            r"http[s]?://.*\.(exe|bat|sh|php|jsp)",  # Malicious URLs
        ]

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        original_path = request.path
        cleaned_path = self.sanitize_path(original_path)
        request.path = cleaned_path
        request.path_info = cleaned_path

        if request.GET:
            mutable_get = request.GET.copy()
            has_changes = False

            for key, value in mutable_get.items():
                sanitized_value = self.sanitize_parameter(value, key)
                if sanitized_value != value:
                    mutable_get[key] = sanitized_value
                    has_changes = True

            if has_changes:
                request.GET = mutable_get
                request.META["QUERY_STRING"] = mutable_get.urlencode()

        # Check URL path (this was missing!)
        url_path = urllib.parse.unquote(request.get_full_path())

        # Check if malicious patterns are in the URL path
        for pattern in self.attack_patterns:
            if re.search(pattern, url_path, re.IGNORECASE):
                attack_type = self._identify_attack_type(pattern, url_path)
                if attack_type:
                    log.error(
                        f"SECURITY BLOCK: {attack_type} in URL from {ip} | "
                        f"URL: {url_path[:200]} | "
                        f"UA: {request.META.get('HTTP_USER_AGENT', 'Unknown')[:50]}"
                    )

                    return HttpResponse("Request blocked for security reasons", status=403)

        # Check GET and POST parameters
        all_params = {}
        all_params.update(request.GET.dict())
        all_params.update(request.POST.dict())

        for param_name, param_value in all_params.items():
            for pattern in self.attack_patterns:
                if re.search(pattern, str(param_value), re.IGNORECASE):
                    attack_type = self._identify_attack_type(pattern, param_value)

                    if attack_type:
                        log.error(
                            f"SECURITY BLOCK: {attack_type} in params from {ip} | "
                            f"Param: {param_name} | "
                            f"Value: {str(param_value)[:100]} | "
                            f"UA: {request.META.get('HTTP_USER_AGENT', 'Unknown')[:50]}"
                        )

                        return HttpResponse("Request blocked for security reasons", status=403)

        # If no malicious patterns found, continue normally
        response = self.get_response(request)
        return response

    def _identify_attack_type(self, pattern, value):
        value_lower = str(value).lower()

        if self.is_command_injection(value_lower):
            return "Command Injection"
        elif "\x00" in str(value):
            return "Null Byte Injection"
        elif "../" in value_lower or "..\\" in value_lower:
            return "Path Traversal"
        elif "script" in value_lower:
            return "XSS Attempt"
        elif "http://" in value_lower or "https://" in value_lower:
            return "SSRF/URL Injection"
        elif any(char in value_lower for char in ["'", '"', ";"]):
            return "SQL Injection"
        elif "bxss.me" in value_lower:
            return "Security Scanner"
        else:
            log.info("No specific attack type identified for pattern")
            return ""

    def sanitize_path(self, path):
        # Remove consecutive dots from path segments
        segments = path.split("/")
        cleaned_segments = []
        for segment in segments:
            # Remove excessive dots but keep legitimate patterns
            if segment and not segment.startswith(".."):
                # Remove consecutive dots (keeping single dots)
                cleaned_segment = re.sub(r"\.{2,}", "", segment)
                cleaned_segments.append(cleaned_segment)
            else:
                cleaned_segments.append(segment)
        return "/".join(cleaned_segments)

    def sanitize_value(self, value):
        # Remove consecutive dots from parameter values
        return re.sub(r"\.{2,}", "", value)

    def is_command_injection(self, value_lower):
        commands = ["nslookup", "curl", "wget", "ping"]

        # Use word boundaries to match complete words only
        for cmd in commands:
            if re.search(r"\b" + re.escape(cmd) + r"\b", value_lower):
                log.info(f"Detected command injection attempt: {cmd} in value: {value_lower[:100]}")
                return True
        return False

    def sanitize_parameter(self, value, param_name):
        """
        Sanitize a parameter value by removing dangerous patterns.
        :param value: The parameter value to sanitize.
        :param param_name: The name of the parameter (for logging).
        :return: Sanitized value.
        """
        if "\x00" in str(value):
            value = str(value).replace("\x00", "")

        if param_name == "q":
            value = self.sanitize_search_query(value)
        elif param_name in ["sort", "dir"]:
            value = self.sanitize_sort_parameter(value)

        return value

    def sanitize_search_query(self, query):
        dangerous_patterns = ['"']
        for pattern in dangerous_patterns:
            query = re.sub(pattern, "", query, flags=re.IGNORECASE)
        return query

    def sanitize_sort_parameter(self, value):
        allowed_sorts = [
            "date",
            "full_name",
            "id_number",
            "entity",
            "reason",
            "host_name",
            "office",
        ]
        allowed_dirs = ["asc", "desc"]

        if value in allowed_sorts or value in allowed_dirs:
            return value
        return ""
