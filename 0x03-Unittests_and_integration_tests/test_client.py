#!/usr/bin/env python3
"""
Unittests and integration tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from utils import get_json
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org property returns correct org"""
        expected = {"login": org_name, "id": 1}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=MagicMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns correct value"""
        mock_org.return_value = {"repos_url": "https://fake.url"}
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "https://fake.url")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=MagicMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos returns correct names and filters by license"""
        mock_repos_url.return_value = "https://fake.url"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        self.assertEqual(client.public_repos(license="apache-2.0"), ["repo1"])
        mock_get_json.assert_called_once_with("https://fake.url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": fixtures.ORG_PAYLOAD,
        "repos_payload": fixtures.REPOS_PAYLOAD,
        "expected_repos": fixtures.EXPECTED_REPOS,
        "apache2_repos": fixtures.APACHE2_REPOS,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with fixtures"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and provide fixture side effects"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MagicMock(json=lambda: cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MagicMock(json=lambda: cls.repos_payload)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
