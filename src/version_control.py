import subprocess
from loguru import logger

def commit_changes(message="Auto-commit by Alex"):
    """Commit changes to Git repository."""
    try:
        subprocess.run(["git", "add", "."], check=True, cwd="c:/alex_desktop")
        subprocess.run(["git", "commit", "-m", message], check=True, cwd="c:/alex_desktop")
        logger.info("Committed changes: {}", message)
    except subprocess.CalledProcessError as e:
        logger.error("Git commit failed: {}", e)

def push_to_remote():
    """Push changes to remote repository."""
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd="c:/alex_desktop")
        logger.info("Pushed changes to remote")
    except subprocess.CalledProcessError as e:
        logger.error("Git push failed: {}", e)

if __name__ == "__main__":
    commit_changes("Test commit")