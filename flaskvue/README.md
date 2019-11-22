# How to run UI on local computer
1. Run terminal
2. cd to flaskvue directory
3. use: pip install flask
4. use: FLASK_APP=run.py FLASK_DEBUG=1 flask run
    1. If above command doesn't work and you're on Windows:
        1. Powershell: $env:FLASK_APP = "run.py"
        2. Command Prompt: set FLASK_APP=run.py
        3. flask run
5. In a separate terminal, cd to flaskvue/frontend directory
6. use: npm install
7. npm run dev
    1. If errors relating to "can't find module bulma" do:
        1. Exit the server with CTRL + C
        2. npm install bulma
        3. npm run dev
