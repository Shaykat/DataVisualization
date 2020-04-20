# Visualization of COVID-19 Breakout Around The World

This Application can be run in Linux, Windows and Mac OS. We developed this project in Mac OS and also deployed it on a Linux server. It will perform better in the Linux environment.


# Configuration For Linux:
First download the necessary packages: 
```sudo add-apt-repository ppa:jonathonf/python-3.6 
sudo apt-get update 
sudo apt-get install python3.6 python-pip python-dev libpq-dev
```
# Create Virtual Environment
Update pip and install virtual environment:
```
sudo pip install --upgrade pip 
sudo apt-get install virtualenv 
sudo pip install --upgrade virtualenv
```

Create a project directory:
```
mkdir/DataVisualization 
cd /DataVisualization
```

Create virtual environment and activate:
```
virtualenv --python=python3.6 venv 
source venv/bin/activate
```

# Install Python Packages:
```
pip install psycopg2 django==3.0.3 psycopg2==2.8.4 Pillow==7.0.0 pandas==1.0.3
or
pip install -r req_lib.txt
```

# Clone The Project and Setup
Clone inside DataVisualization or download and Put inside DataVisualization:
```
Git clone https://github.com/Shaykat/DataVisualization
```

Set Static Root and URL:
```
STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static") 
```

Allowed Hosts:
```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'www.localhost']
```
Now Make Migrations for Generate Database According to Model:
```
cd DataVisualization 
Python manage.py makemigrations 
Python manage.py migrate
```

Collect all the static files:
```
Python manage.py  collectstatic
```

Now Run The Application:
```
Python manage.py runserver
```

# For Mac OS 
```
just install packages using Brew
```
