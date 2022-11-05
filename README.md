# contactme_emergency
A single-button page with "Contact Me" function, using PagerDuty to alerm

# First-time configure

0. Install required packages
```
sudo apt install python3-venv python3-pip python3-dev
```
1. Create virtual environment
```
python3 -m venv venv
```
2. And, execute the following command every time:
```
source venv/bin/activate
```
3. Install python dependences
```
pip install -r requirements.txt
```
Recommand configure:
```
alias python3="PYTHONPATH=. python3"
```

# In development environment
```
python3 src/wsgi.py
```

# In production environment
Please refer to `deployment/howto.md`