from loguru import logger
from alex_agent import AlexAgent

class AgentCoordinator:
    def __init__(self):
        self.alex = AlexAgent()

    def run_single_task(self, task_description):
        logger.info('Coordinator executing single task: {}', task_description)
        # Placeholder for single-agent execution logic
        self.alex.execute_task(task_description)

    def run_swarm(self):
        logger.info('Coordinator starting swarm mode...')
        # Placeholder for multi-agent swarm logic
        self.alex.execute_task('Initialize project structure')

if __name__ == '__main__':
    coord = AgentCoordinator()
    coord.run_swarm()
