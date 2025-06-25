# Python Virtual Environment Setup Commands

Use the commands below to create and manage your virtual environment and dependencies.

```bash
# Create virtual environment
python -m venv .

# Activate the virtual environment
source ./bin/activate

# Install required packages
pip install Flask

# Generate requirements.txt file
pip freeze > requirements.txt

# Install packages from requirements.txt
pip install -r ./requirements.txt
```
