import requests

JIRA_URL = "https://your-domain.atlassian.net"
API_ENDPOINT = "/rest/api/2/issue"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "fields": {
        "project": {
            "key": "QA"
        },
        "summary": "Sample Test Case Integration",
        "description": "Created from automation tool",
        "issuetype": {
            "name": "Task"
        }
    }
}

print("Sample Jira integration payload prepared.")