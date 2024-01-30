## Fingerprint Authentication System (Remote server)

### Development Setup:
```
virtualenv --python=$(which python3) venv
source venv/bin/activate
pip install -r req.txt
```

### Create SQLite DB:
```
python3 create_table.py
```

### Run the code
```
python3 app.py
```
