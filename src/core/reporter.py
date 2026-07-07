"""
SaaS-Security-Auditor — Report Engine

Generates Markdown, JSON, and HTML reports from ScanResults.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from src.core.models import ScanResult, Severity


class ReportEngine:
    """Generates output reports in multiple formats."""

    @staticmethod
    def generate_markdown(result: ScanResult, output_path: Optional[Path] = None) -> str:
        lines = [
            f"# Security Scan Report: {result.brand}",
            f"",
            f"**Scan ID:** {result.scan_id}",
            f"**Started:** {result.started_at}",
            f"**Completed:** {result.completed_at or 'N/A'}",
            f"**Duration:** {result.duration_seconds:.1f}s" if result.duration_seconds else "",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Vulnerabilities | {len(result.vulnerabilities)} |",
            f"| Checks Run | {result.total_checks} |",
            f"| Passed | {result.passed_checks} |",
            f"| Failed | {result.failed_checks} |",
            f"",
        ]

        if result.vulnerabilities:
            lines.append("## Vulnerabilities")
            lines.append("")
            for i, v in enumerate(result.vulnerabilities, 1):
                sev_icon = {"critical": "!!", "high": "! ", "medium": "- ", "low": "  ", "info": "  "}
                icon = sev_icon.get(v.severity.value, "  ")
                lines.append(f"### {i}. [{v.severity.value.upper()}] {v.title}")
                lines.append(f"")
                lines.append(f"- **Category:** {v.category.value}")
                lines.append(f"- **Location:** `{v.location}`")
                lines.append(f"- **CVSS:** {v.cvss_score or 'N/A'}")
                lines.append(f"- **CVE:** {v.cve_id or 'N/A'}")
                lines.append(f"")
                lines.append(f"**Description:**")
                lines.append(f"{v.description}")
                lines.append(f"")
                lines.append(f"**Remediation:**")
                lines.append(f"{v.remediation}")
                if v.evidence:
                    lines.append(f"")
                    lines.append(f"**Evidence:**")
                    lines.append(f"```")
                    lines.append(v.evidence[:500])
                    lines.append(f"```")
                lines.append(f"")
                lines.append(f"**Fix Status:** {v.fix_status.value}")
                lines.append(f"")
                lines.append("---")
                lines.append("")

        report = "\n".join(lines)
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report, encoding="utf-8")
        return report

    @staticmethod
    def generate_json(result: ScanResult, output_path: Optional[Path] = None) -> str:
        import json
        data = result.to_dict()
        text = json.dumps(data, indent=2, ensure_ascii=False)
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding="utf-8")
        return text

    @staticmethod
    def generate_html(result: ScanResult, output_path: Optional[Path] = None) -> str:
        by_sev: dict[str, list] = {"critical": [], "high": [], "medium": [], "low": [], "info": []}
        for v in result.vulnerabilities:
            by_sev.setdefault(v.severity.value, []).append(v)

        vuln_rows = ""
        for v in result.vulnerabilities:
            color = {"critical": "#dc3545", "high": "#fd7e14", "medium": "#ffc107",
                      "low": "#28a745", "info": "#17a2b8"}
            c = color.get(v.severity.value, "#6c757d")
            vuln_rows += f"""
            <tr>
                <td><span style="background:{c};color:#fff;padding:2px 8px;border-radius:4px">{v.severity.value.upper()}</span></td>
                <td>{v.title}</td>
                <td>{v.category.value}</td>
                <td><code>{v.location}</code></td>
                <td>{v.fix_status.value}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Security Scan Report — {result.brand}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f8f9fa; }}
        h1, h2, h3 {{ color: #212529; }}
        table {{ border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #dee2e6; }}
        th {{ background: #343a40; color: #fff; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 20px 0; }}
        .card {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }}
        .card .num {{ font-size: 2em; font-weight: bold; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; color: #fff; font-size: 0.8em; }}
    </style>
</head>
<body>
    <h1>Security Scan Report</h1>
    <h2>{result.brand}</h2>
    <p><strong>Scan ID:</strong> {result.scan_id} | <strong>Duration:</strong> {result.duration_seconds:.1f}s</p>

    <div class="summary">
        <div class="card"><div class="num" style="color:#dc3545">{len(result.vulnerabilities)}</div><div>Vulnerabilities</div></div>
        <div class="card"><div class="num" style="color:#28a745">{result.passed_checks}</div><div>Checks Passed</div></div>
        <div class="card"><div class="num" style="color:#6c757d">{result.total_checks}</div><div>Total Checks</div></div>
    </div>

    <h3>Vulnerabilities by Severity</h3>
    <table>
        <thead><tr><th>Severity</th><th>Title</th><th>Category</th><th>Location</th><th>Fix Status</th></tr></thead>
        <tbody>{vuln_rows}</tbody>
    </table>

    <p style="margin-top:20px;color:#6c757d;font-size:0.9em;">
        Generated by SaaS-Security-Auditor on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </p>
</body>
</html>"""
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")
        return html
