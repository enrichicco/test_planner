"""
Report generator for creating various output formats.
"""
import json
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template

from ..config import settings


class ReportGenerator:
    """Generates reports in various formats."""

    def __init__(self, template_dir: Optional[str] = None) -> None:
        """
        Initialize report generator.

        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = template_dir or settings.report_template_dir
        self.output_dir = Path(settings.report_output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        try:
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.template_dir), autoescape=True
            )
        except Exception:
            # If templates directory doesn't exist, create basic templates
            self.jinja_env = None

    def generate_json_report(self, report_data: Dict[str, Any], filename: str) -> str:
        """
        Generate JSON report.

        Args:
            report_data: Report data
            filename: Output filename

        Returns:
            Path to generated file
        """
        output_path = self.output_dir / filename
        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        return str(output_path)

    def generate_html_report(
        self,
        report_data: Dict[str, Any],
        filename: str,
        template_name: str = "schedule_report.html",
    ) -> str:
        """
        Generate HTML report.

        Args:
            report_data: Report data
            filename: Output filename
            template_name: Template file name

        Returns:
            Path to generated file
        """
        if self.jinja_env:
            try:
                template = self.jinja_env.get_template(template_name)
                html_content = template.render(**report_data)
            except Exception:
                html_content = self._generate_basic_html(report_data)
        else:
            html_content = self._generate_basic_html(report_data)

        output_path = self.output_dir / filename
        with open(output_path, "w") as f:
            f.write(html_content)
        return str(output_path)

    def _generate_basic_html(self, report_data: Dict[str, Any]) -> str:
        """Generate basic HTML report without template."""
        summary = report_data.get("summary", {})
        person_util = report_data.get("person_utilization", [])
        timeline = report_data.get("task_timeline", [])
        exceptions = report_data.get("exceptions", [])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Schedule Report - {summary.get('schedule_name', 'Unknown')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #333;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .summary-item {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
        .summary-item label {{
            display: block;
            font-weight: bold;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        .summary-item value {{
            display: block;
            font-size: 1.5em;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #007bff;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .badge {{
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .badge-error {{
            background-color: #dc3545;
            color: white;
        }}
        .badge-warning {{
            background-color: #ffc107;
            color: black;
        }}
        .badge-info {{
            background-color: #17a2b8;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Schedule Report: {summary.get('schedule_name', 'Unknown')}</h1>
        <p>Generated: {report_data.get('generated_at', '')}</p>

        <h2>Summary</h2>
        <div class="summary">
            <div class="summary-item">
                <label>Total Tasks</label>
                <value>{summary.get('total_tasks', 0)}</value>
            </div>
            <div class="summary-item">
                <label>Scheduled Tasks</label>
                <value>{summary.get('scheduled_tasks', 0)}</value>
            </div>
            <div class="summary-item">
                <label>Total Duration (hours)</label>
                <value>{summary.get('total_duration_hours', 0)}</value>
            </div>
            <div class="summary-item">
                <label>Makespan (hours)</label>
                <value>{summary.get('makespan_hours', 'N/A')}</value>
            </div>
            <div class="summary-item">
                <label>Total Exceptions</label>
                <value>{summary.get('total_exceptions', 0)}</value>
            </div>
            <div class="summary-item">
                <label>Solve Time (s)</label>
                <value>{summary.get('solve_time_seconds', 'N/A')}</value>
            </div>
        </div>

        <h2>Person Utilization</h2>
        <table>
            <thead>
                <tr>
                    <th>Person</th>
                    <th>Total Tasks</th>
                    <th>Total Hours</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f'''
                <tr>
                    <td>{p.get('person_name', 'Unknown')}</td>
                    <td>{p.get('total_tasks', 0)}</td>
                    <td>{p.get('total_hours', 0)}</td>
                </tr>
                ''' for p in person_util)}
            </tbody>
        </table>

        <h2>Task Timeline</h2>
        <table>
            <thead>
                <tr>
                    <th>Task</th>
                    <th>Person</th>
                    <th>Start</th>
                    <th>End</th>
                    <th>Duration (h)</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f'''
                <tr>
                    <td>{t.get('task_name', 'Unknown')}</td>
                    <td>{t.get('person_name', 'N/A')}</td>
                    <td>{t.get('scheduled_start', 'N/A')}</td>
                    <td>{t.get('scheduled_end', 'N/A')}</td>
                    <td>{t.get('duration_hours', 0)}</td>
                    <td>{t.get('status', 'unknown')}</td>
                </tr>
                ''' for t in timeline)}
            </tbody>
        </table>

        <h2>Exceptions</h2>
        <table>
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Message</th>
                    <th>Task</th>
                    <th>Resolved</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f'''
                <tr>
                    <td>{e.get('type', 'unknown')}</td>
                    <td><span class="badge badge-{e.get('severity', 'info')}">{e.get('severity', 'info')}</span></td>
                    <td>{e.get('message', '')}</td>
                    <td>{e.get('task_name', 'N/A')}</td>
                    <td>{'Yes' if e.get('resolved') else 'No'}</td>
                </tr>
                ''' for e in exceptions)}
            </tbody>
        </table>
    </div>
</body>
</html>
        """
        return html

    def generate_csv_report(self, data: list, filename: str) -> str:
        """
        Generate CSV report.

        Args:
            data: List of dictionaries to export
            filename: Output filename

        Returns:
            Path to generated file
        """
        import csv

        if not data:
            return ""

        output_path = self.output_dir / filename
        with open(output_path, "w", newline="") as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

        return str(output_path)
