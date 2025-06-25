python -m venv /path/to/new/virtual/environment -> CREATES VIRTUAL ENVIRONMENT
source ./bin/activate -> ACTIVATES THE VIRTUAL ENV
pip install Flask -> INSTALLS REQUIRED PACKAGES
pip freeze > requirements.txt ---> GENERATES A requirements.txt FILE WITH ALL THE PACKAGES
pip install -r ./requirements.txt ---> INSTALL PACKAGES AND SETS-UP VIRTUAL ENV 
