@echo off
setlocal enabledelayedexpansion

:: ====================================================================
:: Section 0: Setup
:: ====================================================================
title Alex Autonomous Coding Bot Setup
set "PROJECT_DIR=%~dp0"
set "VENV_NAME=venv"
set "VENV_DIR=%PROJECT_DIR%%VENV_NAME%"
set "VBS_CONTENT="

echo.
echo =====================================================
echo   Alex Autonomous Coding Bot Installation Script
echo =====================================================

:: ====================================================================
:: Section 1: Directory Creation
:: ====================================================================
echo.
echo [1/11] Creating directory structure...
if not exist "%PROJECT_DIR%src" mkdir "%PROJECT_DIR%src"
if not exist "%PROJECT_DIR%tests" mkdir "%PROJECT_DIR%tests"
if not exist "%PROJECT_DIR%temp" mkdir "%PROJECT_DIR%temp"
if not exist "%PROJECT_DIR%logs" mkdir "%PROJECT_DIR%logs"
if not exist "%PROJECT_DIR%docker" mkdir "%PROJECT_DIR%docker"
if not exist "%PROJECT_DIR%src\utils" mkdir "%PROJECT_DIR%src\utils"
if not exist "%PROJECT_DIR%src\modules" mkdir "%PROJECT_DIR%src\modules"
echo Directory structure created successfully.

:: ====================================================================
:: Section 2: Virtual Environment Setup and Dependencies (FIXED PIP COMMAND)
:: ====================================================================
echo.
echo [2/11] Setting up Python virtual environment and dependencies...

:: Check for Python installation
where python >nul 2>&1
if ERRORLEVEL 1 (
    echo ERROR: Python is not installed or not found in PATH. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: Create Virtual Environment
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
) else (
    echo Virtual environment already exists. Skipping creation.
)

:: Activate and Install Dependencies
echo Installing dependencies...
call "%VENV_DIR%\Scripts\activate"

:: Create Requirements Files
echo Creating requirements files...
type nul > requirements.txt
type nul > requirements-dev.txt
type nul > requirements-plugins.txt

:: Write core requirements
(
    echo loguru
    echo argcomplete
    echo python-dotenv
    echo requests
) > requirements.txt

:: Run pip upgrade and then install requirements
pip install --upgrade pip
pip install -r requirements.txt
if ERRORLEVEL 1 (
    echo WARNING: Failed to install all dependencies. Installation will continue.
)

:: ====================================================================
:: Section 3: Core Code Files and Dependencies (ULTIMATE SEQUENTIAL APPEND)
:: ====================================================================
echo.
echo [3/11] Writing core Python code files...

:: --- Placeholder Files (Still empty, but created) ---
for %%f in (
    src\context_engine.py
    src\telemetry.py
    src\state_manager.py
    src\task_queue.py
    src\scheduler.py
    src\error_handler.py
    src\version_control.py
    src\sandbox.py
    src\install_alex.py
    src\utils\__init__.py
    src\modules\__init__.py
) do (
    type nul > "%%f"
)

:: --- Core File: src\main.py ---
echo Creating src\main.py...
del write_main.vbs >nul 2>&1
echo Set fso = WScript.CreateObject("Scripting.FileSystemObject") >> write_main.vbs
echo Set ts = fso.CreateTextFile("src\main.py", True) >> write_main.vbs
echo ts.WriteLine("import argparse") >> write_main.vbs
echo ts.WriteLine("from loguru import logger") >> write_main.vbs
echo ts.WriteLine("from agent_coordinator import AgentCoordinator") >> write_main.vbs
echo ts.WriteLine("") >> write_main.vbs
echo ts.WriteLine("def main():") >> write_main.vbs
echo ts.WriteLine("    """"""Entry point for Alex Autonomous Coding Bot."""""""") >> write_main.vbs
echo ts.WriteLine("    parser = argparse.ArgumentParser(description='Alex Autonomous Coding Bot')") >> write_main.vbs
echo ts.WriteLine("    parser.add_argument('--mode', default='swarm', help='Run mode: swarm or single')") >> write_main.vbs
echo ts.WriteLine("    args = parser.parse_args()") >> write_main.vbs
echo ts.WriteLine("") >> write_main.vbs
echo ts.WriteLine("    logger.info('Starting Alex in mode: {}', args.mode)") >> write_main.vbs
echo ts.WriteLine("    coordinator = AgentCoordinator()") >> write_main.vbs
echo ts.WriteLine("    if args.mode == 'swarm':") >> write_main.vbs
echo ts.WriteLine("        coordinator.run_swarm()") >> write_main.vbs
echo ts.WriteLine("    else:") >> write_main.vbs
echo ts.WriteLine("        coordinator.run_single_task('Generate sample code')") >> write_main.vbs
echo ts.WriteLine("") >> write_main.vbs
echo ts.WriteLine("if __name__ == '__main__':") >> write_main.vbs
echo ts.WriteLine("    main()") >> write_main.vbs
echo ts.Close() >> write_main.vbs
cscript //nologo write_main.vbs >nul 2>&1
del write_main.vbs >nul 2>&1
echo Created src\main.py.

:: --- Core File: src\agent_coordinator.py ---
echo Creating src\agent_coordinator.py...
del write_coordinator.vbs >nul 2>&1
echo Set fso = WScript.CreateObject("Scripting.FileSystemObject") >> write_coordinator.vbs
echo Set ts = fso.CreateTextFile("src\agent_coordinator.py", True) >> write_coordinator.vbs
echo ts.WriteLine("from loguru import logger") >> write_coordinator.vbs
echo ts.WriteLine("from alex_agent import AlexAgent") >> write_coordinator.vbs
echo ts.WriteLine("") >> write_coordinator.vbs
echo ts.WriteLine("class AgentCoordinator:") >> write_coordinator.vbs
echo ts.WriteLine("    def __init__(self):") >> write_coordinator.vbs
echo ts.WriteLine("        self.alex = AlexAgent()") >> write_coordinator.vbs
echo ts.WriteLine("") >> write_coordinator.vbs
echo ts.WriteLine("    def run_single_task(self, task_description):") >> write_coordinator.vbs
echo ts.WriteLine("        logger.info('Coordinator executing single task: {}', task_description)") >> write_coordinator.vbs
echo ts.WriteLine("        # Placeholder for single-agent execution logic") >> write_coordinator.vbs
echo ts.WriteLine("        self.alex.execute_task(task_description)") >> write_coordinator.vbs
echo ts.WriteLine("") >> write_coordinator.vbs
echo ts.WriteLine("    def run_swarm(self):") >> write_coordinator.vbs
echo ts.WriteLine("        logger.info('Coordinator starting swarm mode...')") >> write_coordinator.vbs
echo ts.WriteLine("        # Placeholder for multi-agent swarm logic") >> write_coordinator.vbs
echo ts.WriteLine("        self.alex.execute_task('Initialize project structure')") >> write_coordinator.vbs
echo ts.WriteLine("") >> write_coordinator.vbs
echo ts.WriteLine("if __name__ == '__main__':") >> write_coordinator.vbs
echo ts.WriteLine("    coord = AgentCoordinator()") >> write_coordinator.vbs
echo ts.WriteLine("    coord.run_swarm()") >> write_coordinator.vbs
echo ts.Close() >> write_coordinator.vbs
cscript //nologo write_coordinator.vbs >nul 2>&1
del write_coordinator.vbs >nul 2>&1
echo Created src\agent_coordinator.py.

:: --- Core File: src\alex_agent.py ---
echo Creating src\alex_agent.py...
del write_alex_agent.vbs >nul 2>&1
echo Set fso = WScript.CreateObject("Scripting.FileSystemObject") >> write_alex_agent.vbs
echo Set ts = fso.CreateTextFile("src\alex_agent.py", True) >> write_alex_agent.vbs
echo ts.WriteLine("from loguru import logger") >> write_alex_agent.vbs
echo ts.WriteLine("from code_generator import CodeGenerator") >> write_alex_agent.vbs
echo ts.WriteLine("") >> write_alex_agent.vbs
echo ts.WriteLine("class AlexAgent:") >> write_alex_agent.vbs
echo ts.WriteLine("    def __init__(self, role='coder'):") >> write_alex_agent.vbs
echo ts.WriteLine("        self.role = role") >> write_alex_agent.vbs
echo ts.WriteLine("        self.code_generator = CodeGenerator()") >> write_alex_agent.vbs
echo ts.WriteLine("") >> write_alex_agent.vbs
echo ts.WriteLine("    def execute_task(self, task):") >> write_alex_agent.vbs
echo ts.WriteLine("        logger.info('Agent ({}) received task: {}', self.role, task)") >> write_alex_agent.vbs
echo ts.WriteLine("        # Simple decision tree for demonstration") >> write_alex_agent.vbs
echo ts.WriteLine("        if 'code' in task.lower() or 'generate' in task.lower():") >> write_alex_agent.vbs
echo ts.WriteLine("            self.code_generator.generate(task)") >> write_alex_agent.vbs
echo ts.WriteLine("        else:") >> write_alex_agent.vbs
echo ts.WriteLine("            logger.info('Agent is planning for task: {}', task)") >> write_alex_agent.vbs
echo ts.WriteLine("            # In a real system, this would involve long-term planning") >> write_alex_agent.vbs
echo ts.Close() >> write_alex_agent.vbs
cscript //nologo write_alex_agent.vbs >nul 2>&1
del write_alex_agent.vbs >nul 2>&1
echo Created src\alex_agent.py.

:: --- Core File: src\code_generator.py ---
echo Creating src\code_generator.py...
del write_code_generator.vbs >nul 2>&1
echo Set fso = WScript.CreateObject("Scripting.FileSystemObject") >> write_code_generator.vbs
echo Set ts = fso.CreateTextFile("src\code_generator.py", True) >> write_code_generator.vbs
echo ts.WriteLine("from loguru import logger") >> write_code_generator.vbs
echo ts.WriteLine("") >> write_code_generator.vbs
echo ts.WriteLine("class CodeGenerator:") >> write_code_generator.vbs
echo ts.WriteLine("    def __init__(self):") >> write_code_generator.vbs
echo ts.WriteLine("        pass") >> write_code_generator.vbs
echo ts.WriteLine("") >> write_code_generator.vbs
echo ts.WriteLine("    def generate(self, prompt):") >> write_code_generator.vbs
echo ts.WriteLine("        logger.info('CodeGenerator received prompt: {}', prompt)") >> write_code_generator.vbs
echo ts.WriteLine("        # Placeholder for actual code generation logic") >> write_code_generator.vbs
echo ts.WriteLine("        logger.info('Generating placeholder file...')") >> write_code_generator.vbs
echo ts.WriteLine("        with open('temp/generated_code.txt', 'w') as f:") >> write_code_generator.vbs
echo ts.WriteLine("            f.write(f'# Code generated for: {prompt}\n')") >> write_code_generator.vbs
echo ts.WriteLine("            f.write('def placeholder_function():\n')") >> write_code_generator.vbs
echo ts.WriteLine("            f.write('    return ""Successfully generated placeholder code!""\n')") >> write_code_generator.vbs
echo ts.WriteLine("        logger.success('Code generation complete. Check temp/generated_code.txt')") >> write_code_generator.vbs
echo ts.Close() >> write_code_generator.vbs
cscript //nologo write_code_generator.vbs >nul 2>&1
del write_code_generator.vbs >nul 2>&1
echo Created src\code_generator.py.

:: ====================================================================
:: Section 4-7: Configuration, Docker, and Testing
:: ====================================================================
echo.
echo [4/11] Writing .env configuration file...
(
    echo # Alex Environment Variables
    echo ALEX_MODE=swarm
    echo LOG_LEVEL=INFO
    echo PROJECT_ROOT=%PROJECT_DIR%
) > .env

echo.
echo [5/11] Writing .gitignore file...
(
    echo # Python
    echo __pycache__/
    echo *.pyc
    echo *.pyo
    echo *.pyd
    echo .venv/
    echo venv/
    echo temp/
    echo logs/*.log
    echo # OS Files
    echo .DS_Store
    echo Thumbs.db
    echo # Installer Files
    echo *.vbs
) > .gitignore

echo.
echo [6/11] Writing Dockerfile...
(
    echo # Use an official Python runtime as a parent image
    echo FROM python:3.11-slim
    echo 
    echo # Set the working directory in the container
    echo WORKDIR /usr/src/app
    echo 
    echo # Copy the current directory contents into the container at /usr/src/app
    echo COPY . .
    echo 
    echo # Install any needed packages specified in requirements.txt
    echo RUN pip install --no-cache-dir -r requirements.txt
    echo 
    echo # Run main.py when the container launches
    echo CMD ["python", "src/main.py", "--mode", "swarm"]
) > docker/Dockerfile

echo.
echo [7/11] Running placeholder tests...
:: Placeholder for actual pytest command
if exist "%VENV_DIR%\Scripts\pytest.exe" (
    "%VENV_DIR%\Scripts\pytest.exe" 
) else (
    echo WARNING: Pytest not found. Skipping tests.
)

:: ====================================================================
:: Section 8-11: Finalization and Launch (ULTIMATE SEQUENTIAL APPEND & PATH FIX)
:: ====================================================================
echo.
echo [10/11] Building and running Docker container (if Docker is installed)...
where docker >nul 2>&1
if ERRORLEVEL 0 (
    echo Building Docker image...
    docker build -t alex-bot-image . >nul 2>&1
    echo Running Docker container...
    :: Example run command (remove -d if you want to see logs)
    docker run -d --name alex-bot-container alex-bot-image >nul 2>&1
) else (
    echo WARNING: Docker not found. Skipping container build/run.
)

echo.
echo [11/11] Creating shortcuts and launching Alex...
set "TARGET_EXE=%VENV_DIR%\Scripts\python.exe" 
set "ARGS=src\main.py --mode swarm"

if not exist "%TARGET_EXE%" (
    echo ERROR: Python executable not found at "%TARGET_EXE%". Shortcut creation skipped.
    goto launch_only
)

:: --------------------------------------------------------------------
:: Desktop Shortcut (FINAL FIX)
:: --------------------------------------------------------------------
echo Writing Desktop VBScript file...
del CreateDesktopShortcut.vbs >nul 2>&1
echo Set oShell = WScript.CreateObject("WScript.Shell") >> CreateDesktopShortcut.vbs
echo Set oShortcut = oShell.CreateShortcut(oShell.ExpandEnvironmentStrings("%%USERPROFILE%%\Desktop\Alex.lnk")) >> CreateDesktopShortcut.vbs
echo oShortcut.TargetPath = "%TARGET_EXE%" >> CreateDesktopShortcut.vbs
echo oShortcut.Arguments = "%ARGS%" >> CreateDesktopShortcut.vbs
echo oShortcut.WorkingDirectory = "%PROJECT_DIR%" >> CreateDesktopShortcut.vbs
echo oShortcut.IconLocation = "%%SystemRoot%%\System32\SHELL32.dll,0" >> CreateDesktopShortcut.vbs
echo oShortcut.Save >> CreateDesktopShortcut.vbs

cscript //nologo CreateDesktopShortcut.vbs
if exist "%USERPROFILE%\Desktop\Alex.lnk" (
    echo Desktop shortcut created successfully.
) else (
    echo WARNING: Failed to create Desktop shortcut.
)
del CreateDesktopShortcut.vbs >nul 2>&1

:: --------------------------------------------------------------------
:: Start Menu Shortcut (FINAL FIX)
:: --------------------------------------------------------------------
echo Writing Start Menu VBScript file...
del CreateStartMenuShortcut.vbs >nul 2>&1
echo Set oShell = WScript.CreateObject("WScript.Shell") >> CreateStartMenuShortcut.vbs
echo Set oShortcut = oShell.CreateShortcut(oShell.ExpandEnvironmentStrings("%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Alex.lnk")) >> CreateStartMenuShortcut.vbs
echo oShortcut.TargetPath = "%TARGET_EXE%" >> CreateStartMenuShortcut.vbs
echo oShortcut.Arguments = "%ARGS%" >> CreateStartMenuShortcut.vbs
echo oShortcut.WorkingDirectory = "%PROJECT_DIR%" >> CreateStartMenuShortcut.vbs
echo oShortcut.IconLocation = "%%SystemRoot%%\System32\SHELL32.dll,0" >> CreateStartMenuShortcut.vbs
echo oShortcut.Save >> CreateStartMenuShortcut.vbs

cscript //nologo CreateStartMenuShortcut.vbs >nul 2>&1
del CreateStartMenuShortcut.vbs >nul 2>&1


:launch_only
echo.
echo Launching Alex...
:: We use the full path to python.exe in the venv
start "" "%VENV_DIR%\Scripts\python.exe" "src\main.py" --mode swarm

echo.
echo =====================================================
echo   ✅ Installation Complete
echo   Alex is running in swarm mode
echo =====================================================

endlocal
pause