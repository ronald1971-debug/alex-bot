import subprocess
from loguru import logger

def run_in_sandbox(code_path, timeout=10):
    """Run Python code in a sandbox with timeout."""
    try:
        result = subprocess.run(
            ["python", code_path],
            capture_output=True, text=True, timeout=timeout, cwd="c:/alex_desktop"
        )
        logger.info("Sandbox execution: stdout={}, stderr={}", result.stdout, result.stderr)
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error("Sandbox execution timed out")
        return None, "Timeout"
    except subprocess.CalledProcessError as e:
        logger.error("Sandbox execution failed: {}", e)
        return None, str(e)

if __name__ == "__main__":
    stdout, stderr = run_in_sandbox("data/output/generated/code_gen_001.py")
    print(f"Output: {stdout}\nError: {stderr}")