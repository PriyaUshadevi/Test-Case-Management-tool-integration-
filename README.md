# Test Management Jira Integration

A focused Python project that demonstrates how QA test case data can be converted into Jira issues through the Jira REST API. The project is intentionally small, readable, and testable so recruiters, clients, and engineering reviewers can quickly understand the workflow and extend it for real test management systems.

## Problem Statement

QA teams often manage test cases, execution notes, and defect follow-up in separate tools such as spreadsheets, internal test management systems, and Jira. Manual handoff creates repeated data entry, inconsistent issue descriptions, missed traceability, and delays between test execution and engineering action.

This project solves the core integration problem: take validated test case details, map them to Jira issue fields, and create a Jira issue using secure API token authentication.

## Solution

The integration provides a lightweight Python layer that:

- Builds Jira-compatible issue payloads from test case metadata.
- Reads Jira configuration from environment variables instead of hard-coding secrets.
- Sends issue creation requests to Jira through the REST API.
- Validates required values before making API calls.
- Raises clear errors for missing configuration, invalid payloads, failed HTTP responses, or unexpected Jira responses.
- Includes unit tests for payload creation, API request behavior, validation, and configuration handling.

## Current Scope

This repository contains a working foundation for Jira issue creation. It is suitable for demonstrating integration design, API automation, and testable Python code.

Included:

- Jira issue payload builder.
- Jira REST API issue creation client.
- Environment-based configuration.
- Unit tests with mocked API calls.
- Documentation for setup, configuration, execution, and review.

Not included yet:

- Excel or CSV file parsing.
- Bulk synchronization.
- Jira issue updates.
- Web UI.
- Persistent storage of Jira issue keys.

Those are natural next enhancements, but they are outside the current repository implementation.

## Project Structure

```text
test-management-jira-integration/
  sample-api/
    jira_integration.py        # Jira payload builder and API client
  tests/
    test_jira_integration.py   # Unit tests for integration behavior
  screenshots/
    Jira.png                   # Jira reference screenshot
    workflow.png               # Workflow reference screenshot
  requirements.txt             # Runtime dependency list
  README.md                    # Project documentation
```

## Prerequisites

- Python 3.10 or later.
- A Jira Cloud site, for example `https://your-domain.atlassian.net`.
- A Jira user email address.
- A Jira API token.
- A Jira project key where issues can be created.
- Permission in Jira to create issues in the target project.

## Installation

Clone the repository:

```bash
git clone https://github.com/PriyaUshadevi/test-management-jira-integration.git
cd test-management-jira-integration
```

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Jira Configuration

Set the required environment variables before running the integration.

Windows PowerShell:

```powershell
$env:JIRA_URL = "https://your-domain.atlassian.net"
$env:JIRA_EMAIL = "your-email@example.com"
$env:JIRA_API_TOKEN = "your-api-token"
```

macOS or Linux:

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
```

Optional environment variables:

```bash
JIRA_PROJECT_KEY=QA
JIRA_ISSUE_TYPE=Task
JIRA_ISSUE_SUMMARY=Sample Test Case Integration
JIRA_ISSUE_DESCRIPTION=Created from automation tool
```

Defaults used by the sample when optional values are not provided:

| Variable | Default |
| --- | --- |
| `JIRA_PROJECT_KEY` | `QA` |
| `JIRA_ISSUE_TYPE` | `Task` |
| `JIRA_ISSUE_SUMMARY` | `Sample Test Case Integration` |
| `JIRA_ISSUE_DESCRIPTION` | `Created from automation tool` |

## How To Run

After installing dependencies and setting environment variables, run:

```bash
python sample-api/jira_integration.py
```

Expected successful output:

```text
Created Jira issue: QA-1
```

The actual issue key depends on your Jira project and current issue sequence.

## How To Test

Run the unit test suite:

```bash
python -m unittest discover -s tests -v
```

The tests use mocks for the Jira API call, so they do not create real Jira issues and do not require live Jira credentials.

## Workflow

1. A QA user or test management source provides test case information.
2. The integration validates required values.
3. Test case fields are mapped into a Jira issue payload.
4. The Jira REST API is called with email and API token authentication.
5. Jira creates an issue and returns an issue key.
6. The issue key can be stored by a future synchronization layer for traceability.

## Main Module Details

`sample-api/jira_integration.py` contains the integration logic.

| Function | Purpose |
| --- | --- |
| `build_issue_payload()` | Creates the Jira issue JSON payload from project key, summary, description, and issue type. |
| `create_jira_issue()` | Sends the payload to Jira and returns the JSON response. |
| `required_env()` | Reads and validates mandatory environment variables. |
| `main()` | Builds the sample payload, reads configuration, creates the issue, and prints the result. |

## Error Handling

The project handles common failure cases:

- Missing required environment variables.
- Blank required values.
- Empty Jira payloads.
- HTTP errors returned by Jira.
- Unexpected non-object JSON responses from Jira.

Credential values are never stored in the repository.

## Security Notes

- Do not commit Jira API tokens.
- Prefer environment variables or a secret manager for credentials.
- Rotate the Jira API token if it is ever exposed.
- Use least-privilege Jira permissions for demo or automation users.

## Recruiter And Client Summary

This project demonstrates:

- API integration with Jira Cloud.
- Secure configuration through environment variables.
- Clean Python functions with typed return structures.
- Unit testing with mocked external dependencies.
- Practical QA workflow automation.
- Documentation suitable for handoff and project review.

## Roadmap

Recommended next improvements:

- Add CSV or Excel import for bulk test case creation.
- Add duplicate detection before creating Jira issues.
- Store created Jira issue keys for traceability.
- Add support for execution result updates.
- Add GitHub Actions CI to run tests automatically.
- Package the code as an installable Python module.

## Current Project Status

Status: Working foundation.

The local unit test suite passes, and the implementation is in good working condition for the current documented scope: creating a Jira issue from configured test case data. A live Jira smoke test still requires valid Jira credentials and create-issue permission in the target Jira project.
