# -*- coding: utf-8 -*-
from flask import Flask
from databases import Neo, ES
from Entities import Person, Organization, Membership
from flask import request
import logger

app = Flask(__name__)


def execute_neo_query(en_query, en_output):
    a = Neo()
    en_result = a.execute_neo_query(en_query, en_output)
    a.close()
    return en_result


def execute_es_query():
    es = ES()
    countPeople, countOrganizations = es.count_recordsES()
    es.close()
    return countPeople, countOrganizations


# instead of index.html
@app.route('/')
def index():
    i_result_neo = execute_neo_query('MATCH (n) RETURN count(n) as ', 'count')
    countPeople, countOrganizations = execute_es_query()
    i_result = '<h1>Total records</h1><h2>Records in Neo4j db: ' + \
           str(i_result_neo) + '</h2>' + \
           '<h2>Records in Elasticsearch db: [' + \
           str(countPeople + countOrganizations) + ']</h2>'
    return i_result


# to output all records by fieldname such as: id, name, or email..
@app.route('/parliament_records_neo/<string:fields>', methods=["GET"])
def neo_records(fields):
    n_results = execute_neo_query('MATCH (a) RETURN ', 'a.' + fields)
    result_str = ""
    for e in n_results:
        if e != None:
            result_str += '<p>' + e + '</p>'
    return result_str


# to output all records
@app.route('/parliament_records_neo', methods=["GET"])
def parliament_records():
    n_results = execute_neo_query('MATCH (a) RETURN ', 'a.name')
    result_str = ""
    for e in n_results:
        if e is not None:
            result_str += '<p>' + e + '</p>'
    return result_str


# to output all records
@app.route('/parliament_records_es', methods=["GET"])
def parliament_records_es():
    es = ES()
    n_results = es.findall()
    result_str = ""
    print(n_results)
    for e in n_results:
        if e is not None:
            result_str += '<p>' + e + '</p>'
    return result_str


@app.route('/parliament_records_neo', methods=['POST'])
def create_record():
    try:
        body = request.json
        neo = Neo()
        if body['entity'] == 'person':
            person = Person(body['id'],body['name'], body['alias'], body['email'], body['nationality'])
            neo.createPersonNeo4j(person)
        elif body['entity'] == 'organization':
            organization = Organization(body['group_id'], body['group'])
            neo.createOrganizationNeo4j(organization)
        elif body['entity'] == 'membership':
            membership = Membership(body['id'], body['group_id'])
            neo.createMembershipNeo4j(membership)
        neo.close()
        return "Success"
    except Exception as e:
        logging.error(f'Error while creating new record. Details: {e}', exc_info=True)
        neo.close()
        return f"Fail {e}"


@app.route('/parliament_records_neo', methods=['PUT'])
def insert_record():
    try:
        body = request.json
        neo = Neo()
        if body['entity'] == 'person':
            person = Person(body['id'],body['name'], body['alias'], body['email'], body['nationality'])
            neo.insertPersonNeo4j(person)
        elif body['entity'] == 'organization':
            organization = Organization(body['group_id'], body['group'])
            neo.insertOrganizationNeo4j(organization)
        elif body['entity'] == 'membership':
            membership = Membership(body['id'], body['group_id'])
            neo.insertMembershipNeo4j(membership)
        neo.close()
        return "Success"
    except Exception as e:
        logging.error(f'Error while creating new record. Details: {e}', exc_info=True)
        neo.close()
        return f"Fail {e}"

# Delete by id or group_id depending on the collection
@app.route('/parliament_records_neo', methods=['DELETE'])
def delete():
    try:
        neo = Neo()
        body = request.json
        if body['entity'] == 'person':
            neo.removeRecordNeo4j('person', body['id'])
        if body['entity'] == 'organization':
            neo.removeRecordNeo4j('organization', body['group_id'])
        if body['entity'] == 'membership':
            neo.removeRecordNeo4j('membership', body['id'])
        neo.close()
        return "Deleted successfully"
    except Exception as e:
        logging.error(f'Error while deleting a record. Details: {e}', exc_info=True)
        neo.close()
        return f"Fail {e}"

# Delete by id or group_id depending on the collection
@app.route('/parliament_records_es', methods=['DELETE'])
def delete_es():
    try:
        es = ES()
        body = request.json
        print(body['entity'])
        es.removeRecordES(index='person', doc=body["queries"])
        es.close()
    except Exception as e:
        logging.error(f'Error while deleting a record. Details: {e}', exc_info=True)
        es.close()
        return f"Fail {e}"


if __name__ == "__main__":
    logging = logger.logger_config(with_file=True)
    app.run(debug=True)
