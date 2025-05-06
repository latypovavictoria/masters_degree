import json
import os
import sys
from junitparser import TestCase, TestSuite, Error


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
    suite.add_case(score_case)

    for vuln in data.get("vulnerabilities", []):
        vuln_case = TestCase(f"Plugin: {vuln['plugin']}")
        if vuln.get("cvss_score", 0) >= 7:
            vuln_case.result = "failure"
            vuln_case.message = f"{vuln['description']} (CVSS: {vuln['cvss_score']})"
        vuln_case.system_out = json.dumps(vuln, indent=2)
        suite.add_case(vuln_case)

    for secret in data.get("secrets", []):
        secret_case = TestCase("Secrets Detection")
        secret_case.result = "failure"
        secret_case.message = f"Secret found in line {secret['line']}"
        secret_case.system_out = secret["line_content"]
        suite.add_case(secret_case)

    with open("result.xml", "w") as f:
        suite.write(f)
    print("[INFO] JUnit report 'result.xml' generated successfully.")

if __name__ == "__main__":
    create_junit_report()
