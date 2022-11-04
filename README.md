# contactme_emergency
A single-button page with "Contact Me" function, using PagerDuty to alerm

# First-time configure

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
