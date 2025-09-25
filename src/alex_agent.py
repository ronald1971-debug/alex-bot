from loguru import logger
from code_generator import CodeGenerator
from sandbox import Sandbox


class AlexAgent:
    """Core agent class for performing tasks."""

    def __init__(self, role='general'):
        """Initialize agent with role, code generator, and sandbox.

        Args:
            role (str): Role of the agent (e.g., generator, tester).
        """
        self.role = role
        self.generator = CodeGenerator()
        self.sandbox = Sandbox()
        logger.info("AlexAgent initialized with role: {}", role)

    def perform_task(self, task):
        """Perform a task using AI generation or sandbox execution.

        Args:
            task (str): Task description or file path (for tester role).

        Returns:
            str: Task result or error message.
        """
        try:
            if self.role == 'tester':
                # For tester, task is the path to a generated code file
                stdout, stderr = self.sandbox.run_in_sandbox(task)
                if stdout is None:
                    logger.error("Tester failed for {}: {}", task, stderr)
                    return f"Test failed: {stderr}"
                logger.info("Tester result for {}: stdout={}, stderr={}", task, stdout, stderr)
                return f"Test result: stdout={stdout}, stderr={stderr}"
            else:
                # Other roles use AI generation
                prompt = f"As a {self.role} agent, {task}"
                result = self.generator.generate_code(prompt)
                logger.info("Agent {} result: {}", self.role, result)
                return result
        except Exception as e:
            logger.error("Task failed for role {}: {}", self.role, e)
            raise


import unittest
import tempfile
import os


class TestAlexAgent(unittest.TestCase):
    """Unit tests for AlexAgent."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_script.py")
        with open(self.test_file, "w") as f:
            f.write('print("Test output")')

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_perform_task_generator(self):
        """Test generator role (mocked)."""
        agent = AlexAgent('generator')
        def mock_generate_code(prompt):
            return "Mock generated code"
        agent.generator.generate_code = mock_generate_code
        result = agent.perform_task("Write hello world")
        self.assertEqual(result, "Mock generated code")

    def test_perform_task_tester(self):
        """Test tester role with sandbox."""
        agent = AlexAgent('tester')
        result = agent.perform_task(self.test_file)
        self.assertIn("Test output", result)
        with open("data/logs/sandbox.log", "r") as f:
            logs = f.read()
        self.assertIn("Sandbox execution of", logs)

    def test_perform_task_error(self):
        """Test error handling for nonexistent file in tester role."""
        agent = AlexAgent('tester')
        result = agent.perform_task("nonexistent.py")
        self.assertIn("File not found", result)


if __name__ == "__main__":
    unittest.main()