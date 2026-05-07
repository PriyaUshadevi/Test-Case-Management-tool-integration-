import os
import sys
from typing import Any

import requests


API_ENDPOINT = "/rest/api/2/issue"


def build_issue_payload(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Task",
) -> dict[str, Any]:
    return {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
    }


def create_jira_issue(
    jira_url: str,
    email: str,
    api_token: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    response = requests.post(
        f"{jira_url.rstrip('/')}{API_ENDPOINT}",
        auth=(email, api_token),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    payload = build_issue_payload(
        project_key=os.getenv("JIRA_PROJECT_KEY", "QA"),
        summary=os.getenv("JIRA_ISSUE_SUMMARY", "Sample Test Case Integration"),
        description=os.getenv("JIRA_ISSUE_DESCRIPTION", "Created from automation tool"),
        issue_type=os.getenv("JIRA_ISSUE_TYPE", "Task"),
    )

    result = create_jira_issue(
        jira_url=required_env("JIRA_URL"),
        email=required_env("JIRA_EMAIL"),
        api_token=required_env("JIRA_API_TOKEN"),
        payload=payload,
    )
    print(f"Created Jira issue: {result.get('key', result.get('id', 'unknown'))}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
