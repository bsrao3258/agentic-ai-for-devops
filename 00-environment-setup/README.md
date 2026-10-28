# 00 — Local Environment Setup (Python, venv, and VS Code)

This guide prepares a local development environment for the Agentic AI for DevOps repository on Windows or Linux. Complete this module before starting the Python exercises.

## 1. Install prerequisites

Install Python 3.10 or newer and Git.

- Python downloads: https://www.python.org/downloads/
- Git downloads: https://git-scm.com/downloads
- Visual Studio Code: https://code.visualstudio.com/

On Windows, during Python installation, enable **Add Python to PATH**. On Linux, use your distribution's package manager or the official Python installation guidance. Avoid replacing the system-managed Python used by the operating system.

Verify installations.

### Windows PowerShell

```powershell
py --version
python --version
git --version
code --version
```

If `py` is unavailable but `python` works, use `python` in the commands below.

### Linux terminal

```bash
python3 --version
git --version
code --version
```

The `code` command is available when VS Code's command-line launcher is installed and on PATH. You can also open VS Code from the Start menu or your desktop environment.

## 2. Clone the GitHub repository

Choose a directory where you keep projects.

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\Projects" | Out-Null
Set-Location "$HOME\Projects"
git clone https://github.com/bsrao3258/agentic-ai-for-devops.git
Set-Location .\agentic-ai-for-devops
```

### Linux

```bash
mkdir -p "$HOME/Projects"
cd "$HOME/Projects"
git clone https://github.com/bsrao3258/agentic-ai-for-devops.git
cd agentic-ai-for-devops
```

If you have already cloned the repository, open a terminal in that existing folder instead of cloning it again.

## 3. Create a virtual environment

A virtual environment keeps this project's Python packages separate from other projects and from system Python. The environment folder is named `.venv`.

### Windows PowerShell

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation because of the execution policy, you can use this temporary, current-process-only option:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This setting applies only to the current PowerShell process. Alternatively, skip activation and run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe --version
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If the venv module is missing, install your distribution's Python venv package. For example, on Ubuntu/Debian, the package is commonly named `python3-venv` (use the package matching your Python version).

Verify the environment:

```bash
python --version
python -c "import sys; print(sys.executable)"
```

The executable path should point inside this repository's `.venv` directory.

## 4. Upgrade pip and install dependencies

```bash
python -m pip install --upgrade pip
```

PowerShell and Linux can both run this command after the virtual environment is activated.

This starter project currently uses Python's standard library for its basic examples and unit tests, so you do not need to install third-party packages yet. When the project adds libraries, we will record them in `requirements.txt` and install them with:

```bash
python -m pip install -r requirements.txt
```

Only run that last command after a `requirements.txt` file has been added.

## 5. Open the project in VS Code

From the repository root, run:

```bash
code .
```

This command works in PowerShell and Linux when the VS Code command-line launcher is configured.

Then select the virtual environment's Python interpreter:

1. Open the Command Palette: **Ctrl+Shift+P** (on macOS, **Cmd+Shift+P**).
2. Search for **Python: Select Interpreter**.
3. Select the interpreter inside this repository's `.venv` folder.
   - Windows: `.venv\Scripts\python.exe`
   - Linux: `.venv/bin/python`
4. If it is not listed, choose **Enter interpreter path** and browse to that executable.
5. Open a new VS Code terminal. If necessary, activate the environment manually using the commands above.
6. Confirm the terminal's Python path points to `.venv`.

Install the Microsoft **Python** extension in VS Code if prompted or if Python interpreter selection is unavailable.

## 6. Run the first exercise and tests

From the repository root:

### Windows PowerShell

```powershell
python .\01-python-fundamentals\agent.py
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

### Linux

```bash
python ./01-python-fundamentals/agent.py
python -m unittest discover -s ./07-devops-ai-project/tests -v
```

The tests should report success when the starter code and test files are present.

## 7. Deactivate the virtual environment

When you finish working:

```bash
deactivate
```

This command is the same in PowerShell and Linux shells.

## 8. Keep the virtual environment out of Git

Do not commit `.venv`. It contains machine-specific files and can be recreated using this guide. The repository includes a `.gitignore` with common Python environment exclusions.

Commit source code and documentation, not the virtual environment, API keys, passwords, tokens, or sensitive logs.

## Troubleshooting

- **Python command not found:** verify Python installation and PATH; reopen the terminal after installation.
- **Activation blocked in PowerShell:** use the process-scoped policy command above, or invoke `.venv\Scripts\python.exe` directly.
- **VS Code uses the wrong Python:** run **Python: Select Interpreter** and choose the project's `.venv` interpreter.
- **Linux says venv is unavailable:** install the venv package for your distribution and Python version.
- **Packages installed in the wrong place:** activate `.venv`, then use `python -m pip` rather than a bare `pip` command.

## Checklist

- [ ] Python and Git installed
- [ ] Repository cloned locally
- [ ] `.venv` created and activated
- [ ] VS Code opened at the repository root
- [ ] VS Code interpreter points to `.venv`
- [ ] First script and unit tests run successfully

## Additional example: verify your Python environment

Run from the repository root:

```powershell
python .\00-environment-setup\environment_check.py
```

Linux:

```bash
python ./00-environment-setup/environment_check.py
```

Expected output will resemble:

```text
Python version: 3.x.x
Operating system: Windows
Python executable: python.exe
Virtual environment active: False
```

Your Python version and operating system will differ. If you run it from the activated project virtual environment, `Virtual environment active` should normally be `True`. This script checks the current interpreter; it does not install or modify anything.
