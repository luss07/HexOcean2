### Python version: 3.6.9

### Virtual environment:
If You don't have virtualenv manager installed:
```bash
sudo apt-get install python3-venv 
```

Create environment:
```bash
python3 -m venv .venv
```

Activate:
```bash
source ./venv/bin/activate
```

 
### Install required python packages:
```bash
pip install -r requirements-dev.txt
```


### Apply database migrations:
```bash
python manage.py migrate
```


### Collect static files:
```bash
python manage.py collectstatic
```


### Run local server:
```bash
python manage.py runserver
```