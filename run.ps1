# run_main.ps1

# Check if virtual environment exists, create if it doesn't
if (-not (Test-Path .\venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Run main.py
Write-Host "Running main.py..."
python .\main.py

# Note: We're not deactivating the virtual environment here
# so that it remains active in the current PowerShell session

Write-Host "Script execution completed. Virtual environment is still active."