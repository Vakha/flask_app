# Shepherd
_Herd management system_

## Requirements
 - Python 3.8+
 - pip

## Installation
1. Checkout project
```bash
git clone https://github.com/Vakha/xccelerated_task
cd xccelerated_task
```
2. Setup and activate virtual environment
```bash
python3 -m venv venv
. venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Add project root to python path
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Run as python script
```bash
python shepherd/herd.py $FILENAME $DAY_NUMBER
```
Example:
```bash
python shepherd/herd.py herd.xml 14
```

## Run as web service locally
1. Setup flask variables
```bash
export FLASK_APP=shepherd
export FLASK_ENV=development
flask run
```
2. Initialise database schema
```bash
flask init-db
```
3. Write test data to database
```bash
flask write-test-data tests/data.sql
```
4. Run Flask application
```bash
flask run
```

## Explore application
Open http://127.0.0.1:5000/ in your favourite browser, and you'll be redirected to overview page.
Overview page contains
- Navigation between days
- Ordering form
- Amount of resources in stock
- Herd list (as for current day)
- Order list for current day

## Run test
