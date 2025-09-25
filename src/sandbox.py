import subprocess
import os
from loguru import logger


class Sandbox:
    """Executes Python code in a safe, isolated environment with timeouts."""

    def __init__(self, log_file="data/logs/sandbox.log", working_dir="c:/alex_desktop"):
        """Initialize sandbox with logging and working directory.

        Args:
            log_file (str): Path to log file for sandbox events.
            working_dir (str): Working directory for code execution.
        """
        self.log_file = log_file
        self.working_dir = working_dir.replace("/", "\\")  # Normalize for Windows
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logger.add(log_file, rotation="10 MB", retention="30 days", level="INFO")
        logger.info("Sandbox initialized with working directory: {}", self.working_dir)

    def run_in_sandbox(self, code_path, timeout=10):
        """Execute a Python script in a sandbox with timeout.

        Args:
            code_path (str): Path to the Python script to execute (relative to working_dir).
            timeout (int): Maximum execution time in seconds.

        Returns:
            tuple: (stdout, stderr) if successful, (None, error_message) if failed.
        """
        try:
            # Validate code path
            code_path = os.path.join(self.working_dir, code_path).replace("/", "\\")
            if not os.path.isfile(code_path):
                logger.error("Code file not found: {}", code_path)
                return None, f"File not found: {code_path}"
            if not code_path.endswith(".py"):
                logger.error("Invalid file type, must be .py: {}", code_path)
                return None, f"Invalid file type: {code_path}"

            # Run script with timeout
            result = subprocess.run(
                ["python", code_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_dir,
            )
            logger.info(
                "Sandbox execution of {}: returncode={}, stdout={}, stderr={}",
                code_path,
                result.returncode,
                result.stdout,
                result.stderr,
            )
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error("Sandbox execution of {} timed out after {} seconds", code_path, timeout)
            return None, f"Execution timed out after {timeout} seconds"
        except subprocess.CalledProcessError as e:
            logger.error("Sandbox execution of {} failed: {}", code_path, e.stderr)
            return None, f"Execution failed: {e.stderr}"
        except Exception as e:
            logger.error("Unexpected error in sandbox execution of {}: {}", code_path, e)
            return None, f"Unexpected error: {str(e)}"


if __name__ == "__main__":
    sandbox = Sandbox()
    stdout, stderr = sandbox.run_in_sandbox("data/output/generated/code_gen_001.py")
    print(f"Stdout: {stdout}\nStderr: {stderr}")


import unittest
import os
import tempfile


class TestSandbox(unittest.TestCase):
    """Unit tests for Sandbox class."""

    def setUp(self):
        """Set up temporary directory and sandbox instance."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "sandbox_test.log")
        self.sandbox = Sandbox(log_file=self.log_file, working_dir=self.temp_dir)
        logger.add(self.log_file, rotation="10 MB", retention="30 days", level="INFO")

        # Create a test Python file
        self.test_file = os.path.join(self.temp_dir, "test_script.py")
        with open(self.test_file, "w") as f:
            f.write('print("Hello from sandbox")')

    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init(self):
        """Test sandbox initialization and log file creation."""
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Sandbox initialized", logs)

    def test_run_valid_script(self):
        """Test running a valid Python script."""
        stdout, stderr = self.sandbox.run_in_sandbox("test_script.py")
        self.assertEqual(stdout.strip(), "Hello from sandbox")
        self.assertEqual(stderr.strip(), "")
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Sandbox execution of", logs)

    def test_run_nonexistent_script(self):
        """Test running a nonexistent script."""
        stdout, stderr = self.sandbox.run_in_sandbox("nonexistent.py")
        self.assertIsNone(stdout)
        self.assertIn("File not found", stderr)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Code file not found", logs)

    def test_run_timeout(self):
        """Test running a script that exceeds timeout."""
        with open(os.path.join(self.temp_dir, "timeout_script.py"), "w") as f:
            f.write("import time\ntime.sleep(5)")
        stdout, stderr = self.sandbox.run_in_sandbox("timeout_script.py", timeout=1)
        self.assertIsNone(stdout)
        self.assertIn("timed out", stderr)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("timed out after 1 seconds", logs)


if __name__ == "__main__":
    unittest.main()