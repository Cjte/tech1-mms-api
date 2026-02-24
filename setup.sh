mkdir TECH_1_PROJECT
mv requirements.txt
mv tech1core
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

cd tech1core
# Run Django migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Setup complete!"
python manage.py runserver
