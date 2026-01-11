# PowerShell: create virtual environment and install dependencies
python -m venv .venv
# Allow script execution for this session (may prompt for elevation in some systems)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
# Activate the venv for this PowerShell session
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Virtual environment created and requirements installed. Activate with: .\.venv\Scripts\Activate.ps1"
