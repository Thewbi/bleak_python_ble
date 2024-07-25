# bleak_python_ble
Bluetooth Low Energy using bleak

# Introduction

Warning: Do not name your script bleak.py! It will cause a circular import error

# Python Virtual Environment

## Activating the Virtual Environment

```
python -m venv --system-site-packages venv
venv\Scripts\activate
Behind proxy:     pip install --proxy http://<YOUR_PROXY>:8080 bleak
Not behind proxy: pip install bleak
```

## Running the Application

```
python main_scanner.py
```

## Deactivating the Virtual Environment

```
deactivate
```
