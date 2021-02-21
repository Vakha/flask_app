# Shepherd
_Herd management system_

## Currently available by following URLs
- http://35.204.73.169/
- http://35.204.73.169/yak-shop/ui

## Project structure
- **shepherd** - folder with flask application
  - **swagger.yml** - API specification with mapping to python function in `yakshopapi` module 
  - **yakshopapi.py** - Adapter between RESTAPI and `service`
  - **service.py** - Business logic implementation
  - **product_calculator.py** - Util module to calculate milk and skins production
  - **storage.py** - Persistence module, works with database
  - **db.py** - Setup database connection
  - **\_\_init\_\_.py** - Create Flask application
  - **parser.py** - Parser of xml file with herd
  - **schema.sql** - Script to setup database schema
  - **model.py** - Dataclasses of core system objects
  - **records** - Convertor of model from/to db records
  - **templates** - Jinja2 html templates
    - **overview.html** - Html for single page application
  - **static** - Static content
    - **js** - JavaScript
      - **overview.js** - Scripts supporting overview.html
- **tests** - test folder

## Checkout project
```bash
git clone https://github.com/Vakha/flask_app
cd flask_app
```

## Run as prebuild docker image locally
### Requirements
- docker 
- docker-compose

Simply run following command 
```bash
docker-compose up -d
```

## Explore API specification
Open http://127.0.0.1:5000/yak-shop/ui in your favourite browser.

## Explore application
Open http://127.0.0.1:5000/ in your favourite browser, and you'll be redirected to overview page.

Overview page contains:
- Navigation between days
- Ordering form
- Amount of resources in stock
- Herd list (as for current day)
- Order list for current day

## Installation
### Requirements
 - Python 3.8+
 - pip

1. Setup and activate virtual environment
```bash
python3 -m venv venv
. venv/bin/activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Add project root to python path
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

## Run test
```bash
pytest
```

## Check test coverage
1. Run test with coverage
```bash
coverage run -m pytest
```
2. See report in terminal
```bash
coverage report
```
3. More detailed html report
```bash
coverage html
open htmlcov/index.html
```

## Make distribution file
```bash
python setup.py bdist_wheel
```
`.whl` file could be found in `dist` folder
```bash
ls dist/shepherd-1.0.0-py3-none-any.whl
```
Could be run on another machine as following:
```bash
pip install shepherd-1.0.0-py3-none-any.whl
flask init-db
flask write-test-data $TEST_DATA_FILE
flask run 
```
Note:
If you see this message
```
The swagger_ui directory could not be found.
```
run the following command (must be quoted in `zsh`)
```bash
pip install 'connexion[swagger-ui]'
```

## Build docker image
```bash
docker build -t vakha/shepherd:latest .
```
then run
```bash
docker-compose up -d
```