# Scanner Reference

## Architecture

All scanners live in `src/scanners/` and follow this interface:

```python
class BaseScanner:
    name: str           # Scanner identifier
    category: str       # Category (dependencies, config, auth, etc.)
    
    async def scan(self, url: str, config: dict) -> ScanResult:
        """Run the scan and return results."""
```

## Available Scanners

| Scanner | Category | What It Checks |
|---------|----------|----------------|
| `dependency_scanner.py` | dependencies | Known vulnerable dependencies, outdated packages |
| `config_scanner.py` | configuration | DEBUG mode, default credentials, exposed configs |
| `auth_scanner.py` | authentication | Weak auth, missing MFA, session handling |
| `cors_scanner.py` | cors_headers | CORS misconfiguration, missing security headers |
| `secrets_scanner.py` | secrets | Hardcoded API keys, tokens, passwords |
| `ssl_scanner.py` | ssl_tls | SSL certificate validity, TLS version, cipher strength |
| `headers_scanner.py` | security_headers | Missing HSTS, CSP, X-Frame-Options, XSS Protection |

## Adding a New Scanner

1. Create `src/scanners/<name>_scanner.py`:
```python
from src.core.models import Vulnerability, Severity

class CustomScanner:
    name = "custom"
    category = "custom_category"
    
    async def scan(self, url: str, config: dict) -> list[Vulnerability]:
        vulns = []
        # ... scanning logic ...
        return vulns
```

2. Register it in `src/core/engine.py`:
```python
from src.scanners.custom_scanner import CustomScanner

class ScanEngine:
    def __init__(self):
        self.scanners = [
            # ... existing scanners ...
            CustomScanner(),
        ]
```

3. Add it to `enabled_categories` in brand configs to activate it.

## Scan Result Format

```python
@dataclass
class Vulnerability:
    id: str
    title: str
    category: str
    severity: Severity        # CRITICAL, HIGH, MEDIUM, LOW, INFO
    location: str
    description: str
    impact: str
    cvss_score: float
    fix_available: bool
    fix_description: str
    evidence: str
```

## Severity Levels

| Level | Score | Response Time |
|-------|-------|---------------|
| CRITICAL | 9.0-10.0 | 24 hours |
| HIGH | 7.0-8.9 | 1 week |
| MEDIUM | 4.0-6.9 | 1 month |
| LOW | 1.0-3.9 | 3 months |
| INFO | 0.0 | No action required |
