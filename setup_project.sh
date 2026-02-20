#!/bin/bash

set -e  

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Redis server
echo "Installing Redis server..."
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Verify Redis installation
if redis-cli ping | grep -q PONG; then
    echo "Redis is running!"
else
    echo "Redis failed to start. Check your installation."
    exit 1
fi

# Install Python 3.13 venv and pip if missing
echo "Ensuring Python 3.13 and venv are installed..."
sudo apt install -y python3.13 python3.13-venv python3.13-dev python3-pip build-essential
mkdir TECH_1_PROJECT
cd TECH_1_PROJECT
# Create virtual environment
echo "Creating virtual environment..."
python3.13 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Setup complete! You can now run the server with: python manage.py runserver"
