# Test Case Management Jira Integration

This repository demonstrates how a test case management workflow can create Jira issues through the Jira REST API.

## Overview

The sample integration prepares a Jira issue payload from test case data and sends it to Jira using API token authentication. It is designed as a starting point for synchronizing test cases, execution results, and traceability data from a test management source such as an Excel workbook or internal QA tool.

## Features

- Build Jira issue payloads from test case metadata.
- Create Jira issues through the Jira REST API.
- Configure Jira connection details through environment variables.
- Keep credentials out of source control.

## Project Structure

```text
sample-api/
  jira_integration.py
tests/
  test_jira_integration.py
requirements.txt
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the required Jira environment variables:

```bash
set JIRA_URL=https://your-domain.atlassian.net
set JIRA_EMAIL=your-email@example.com
set JIRA_API_TOKEN=your-api-token
```

Optional values:

```bash
set JIRA_PROJECT_KEY=QA
set JIRA_ISSUE_TYPE=Task
set JIRA_ISSUE_SUMMARY=Sample Test Case Integration
set JIRA_ISSUE_DESCRIPTION=Created from automation tool
```

Run the sample integration:

```bash
python sample-api/jira_integration.py
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Sample Workflow

1. QA user prepares test cases.
2. Tool validates required fields.
3. Integration layer maps test case fields to Jira fields.
4. Jira issue is created through the API.
5. Jira issue key is stored for traceability.
