import json
import os
import sys
from junitparser import TestCase, TestSuite, Failure


def load_analysis_results(filepath="jenkinsfile_analysis.json"):
    if not os.path.exists(filepath):
        print(f"[ERROR] File '{filepath}' not found.")
        sys.exit(1)
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        sys.exit(1)


def create_junit_report():
    data = load_analysis_results()

    suite = TestSuite("Jenkinsfile Security Analysis")

    score_case = TestCase("CVSS Score Analysis")
    score = data.get("cvss_score", "N/A")
    color = data.get("cvss_color", "N/A")
    score_case.system_out = f"CVSS Score: {score} ({color})"
    suite.add_testcase(score_case)

    for vuln in data.get("vulnerabilities", []):
        vuln_case = TestCase(f"Plugin: {vuln['plugin']}")
        if vuln.get("cvss_score", 0) >= 7:
            message = f"{vuln['description']} (CVSS: {vuln['cvss_score']})"
            vuln_case.add_failure_info(message=message)
        vuln_case.system_out = json.dumps(vuln, indent=2)
        suite.add_testcase(vuln_case)

    for secret in data.get("secrets", []):
        secret_case = TestCase("Secrets Detection")
        message = f"Secret found in line {secret['line']}"
        secret_case.add_failure_info(message=message)
        secret_case.system_out = secret["line_content"]
        suite.add_testcase(secret_case)

    suite.write("result.xml")
    print("[INFO] JUnit report 'result.xml' generated successfully.")


if __name__ == "__main__":
    create_junit_report()
