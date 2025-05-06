import requests
import time
import json
import sys
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
MAX_RETRIES = 3
RETRY_DELAY = 5


def fetch_plugins(base_url, user, token):
    url = f"{base_url}/pluginManager/api/json?depth=1"
    response = requests.get(url, auth=HTTPBasicAuth(user, token), verify=False)
    response.raise_for_status()
    return response.json()['plugins']


def fetch_cves(plugin_name, version, apikey):
    query = f"{plugin_name} {version}"
    params = {
        "keywordSearch": query,
        "resultsPerPage": 10
    }

    headers = {"User-Agent": "Jenkins CVE Checker"}
    if apikey:
        headers["apiKey"] = apikey

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(NVD_API_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "id": item["cve"]["id"],
                    "description": next(
                        (desc["value"] for desc in item["cve"]["descriptions"] if desc["lang"] == "en"),
                        "No description"
                    ),
                    "cvss": item.get("cve", {}).get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData",
                                                                                                     {}).get(
                        "baseScore", "N/A"),
                    "severity": item.get("cve", {}).get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData",
                                                                                                         {}).get(
                        "baseSeverity", "UNKNOWN")
                }
                for item in data.get("vulnerabilities", [])
            ]
        except requests.RequestException as e:
            print(f"Error fetching CVEs for {plugin_name}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                return []


def check_plugins(plugins, apikey):
    results = []
    for plugin in plugins:
        name = plugin['shortName']
        version = plugin['version']
        print(f"Checking CVEs for {name} {version}...")
        cves = fetch_cves(name, version, apikey)
        results.append({
            "plugin": name,
            "version": version,
            "vulnerable": bool(cves),
            "cves": cves
        })
    return results


def save_junit_xml(results, output_path):
    testsuite = ET.Element("testsuite", name="Jenkins Plugin CVE Report", tests=str(len(results)))
    for plugin in results:
        plugin_name = f"{plugin['plugin']}:{plugin['version']}"
        testcase = ET.SubElement(
            testsuite,
            "testcase",
            classname="JenkinsPluginAudit",
            name=plugin_name
        )

        if plugin["vulnerable"]:
            failure = ET.SubElement(
                testcase,
                "failure",
                message=f"{len(plugin['cves'])} CVEs found"
            )

            details_lines = []
            for cve in plugin["cves"]:
                line = (
                    f"{cve['id']} | CVSS: {cve['cvss']} | Severity: {cve['severity']}\n"
                    f"{cve['description']}\n"
                )
                details_lines.append(line)

            failure.text = "\n".join(details_lines)

    tree = ET.ElementTree(testsuite)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    base_url, user, token, apikey = sys.argv[1:5]

    plugins = fetch_plugins(base_url, user, token)
    results = check_plugins(plugins, apikey)

    with open("plugin_vuln_report.json", "w") as f:
        json.dump(results, f, indent=2)

    save_junit_xml(results, "plugin_vuln_report.xml")

    print("CVE check completed. Reports saved:")
    print("  - plugin_vuln_report.json")
    print("  - plugin_vuln_report.xml (for Allure)")
