import datetime
import os
from .logger import logger

class HTMLReporter:
    def __init__(self, report_dir="reports"):
        self.report_dir = report_dir
        self.results = []
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def add_result(self, test_name, status, message="", duration=0):
        self.results.append({
            "name": test_name,
            "status": status,
            "message": message,
            "duration": duration,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def generate_report(self, filename="test_report.html"):
        filepath = os.path.join(self.report_dir, filename)
        
        # Simple HTML template
        html = f"""
        <html>
        <head>
            <title>Test Execution Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #f4f4f4; }}
                .PASS {{ color: green; font-weight: bold; }}
                .FAIL {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Test Execution Report</h1>
            <p>Generated on: {datetime.datetime.now()}</p>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                </tr>
        """
        
        for res in self.results:
            html += f"""
                <tr>
                    <td>{res['name']}</td>
                    <td class="{res['status']}">{res['status']}</td>
                    <td>{res['duration']:.2f}</td>
                    <td>{res['message']}</td>
                    <td>{res['timestamp']}</td>
                </tr>
            """
            
        html += """
            </table>
        </body>
        </html>
        """
        
        try:
            with open(filepath, "w") as f:
                f.write(html)
            logger.info(f"Report: HTML report generated at {filepath}")
        except Exception as e:
            logger.error(f"Report: Failed to generate report: {e}")

# Global reporter instance
reporter = HTMLReporter()
