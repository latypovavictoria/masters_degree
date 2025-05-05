import requests
import time
import json
import sys
from requests.auth import HTTPBasicAuth

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Максимальное количество попыток для получения CVE
MAX_RETRIES = 3
RETRY_DELAY = 5  # задержка между попытками в секундах


def fetch_plugins(base_url, user, token):
    """Получаем список плагинов из Jenkins."""
    url = f"{base_url}/pluginManager/api/json?depth=1"
    response = requests.get(url, auth=HTTPBasicAuth(user, token), verify=False)
    response.raise_for_status()
    return response.json()['plugins']


def fetch_cves(plugin_name, version, apikey):
    """Получаем CVEs для плагина из NVD API."""
    query = f"{plugin_name} {version}"
    params = {
        "keywordSearch": query,
        "resultsPerPage": 10
    }

    headers = {
        "User-Agent": "Jenkins CVE Checker",
    }
    if apikey:
        headers["apiKey"] = apikey

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(NVD_API_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            cves = [item["cve"]["id"] for item in data.get("vulnerabilities", [])]
            return cves
        except requests.RequestException as e:
            print(f"Error fetching CVEs for {plugin_name}: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed to fetch CVEs for {plugin_name} after {MAX_RETRIES} attempts.")
                return []


def check_plugins(plugins, apikey):
    """Проверяем все плагины на наличие CVE."""
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


if __name__ == "__main__":
    base_url, user, token, apikey = sys.argv[1:5]

    plugins = fetch_plugins(base_url, user, token)

    results = check_plugins(plugins, apikey)

    with open("plugin_vuln_report.json", "w") as f:
        json.dump(results, f, indent=2)

    print("CVE check completed and results saved to plugin_vuln_report.json")
