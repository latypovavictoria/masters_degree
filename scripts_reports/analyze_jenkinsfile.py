import re
import sys
import json


def analyze_file(filepath):
    issues = []
    cvss_score = 0

    with open(filepath, "r") as f:
        content = f.read()

    if "withCredentials" not in content and re.search(r'["\']?credentials\([^)]+\)', content):
        issues.append("❌ Открытые креды используются без защиты withCredentials")
        cvss_score += 6

    if "triggered by" in content.lower():
        issues.append("⚠️ В Jenkinsfile явно указан ручной запуск")
        cvss_score += 2

    if "checkout" not in content:
        issues.append("⚠️ Отсутствует этап получения кода (checkout)")
        cvss_score += 1

    color = "green"
    if cvss_score >= 9:
        color = "maroon"
    elif cvss_score >= 7:
        color = "red"
    elif cvss_score >= 4:
        color = "orange"

    report = {
        "issues": issues,
        "cvss_score": cvss_score,
        "cvss_color": color
    }

    with open("jenkinsfile_analysis.json", "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    analyze_file(sys.argv[1])
