# plot_data.ps1

# Check if virtual environment exists, create if it doesn't
if (-not (Test-Path .\venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Check if requirements are installed, install if they're not
if (-not (Test-Path .\venv\Lib\site-packages\numpy) -or 
    -not (Test-Path .\venv\Lib\site-packages\pandas) -or 
    -not (Test-Path .\venv\Lib\site-packages\matplotlib)) {
    Write-Host "Installing requirements..."
    pip install -r requirements.txt
}

# Run the Python script
Write-Host "Running plot.py..."
python .\src\binance\plot.py

# Deactivate virtual environment
deactivate

Write-Host "Script execution completed."