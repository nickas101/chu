## Introduction
This repo is for keeping track of Dorsum solver in the static oven code things.
## Getting Started
>Python and pip are supposed to be installed
>https://www.python.org/downloads/

## Using virtual environment
>Using a virtual environment is not compulsory but advisable

Install `virtualenvwrapper`:
```
$ pip install virtualenvwrapper
```
Create virtual environment with a name `venv_name`:
```
$ mkvirtualenv venv_name
```
Switch to the virtual environment:
```
$ workon venv_name
```
Install dependences into the virtual environment:
```
(venv_name)$ pip install -r requirements.txt
```

To save list of current dependences of the virtual environment:
```
(venv_name)$ pip freeze > requirements.txt
```
To deactivate the virtual environment:
```
(venv_name)$ deactivate
```

## Start the application
Host and port can be changed in `main.py` file:
```
if __name__ == "__main__":
    serve(app, host='172.20.7.226', port=8080)
```
To start the application from a working folder (using the virtual environment):
```
(venv_name)$ <<your_path>>\chu>python main.py
```
 
 ## Tests
 To run all tests:
```
$ py.test -v tests/
```
