cd streamlit-app-deploy
py -m venv env
env\Scripts\activate.bat
py -m pip install streamlit==1.41.1
py -m pip freeze > requirements.txt


python -m venv env
env\Scripts\activate.bat
pip freeze > requirements.txt