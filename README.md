# gb_parliament
## Test task

### Usage
1. git clone
2. cd to `gb_paliament/`
3. run `docker-compose up` to run images: neo4j, elasticsearch, and kibana
4. cd `code/` 
5. run `main.py` to upload data to neo4j and elasticsearch
6. run `api.py` to run flask server with basic REST API on `localhost:5050`
7. GET, POST, PUT and DELETE are on `localhost:5050/parliament_records_neo` and `localhost:5050/parliament_records_es`

### Requires
* Ubuntu 18.04
* python >= 3.8
* required modules are listed in requirements.txt

### Configure
* urls and ports are in `config.yml`

#### TODO:
* Dockerfile still in production 