import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "sample-api" / "jira_integration.py"
SPEC = importlib.util.spec_from_file_location("jira_integration", MODULE_PATH)
jira_integration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(jira_integration)


class JiraIntegrationTests(unittest.TestCase):
    def test_build_issue_payload_uses_jira_fields(self):
        payload = jira_integration.build_issue_payload(
            project_key="QA",
            summary="Login test",
            description="Validate successful login",
            issue_type="Task",
        )

        self.assertEqual(
            payload,
            {
                "fields": {
                    "project": {"key": "QA"},
                    "summary": "Login test",
                    "description": "Validate successful login",
                    "issuetype": {"name": "Task"},
                }
            },
        )

    def test_create_jira_issue_posts_json_payload(self):
        response = Mock()
        response.json.return_value = {"key": "QA-1"}

        with patch.object(jira_integration.requests, "post", return_value=response) as post:
            result = jira_integration.create_jira_issue(
                jira_url="https://example.atlassian.net/",
                email="qa@example.com",
                api_token="token",
                payload={"fields": {"summary": "Login test"}},
            )

        post.assert_called_once_with(
            "https://example.atlassian.net/rest/api/2/issue",
            auth=("qa@example.com", "token"),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={"fields": {"summary": "Login test"}},
            timeout=30,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, {"key": "QA-1"})

    def test_build_issue_payload_rejects_empty_required_fields(self):
        with self.assertRaisesRegex(ValueError, "summary must not be empty"):
            jira_integration.build_issue_payload(
                project_key="QA",
                summary=" ",
                description="Validate successful login",
            )

    def test_create_jira_issue_rejects_empty_payload(self):
        with self.assertRaisesRegex(ValueError, "payload must not be empty"):
            jira_integration.create_jira_issue(
                jira_url="https://example.atlassian.net",
                email="qa@example.com",
                api_token="token",
                payload={},
            )

    def test_create_jira_issue_rejects_unexpected_json_response(self):
        response = Mock()
        response.json.return_value = ["QA-1"]

        with patch.object(jira_integration.requests, "post", return_value=response):
            with self.assertRaisesRegex(
                RuntimeError,
                "Jira API returned an unexpected response",
            ):
                jira_integration.create_jira_issue(
                    jira_url="https://example.atlassian.net",
                    email="qa@example.com",
                    api_token="token",
                    payload={"fields": {"summary": "Login test"}},
                )

        response.raise_for_status.assert_called_once_with()

    def test_required_env_raises_clear_error_when_missing(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(
                RuntimeError,
                "Missing required environment variable: JIRA_URL",
            ):
                jira_integration.required_env("JIRA_URL")

    def test_required_env_trims_configured_value(self):
        with patch.dict("os.environ", {"JIRA_URL": " https://example.atlassian.net "}):
            self.assertEqual(
                jira_integration.required_env("JIRA_URL"),
                "https://example.atlassian.net",
            )


if __name__ == "__main__":
    unittest.main()
