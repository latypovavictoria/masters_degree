import json
from junit_xml import TestSuite, TestCase


def create_junit_report():
    test_cases = []

    with open("plugin_vuln_report.json") as f:
        plugin_data = json.load(f)
        for plugin in plugin_data:
            tc = TestCase(f"Plugin: {plugin['plugin']}", "PluginCVECheck")
            if plugin["vulnerable"]:
                tc.add_failure_info(f"CVE found: {plugin['cves']}")
            test_cases.append(tc)

    with open("jenkinsfile_analysis.json") as f:
        jenkinsfile_data = json.load(f)
        for issue in jenkinsfile_data["issues"]:
            tc = TestCase("Jenkinsfile Issue", "JenkinsfileStaticCheck")
            tc.add_failure_info(issue)
            test_cases.append(tc)

        score_case = TestCase("CVSS Score", "SecurityScore")
        score_case.add_stdout(f"CVSS Score: {jenkinsfile_data['cvss_score']} ({jenkinsfile_data['cvss_color']})")
        test_cases.append(score_case)

    ts = TestSuite("Security Report", test_cases)
    with open("security_result.xml", "w") as f:
        TestSuite.to_file(f, [ts], prettyprint=True)


if __name__ == "__main__":
    create_junit_report()
