import subprocess
import os
import yaml
from loguru import logger
from datetime import datetime


class VersionControl:
    """Manages Git operations for Alex's autonomous code commits."""

    def __init__(self, repo_path="c:/alex_desktop", log_file="data/logs/version_control.log", config_path="config/api_keys.yaml"):
        """Initialize version control with repository path, logging, and GitHub credentials.

        Args:
            repo_path (str): Path to the Git repository.
            log_file (str): Path to log file for version control events.
            config_path (str): Path to API keys configuration file.
        """
        self.repo_path = repo_path.replace("/", "\\")  # Normalize for Windows
        self.log_file = log_file
        self.config_path = config_path
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logger.add(log_file, rotation="10 MB", retention="30 days", level="INFO")
        self.github_pat = self._load_github_pat()
        logger.info("VersionControl initialized for repo: {}", self.repo_path)
        self._ensure_git_initialized()

    def _load_github_pat(self):
        """Load GitHub Personal Access Token from config file.

        Returns:
            str: GitHub PAT or None if not found.
        """
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f) or {}
            pat = config.get("github_pat")
            if not pat:
                logger.warning("No GitHub PAT found in {}", self.config_path)
            return pat
        except FileNotFoundError:
            logger.error("Config file not found: {}", self.config_path)
            return None
        except yaml.YAMLError as e:
            logger.error("Failed to parse config file: {}", e)
            return None

    def _ensure_git_initialized(self):
        """Ensure the Git repository is initialized."""
        try:
            if not os.path.exists(os.path.join(self.repo_path, ".git")):
                subprocess.run(["git", "init"], check=True, cwd=self.repo_path, capture_output=True)
                logger.info("Initialized new Git repository")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to initialize Git repository: {}", e.stderr.decode())
            raise

    def commit_changes(self, message=None):
        """Commit all changes in the repository.

        Args:
            message (str, optional): Commit message. Defaults to timestamped message.

        Returns:
            bool: True if commit succeeded, False if no changes or failed.
        """
        try:
            # Check if there are changes to commit
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            if not status.stdout.strip():
                logger.info("No changes to commit")
                return False

            # Add all changes
            subprocess.run(["git", "add", "."], check=True, cwd=self.repo_path, capture_output=True)

            # Create commit message
            commit_message = message or f"Auto-commit by Alex on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                check=True,
                cwd=self.repo_path,
                capture_output=True,
            )
            logger.info("Committed changes: {}", commit_message)
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Git commit failed: {}", e.stderr.decode())
            return False

    def push_to_remote(self, remote="origin", branch="main"):
        """Push committed changes to the remote repository using HTTPS.

        Args:
            remote (str): Remote repository name (default: 'origin').
            branch (str): Branch to push to (default: 'main').

        Returns:
            bool: True if push succeeded, False if failed.
        """
        try:
            if not self.github_pat:
                logger.error("Cannot push: No GitHub PAT available")
                return False

            # Configure remote URL with PAT
            remote_url = f"https://{self.github_pat}@github.com/ronald1971-debug/alex-bot.git"
            subprocess.run(
                ["git", "remote", "set-url", remote, remote_url],
                check=True,
                cwd=self.repo_path,
                capture_output=True,
            )

            # Push changes
            subprocess.run(
                ["git", "push", remote, branch],
                check=True,
                cwd=self.repo_path,
                capture_output=True,
            )
            logger.info("Pushed changes to {}:{}", remote, branch)
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Git push failed: {}", e.stderr.decode())
            return False
        finally:
            # Reset remote URL to remove PAT for security
            subprocess.run(
                ["git", "remote", "set-url", remote, "https://github.com/ronald1971-debug/alex-bot.git"],
                check=True,
                cwd=self.repo_path,
                capture_output=True,
            )


if __name__ == "__main__":
    vc = VersionControl()
    vc.commit_changes("Test commit")
    vc.push_to_remote()


import unittest
import tempfile
import shutil
import os


class TestVersionControl(unittest.TestCase):
    """Unit tests for VersionControl class."""

    def setUp(self):
        """Set up temporary Git repository, log file, and config."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "version_control_test.log")
        self.config_file = os.path.join(self.temp_dir, "api_keys.yaml")
        with open(self.config_file, "w") as f:
            yaml.safe_dump({"github_pat": "mock_pat"}, f)
        self.vc = VersionControl(repo_path=self.temp_dir, log_file=self.log_file, config_path=self.config_file)
        logger.add(self.log_file, rotation="10 MB", retention="30 days", level="INFO")

        # Create a test file to simulate changes
        with open(os.path.join(self.temp_dir, "test.txt"), "w") as f:
            f.write("Test content")

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init(self):
        """Test initialization and Git repository setup."""
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".git")))
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("VersionControl initialized", logs)

    def test_load_github_pat(self):
        """Test loading GitHub PAT from config."""
        self.assertEqual(self.vc.github_pat, "mock_pat")
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertNotIn("No GitHub PAT found", logs)

    def test_commit_changes(self):
        """Test committing changes."""
        result = self.vc.commit_changes("Test commit")
        self.assertTrue(result)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Committed changes: Test commit", logs)

    def test_no_changes(self):
        """Test commit with no changes."""
        self.vc.commit_changes("Initial commit")
        result = self.vc.commit_changes("No changes commit")
        self.assertFalse(result)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("No changes to commit", logs)

    def test_push_to_remote_failure(self):
        """Test push to non-existent remote."""
        result = self.vc.push_to_remote()
        self.assertFalse(result)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Git push failed", logs)


if __name__ == "__main__":
    unittest.main()