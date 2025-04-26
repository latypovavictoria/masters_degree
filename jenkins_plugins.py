import argparse
import requests
from requests.auth import HTTPBasicAuth


def get_plugins(base_url, user, token):
    url = f"{base_url}/pluginManager/api/json?depth=1"
    response = requests.get(url, auth=HTTPBasicAuth(user, token), verify=False)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Jenkins plugins list.")
    parser.add_argument("--url", required=True, help="Base URL of Jenkins server (e.g., https://your-jenkins-url)")
    parser.add_argument("--user", required=True, help="Jenkins username")
    parser.add_argument("--token", required=True, help="Jenkins API token or password")

    args = parser.parse_args()

    plugins_info = get_plugins(args.url, args.user, args.token)

    for plugin in plugins_info.get('plugins', []):
        print(f"{plugin['longName']} (shortName: {plugin['shortName']}, version: {plugin['version']})")
