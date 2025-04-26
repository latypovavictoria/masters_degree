import requests
import json
import sys

def get_jenkins_config(base_url, username, token):
    api_url = f"{base_url}/api/json"
    try:
        response = requests.get(api_url, auth=(username, token), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Jenkins: {e}")
        sys.exit(1)

def run_security_checks(config):
    results = []

    # Базовые проверки
    # 1. Проверка включения анонимного доступа
    if config.get('useSecurity', False):
        results.append({"check": "Security Realm Configured", "result": "PASS"})
    else:
        results.append({"check": "Security Realm Configured", "result": "FAIL"})

    # 2. Проверка, отключен ли CLI через ремоут
    if config.get('cli', {}).get('enabled', True):
        results.append({"check": "CLI Over Remoting Disabled", "result": "FAIL"})
    else:
        results.append({"check": "CLI Over Remoting Disabled", "result": "PASS"})

    # 3. Проверка на анонимный доступ
    if config.get('authorizationStrategy', {}).get('allowAnonymousRead', False):
        results.append({"check": "Anonymous Read Access", "result": "FAIL"})
    else:
        results.append({"check": "Anonymous Read Access", "result": "PASS"})

    return results

def save_report(results, filename="security_report.json"):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Security report saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python security_check.py <jenkins_url> <username> <token>")
        sys.exit(1)

    base_url = sys.argv[1]
    username = sys.argv[2]
    token = sys.argv[3]

    config = get_jenkins_config(base_url, username, token)
    check_results = run_security_checks(config)
    save_report(check_results)
