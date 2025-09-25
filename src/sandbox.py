# src/alex_agent.py
import os, logging
from src.state_manager import StateManager
from src.context_engine import ContextEngine
from src.tasks import code_generator, code_debugger, code_optimizer, code_review
from src.utils.git_utils import commit_changes
from src.sandbox import run_in_sandbox   # supports code_string now

class AlexAgent:
    def __init__(self, config):
        self.config = config
        self.state = StateManager().load_state()
        self.ctx = ContextEngine()
        self.logger = logging.getLogger("AlexAgent")

    def run(self):
        self.logger.info("🚀 AlexAgent running in autonomous mode...")
        while True:
            self.self_extend()

    def self_extend(self):
        missing = self.detect_missing_modules()
        if not missing:
            self.logger.info("✅ No missing modules. Optimizing existing code...")
            self.optimize_existing_code()
            return

        for module in missing:
            self.logger.info(f"🛠️ Generating {module}...")
            code = code_generator.generate(module, self.config)
            code = code_optimizer.optimize(code)
            code = code_debugger.debug(code)
            code_review.review(code, module)

            # 🔐 Sandbox test BEFORE saving
            stdout, stderr = run_in_sandbox(code_string=code)
            if stderr.strip():
                self.logger.error(f"❌ Sandbox failed for {module}: {stderr}")
                self.ctx.log_context("sandbox_fail", {"module": module, "error": stderr})
                continue

            self.logger.info(f"✅ Sandbox passed for {module}: {stdout.strip()}")

            # Save only verified code
            path = os.path.join("src", f"{module}.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            commit_changes([path], f"Auto-generated {module}.py (sandbox verified)")
            self.state["modules"].append(module)
            StateManager().save_state(self.state)
            self.ctx.log_context("module_created", {"name": module})

    def optimize_existing_code(self):
        for root, _, files in os.walk("src"):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        code = f.read()

                    new_code = code_optimizer.optimize(code)
                    if new_code != code:
                        # 🔐 Sandbox inline check before overwrite
                        stdout, stderr = run_in_sandbox(code_string=new_code)
                        if stderr.strip():
                            self.logger.error(f"❌ Sandbox failed on optimization {file}: {stderr}")
                            self.ctx.log_context("sandbox_fail_opt", {"file": file, "error": stderr})
                            continue

                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_code)

                        self.logger.info(f"✅ Sandbox passed optimization for {file}: {stdout.strip()}")
                        commit_changes([path], f"Optimized {file} (sandbox verified)")
                        self.ctx.log_context("optimized", {"file": file})
