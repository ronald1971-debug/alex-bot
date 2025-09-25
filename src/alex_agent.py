from loguru import logger
from code_generator import CodeGenerator

class AlexAgent:
    def __init__(self, role='coder'):
        self.role = role
        self.code_generator = CodeGenerator()

    def execute_task(self, task):
        logger.info('Agent ({}) received task: {}', self.role, task)
        # Simple decision tree for demonstration
        if 'code' in task.lower() or 'generate' in task.lower():
            self.code_generator.generate(task)
        else:
            logger.info('Agent is planning for task: {}', task)
            # In a real system, this would involve long-term planning
