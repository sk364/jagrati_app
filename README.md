# Installation

Install python3.6, pip, virtualenv  
[This](https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get) will help you install Python 3.6  

Install pip  

> sudo apt-get install python-pip  

Upgrade to latest version
> sudo pip install -U pip

And, finally use pip to install virtualenv  
> sudo pip install virtualenv

Create a virtual environment with python 3.6  
> virtualenv -p python3.6 venv  
> source venv/bin/activate

Clone the project  
> git clone https://github.com/sk364/jagrati_app

Install project requirements  
> cd jagrati_app  
> pip install -r requirements.txt

Make migrations & Migrate
> python manage.py makemigrations  
> python manage.py migrate

Create a superuser
> python manage.py createsuperuser

Test the development server  
> python manage.py runserver
