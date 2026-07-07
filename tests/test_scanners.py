"""
Tests for SaaS-Security-Auditor scanners.
"""

from __future__ import annotations

import pytest

from src.core.engine import ScanEngine, ScannerConfig
from src.core.models import ScanCategory, Severity


class TestDependencyScanner:
    """Requires a real source directory. See test_scanners_integration.py for full tests."""

    def test_imports_ok(self):
        from src.scanners.dependency import DependencyScanner
        s = DependencyScanner()
        assert s.category == ScanCategory.DEPENDENCIES


class TestConfigScanner:
    def test_imports_ok(self):
        from src.scanners.config import ConfigScanner
        s = ConfigScanner()
        assert s.category == ScanCategory.CONFIGURATION


class TestSecretsScanner:
    def test_imports_ok(self):
        from src.scanners.secrets import SecretsScanner
        s = SecretsScanner()
        assert s.category == ScanCategory.SECRETS


class TestModels:
    def test_vulnerability_to_dict(self):
        from src.core.models import Vulnerability, Severity, ScanCategory
        v = Vulnerability(
            id="test123",
            category=ScanCategory.DEPENDENCIES,
            severity=Severity.HIGH,
            title="Test vuln",
            description="Test description",
            location="test/file.py:42",
            remediation="Fix it",
            fixable=True,
        )
        d = v.to_dict()
        assert d["id"] == "test123"
        assert d["severity"] == "high"
        assert d["category"] == "dependencies"
        assert d["fixable"] is True

    def test_scan_result_summary(self):
        from src.core.models import ScanResult, Vulnerability, Severity, ScanCategory
        result = ScanResult(brand="test", scan_id="s1", started_at="now")
        result.vulnerabilities = [
            Vulnerability(id="1", category=ScanCategory.DEPENDENCIES, severity=Severity.CRITICAL,
                          title="T1", description="D1", location="L1", remediation="R1"),
            Vulnerability(id="2", category=ScanCategory.SECRETS, severity=Severity.HIGH,
                          title="T2", description="D2", location="L2", remediation="R2"),
        ]
        result.total_checks = 10
        result.passed_checks = 8
        result.failed_checks = 2
        summary = result.summary
        assert "test" in summary
        assert "critical=1" in summary or "CRITICAL=1" in summary

    def test_severity_enum_values(self):
        assert Severity.CRITICAL.value == "critical"
        assert Severity.HIGH.value == "high"
        assert Severity.LOW.value == "low"


class TestFixerModels:
    def test_fix_result_to_dict(self):
        from src.core.models import FixResult, FixStatus
        fr = FixResult(
            vulnerability_id="v1",
            fix_status=FixStatus.AUTO_FIXED,
            description="Fixed it",
            diff="--- a\n+++ b\n",
        )
        d = fr.to_dict()
        assert d["vulnerability_id"] == "v1"
        assert d["fix_status"] == "auto_fixed"
