import importlib
import os
import sys
from loguru import logger


class PluginManager:
    """Manages loading and execution of plugins for Alex."""

    def __init__(self, plugins_dir="plugins", log_file="data/logs/plugin_manager.log"):
        """Initialize plugin manager with plugins directory and logging.

        Args:
            plugins_dir (str): Directory containing plugin subdirectories.
            log_file (str): Path to log file for plugin manager events.
        """
        self.plugins_dir = plugins_dir.replace("/", "\\")  # Normalize for Windows
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logger.add(log_file, rotation="10 MB", retention="30 days", level="INFO")
        # Add project root to sys.path
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        logger.info("PluginManager initialized with plugins directory: {}", self.plugins_dir)

    def load_plugins(self):
        """Load all plugins from the plugins directory.

        Returns:
            list: List of loaded plugin modules.
        """
        plugins = []
        plugins_path = os.path.join(os.path.dirname(__file__), "..", "..", self.plugins_dir)
        if not os.path.exists(plugins_path):
            logger.error("Plugins directory not found: {}", plugins_path)
            return plugins

        for folder in os.listdir(plugins_path):
            plugin_path = os.path.join(plugins_path, folder, "plugin.py")
            if os.path.isfile(plugin_path):
                try:
                    spec = importlib.util.spec_from_file_location(f"plugins.{folder}.plugin", plugin_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[f"plugins.{folder}.plugin"] = module
                    spec.loader.exec_module(module)
                    plugins.append(module)
                    logger.info("Loaded plugin: {}", folder)
                except Exception as e:
                    logger.error("Failed to load plugin {}: {}", folder, e)
        return plugins

    def execute_plugin_task(self, plugin_name, task_name, *args, **kwargs):
        """Execute a specific task in a plugin.

        Args:
            plugin_name (str): Name of the plugin folder.
            task_name (str): Name of the task function to execute.
            *args, **kwargs: Arguments to pass to the task function.

        Returns:
            Any: Result of the task function or None if failed.
        """
        try:
            module = sys.modules.get(f"plugins.{plugin_name}.plugin")
            if not module:
                logger.error("Plugin not loaded: {}", plugin_name)
                return None
            task_func = getattr(module, task_name, None)
            if not callable(task_func):
                logger.error("Task {} not found in plugin {}", task_name, plugin_name)
                return None
            result = task_func(*args, **kwargs)
            logger.info("Executed task {} in plugin {}: result={}", task_name, plugin_name, result)
            return result
        except Exception as e:
            logger.error("Failed to execute task {} in plugin {}: {}", task_name, plugin_name, e)
            return None


if __name__ == "__main__":
    plugin_manager = PluginManager()
    plugins = plugin_manager.load_plugins()


import unittest
import os
import tempfile
import shutil


class TestPluginManager(unittest.TestCase):
    """Unit tests for PluginManager class."""

    def setUp(self):
        """Set up temporary plugins directory and manager instance."""
        self.temp_dir = tempfile.mkdtemp()
        self.plugins_dir = os.path.join(self.temp_dir, "plugins")
        self.log_file = os.path.join(self.temp_dir, "plugin_manager_test.log")
        os.makedirs(os.path.join(self.plugins_dir, "test_plugin"))
        with open(os.path.join(self.plugins_dir, "test_plugin", "plugin.py"), "w") as f:
            f.write('def test_task():\n    return "Test result"')
        self.manager = PluginManager(plugins_dir="plugins", log_file=self.log_file)
        logger.add(self.log_file, rotation="10 MB", retention="30 days", level="INFO")

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init(self):
        """Test plugin manager initialization and log file creation."""
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("PluginManager initialized", logs)

    def test_load_plugins(self):
        """Test loading plugins from directory."""
        plugins = self.manager.load_plugins()
        self.assertEqual(len(plugins), 1)
        self.assertIn("plugins.test_plugin.plugin", sys.modules)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Loaded plugin: test_plugin", logs)

    def test_execute_plugin_task(self):
        """Test executing a plugin task."""
        self.manager.load_plugins()
        result = self.manager.execute_plugin_task("test_plugin", "test_task")
        self.assertEqual(result, "Test result")
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Executed task test_task in plugin test_plugin", logs)

    def test_nonexistent_plugin(self):
        """Test executing task in nonexistent plugin."""
        result = self.manager.execute_plugin_task("nonexistent", "test_task")
        self.assertIsNone(result)
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.assertIn("Plugin not loaded: nonexistent", logs)


if __name__ == "__main__":
    unittest.main()