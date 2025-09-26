@echo off
echo Reset StockReport MCP Environment...

echo Removing virtual environment...
rmdir /s /q .venv 2>nul

echo Creating new virtual environment...
uv venv

echo Installing dependencies...
uv sync

echo Environment reset complete!
echo Now you can run: uv run python start_server.py

pause