# Safe Sailing

Safe Sailing provides users with the safest route to their destination.
Currently based in New York City

# DEV:

-Create the virtual environment: python -m virtualenv kivy_venv

-Activate the virtual environment on mac: source kivy_venv/bin/activate 

-Run: python3 main.py

Only branch and merge onto develop branch using the following method:

1. New Feature:
   git checkout develop <br>
   git pull origin develop <br>
   git submodule update --remote <br>
   git checkout -b SafeS123(featureNumber)-"featurename" <br>
2. Write Code:
   git status <br>
   [COPY PATH] <br>
   git add {path} <br>
   git commit -m "MESSAGE HERE" <br>
   git push origin BRANCHNAME <br>
