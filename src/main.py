import argparse
from loguru import logger
from agent_coordinator import AgentCoordinator

def main():
    parser = argparse.ArgumentParser(description='Alex Autonomous Coding Bot')
    parser.add_argument('--mode', default='swarm', help='Run mode: swarm or single')
    args = parser.parse_args()

    logger.info('Starting Alex in mode: {}', args.mode)
    coordinator = AgentCoordinator()
    if args.mode == 'swarm':
        coordinator.run_swarm()
    else:
        coordinator.run_single_task('Generate sample code')

if __name__ == '__main__':
    main()
