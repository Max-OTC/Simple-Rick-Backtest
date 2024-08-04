# plot_data.ps1

# Check if virtual environment exists, create if it doesn't
if (-not (Test-Path .\venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1


# Run the Python script
Write-Host "Running plot.py..."
python .\src\plot\plotBinance.py

# Deactivate virtual environment
deactivate

Write-Host "Script execution completed."