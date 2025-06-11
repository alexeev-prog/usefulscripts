import os
import subprocess
import sys
import re
from datetime import datetime
from typing import List, Dict, Any


class CppAnalyzer:

    MAX_LINE_LENGTH: int = 120
    IGNORED_DIRECTORIES: List[str] = ['build', 'docs', 'npm-packages']

    FUNCTION_GUIDELINES: Dict[str, str] = {
        'malloc': 'https://en.cppreference.com/w/c/memory/malloc',
        'free': 'https://en.cppreference.com/w/c/memory/free',
        'strcpy': 'https://en.cppreference.com/w/c/string/byte/strcpy',
        'strcat': 'https://en.cppreference.com/w/c/string/byte/strcat',
        'sprintf': 'https://en.cppreference.com/w/c/string/byte/sprintf',
        'gets': 'https://en.cppreference.com/w/c/string/byte/gets',
        'strcmp': 'https://en.cppreference.com/w/c/string/byte/strcmp',
        'strncpy': 'https://en.cppreference.com/w/c/string/byte/strncpy',
        'snprintf': 'https://en.cppreference.com/w/c/string/byte/snprintf',
        'cout': 'https://en.cppreference.com/w/cpp/io/basic_ostream/operator_lt_lt',
        'cin': 'https://en.cppreference.com/w/cpp/io/basic_istream/operator_gt_gt',
        # Add more functions as needed
    }

    def __init__(self, repo_path: str) -> None:
        self.repo_path = os.path.abspath(repo_path)
        self.reports: List[Dict[str, Any]] = []
        self.modified_files: List[str] = self.get_modified_files()
        self.setup_console()

    def setup_console(self) -> None:
        print("\033[1;36m=============================\033[0m")  # Cyan
        print("\033[1;32m C++ Code Analyzer Initialized \033[0m")  # Green
        print("\033[1;36m=============================\033[0m")  # Cyan

    def get_modified_files(self) -> List[str]:
        print("\033[1;33mChecking for modified C++ files in the repository...\033[0m")  # Yellow
        os.chdir(self.repo_path)
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        modified_files = [file for file in result.stdout.splitlines() if self.is_cpp_file(file)]
        print(f"\033[1;32mFound {len(modified_files)} modified C++ files.\033[0m")  # Green
        return modified_files

    def is_cpp_file(self, filename: str) -> bool:
        return filename.endswith(('.cpp', '.h', '.hpp'))

    def format_file(self, file_path: str) -> None:
        subprocess.run(['clang-format', '-i', file_path], check=True)

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        report = {
            'file_path': file_path,
            'file_size': self.get_file_size(file_path),
            'description': self.get_file_description(file_path),
            'line_count': 0,
            'class_count': 0,
            'function_count': 0,
            'variable_count': 0,
            'includes': [],
            'long_lines': [],
            'memory_issues': [],
            'legacy_issues': [],
            'clang_tidy_warnings': [],
            'used_libraries': [],
            'error': None
        }

        try:
            print(f"\033[1;34mAnalyzing file: {file_path}...\033[0m")  # Blue
            with open(file_path, 'r') as f:
                for line_number, line in enumerate(f, start=1):
                    line = line.strip()
                    report['line_count'] += 1  # Update line count

                    if len(line) > self.MAX_LINE_LENGTH:
                        report['long_lines'].append(f"Line {line_number}: exceeds {self.MAX_LINE_LENGTH} characters.")

                    report['memory_issues'] += self.analyze_memory_usage(line, line_number)
                    report['legacy_issues'] += self.analyze_legacy_code(line, line_number)

                    if '#include' in line:
                        report['includes'].append(line)
                        library = line.split('"')[1] if '"' in line else line.split('<')[1].split('>')[0]
                        report['used_libraries'].append(library)

                    # Counting classes, functions, and variables
                    if re.search(r'\bclass\s+\w+', line):
                        report['class_count'] += 1
                    elif re.search(r'\b\w+\s*\([^)]*\)\s*{', line):
                        report['function_count'] += 1
                    elif re.search(r'\b\w+\s*;', line):
                        report['variable_count'] += 1

                    # Check for function calls and add links
                    for func, link in self.FUNCTION_GUIDELINES.items():
                        if func in line:
                            report['memory_issues'].append(f"Line {line_number}: '{func}' is called. Refer to {link}")

            # Running clang-tidy for static analysis
            result = subprocess.run(
                ['clang-tidy', file_path, '--'],
                capture_output=True,
                text=True,
                check=True
            )
            report['clang_tidy_warnings'] = self.extract_warnings(result.stdout + result.stderr)

            return report

        except Exception as e:
            print(f"\033[1;31mError analyzing file {file_path}: {e}\033[0m")  # Red
            report['error'] = str(e)  # Capture the error message
            return report

    def get_file_size(self, file_path: str) -> str:
        """Get file size in a human-readable format."""
        size = os.path.getsize(file_path)
        return f"{size / 1024:.2f} KB"  # Convert to KB

    def get_file_description(self, file_path: str) -> str:
        """Get a brief description of the file."""
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
        return first_line if first_line else "No description available."

    def analyze_memory_usage(self, line: str, line_number: int) -> List[str]:
        issues = []
        memory_patterns = [
            (r'\b(malloc|calloc|realloc|free)\b', f"Line {line_number}: Use of C memory management function '{line.strip()}' detected. Consider using C++ smart pointers.")
        ]

        for pattern, message in memory_patterns:
            if re.search(pattern, line):
                issues.append(message)

        return issues

    def analyze_legacy_code(self, line: str, line_number: int) -> List[str]:
        issues = []
        legacy_patterns = [
            (r'\b(strcpy|strcat|sprintf|gets|gets_s|strncat)\b', f"Line {line_number}: Use of legacy C function '{line.strip()}'. Consider using safer alternatives like 'strncpy' or 'snprintf'.")
        ]

        for pattern, message in legacy_patterns:
            if re.search(pattern, line):
                issues.append(message)

        return issues

    def extract_warnings(self, output: str) -> List[str]:
        return [line for line in output.splitlines() if "warning" in line or "error" in line]

    def analyze_dependencies(self) -> List[str]:
        print("\033[1;34mAnalyzing dependencies...\033[0m")  # Blue

        dependency_warnings = []
        for file_path in self.modified_files:
            includes = self.find_includes(file_path)
            for included in includes:
                if not os.path.exists(included):
                    dependency_warnings.append(f"File {file_path} includes a non-existent file: {included}")
        return dependency_warnings

    def find_includes(self, file_path: str) -> List[str]:
        includes = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    match = re.match(r'#include\s+"(.+)"', line) or re.match(r'#include\s+<(.+)>', line)
                    if match:
                        includes.append(match.group(1))
        except Exception as e:
            print(f"\033[1;31mCould not read file {file_path}: {e}\033[0m")  # Red
        return includes

    def analyze_directory(self) -> None:
        print("\033[1;34mAnalyzing all C++ files in the repository...\033[0m")  # Blue
        for root, dirs, files in os.walk(self.repo_path):
            # Ignore specified directories
            dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRECTORIES]
            for file in files:
                if self.is_cpp_file(file):
                    file_path = os.path.join(root, file)
                    self.format_file(file_path)
                    report = self.analyze_file(file_path)
                    self.reports.append(report)

    def repository_information(self) -> str:
        """Retrieve and format information about the repository."""
        repo_info = f"""
        <h2>Repository Information</h2>
        <p><strong>Repository Path:</strong> {self.repo_path}</p>
        <p><strong>Modified Files:</strong> {', '.join(self.modified_files) if self.modified_files else 'None'}</p>
        <p><strong>Analysis Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        return repo_info

    def generate_report(self, output_file: str) -> None:
        # Add summary statistics
        html_content = self.create_html_report()
        with open(output_file, 'w') as f:
            f.write(html_content)
        print(f"\033[1;32mGenerated report: {output_file}\033[0m")  # Green

    def create_html_report(self) -> str:
        report_header = "<h1 style='color: #00ff99;'>C++ Code Analysis Report</h1>"
        report_date = f"<p style='color: #999;'>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        repository_info = self.repository_information()
        summary = self.create_summary()

        report_body = ""
        for report in self.reports:
            file_path = report['file_path']
            report_body += f"<div style='border: 1px solid #444; background-color: #232323; padding: 15px; margin: 15px 0; border-radius: 5px;'>"
            report_body += f"<h2 style='color: #00ff99;'><a href='{file_path}' style='color: #00ff99; text-decoration: none;'>{os.path.basename(file_path)}</a></h2>"
            report_body += f"<p style='color: #ccc;'><strong>Description:</strong> {report['description']}</p>"
            report_body += f"<p style='color: #ccc;'><strong>File Size:</strong> {report['file_size']}</p>"

            report_body += "<div style='color: #ccc; margin-bottom: 10px;'>"
            report_body += "<h4>File Statistics</h4>"
            report_body += f"<p><strong>Lines of Code:</strong> {report.get('line_count', 0)}</p>"
            report_body += f"<p><strong>Classes:</strong> {report.get('class_count', 0)}</p>"
            report_body += f"<p><strong>Functions:</strong> {report.get('function_count', 0)}</p>"

            report_body += f"<p><strong>Variables:</strong> {report.get('variable_count', 0)}</p>"
            report_body += f"<p><strong>Used Libraries:</strong> {', '.join(report.get('used_libraries', []))}</p>"
            report_body += f"<p><strong>Includes:</strong> {len(report.get('includes', []))}</p>"
            report_body += "</div>"

            if 'error' in report:
                report_body += f"<pre style='color: #ff4d4d; background-color: #350000; padding: 10px; border-radius: 5px;'>Error: {report['error']}</pre>"

            # Long lines section
            if report['long_lines']:
                report_body += "<div style='background-color: #454545; padding: 10px; border-radius: 5px; margin-top: 10px;'>"
                report_body += "<h4 style='color: #ffcc00;'>Long Lines Detected:</h4><ul>"
                for long_line in report['long_lines']:
                    report_body += f"<li>{long_line}</li>"
                report_body += "</ul></div>"

            # Memory issues
            if report['memory_issues']:
                report_body += "<div style='background-color: #454545; padding: 10px; border-radius: 5px; margin-top: 10px;'>"
                report_body += "<h4 style='color: #ffcc00;'>Memory Management Issues Detected:</h4><ul>"
                for issue in report['memory_issues']:
                    report_body += f"<li>{issue}</li>"
                report_body += "</ul></div>"

            # Legacy issues
            if report['legacy_issues']:
                report_body += "<div style='background-color: #454545; padding: 10px; border-radius: 5px; margin-top: 10px;'>"
                report_body += "<h4 style='color: #ffcc00;'>Legacy Code Issues Detected:</h4><ul>"
                for issue in report['legacy_issues']:
                    report_body += f"<li>{issue}</li>"
                report_body += "</ul></div>"

            # Clang-tidy warnings
            if report['clang_tidy_warnings']:
                report_body += "<div style='background-color: #454545; padding: 10px; border-radius: 5px; margin-top: 10px;'>"
                report_body += "<h4 style='color: #ffcc00;'>Clang-tidy Warnings:</h4><ul>"
                for warning in report['clang_tidy_warnings']:
                    report_body += f"<li>{warning}</li>"
                report_body += "</ul></div>"

            report_body += "</div>"  # Closing the main report block

        return f"""
        <html style="background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; line-height: 1.6;">
        <head><title>C++ Code Analysis Report</title></head>
        <body>
        {report_header}
        {report_date}
        {repository_info}
        {summary}
        <div>{report_body}</div>
        </body>
        </html>
        """

    def create_summary(self) -> str:
        total_files = len(self.reports)
        total_lines = sum(report.get('line_count', 0) for report in self.reports)
        total_warnings = sum(len(report.get('clang_tidy_warnings', [])) for report in self.reports)
        total_memory_issues = sum(len(report.get('memory_issues', [])) for report in self.reports)
        total_legacy_issues = sum(len(report.get('legacy_issues', [])) for report in self.reports)

        summary = f"""
        <div style='background-color: #232323; border: 1px solid #444; padding: 15px; margin: 15px 0; border-radius: 5px;'>
            <h2 style='color: #00ff99;'>Summary</h2>
            <p><strong>Total Files Analyzed:</strong> {total_files}</p>
            <p><strong>Total Lines of Code:</strong> {total_lines}</p>
            <p><strong>Total Clang-tidy Warnings:</strong> {total_warnings}</p>

            <p><strong>Total Memory Management Issues:</strong> {total_memory_issues}</p>
            <p><strong>Total Legacy Code Issues:</strong> {total_legacy_issues}</p>
        </div>
        """
        return summary

    def run_analysis(self) -> None:
        print("\033[1;33mStarting analysis...\033[0m")  # Yellow
        self.analyze_directory()
        self.generate_report('report.html')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_cpp_code.py <path_to_git_repository>")
        sys.exit(1)

    repo_path = sys.argv[1]
    analyzer = CppAnalyzer(repo_path)
    analyzer.run_analysis()
