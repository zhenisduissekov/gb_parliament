# -*- coding: utf-8 -*-
from flask import Flask
from databases import Neo, ES
from Entities import Person

app = Flask(__name__)


def execute_neo_query(en_query, en_output):
    a = Neo()
    en_result = a.execute_neo_query(en_query, en_output)
    a.close()
    return en_result


def execute_es_query(): # TODO: finish it
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
           '<h2>Records in Elasticsearch db: ' + \
           str(countPeople + countOrganizations) + ' (People = ' + str(countPeople) + '), (Organizations = '+ \
           str(countOrganizations) + ')</h2>'
    return i_result


# to output all records by fieldname such as: id, name, or email..
@app.route('/neo_records/<string:fields>', methods=["GET"])
def neo_records(fields):
    n_results = execute_neo_query('MATCH (a) RETURN ', 'a.' + fields)
    result_str = ""
    for e in n_results:
        if e != None:
            result_str += '<p>' + e + '</p>'
    return result_str


@app.route('/new_record', methods=['POST'])
def create_record():
    neo_person = Person('1', 'Zhenis', 'Programmer', 'email@email.com', 'KZ')
    neo = Neo()
    query_person = \
        'MERGE (a:Person {{id: "{a1}",name: "{a2}", sort_name: "{a3}", email: "{a4}", nationality: "GB"}});' \
            .format(a1=neo_person.id, a2=neo_person.name, a3=neo_person.alias, a4=neo_person.email)
    with neo.driver.session() as session:
        session.run(query_person)
    return "Success"

@app.route('/update_nationality_by_id/<int:i>', methods=['PUT'])
def put(i):
    neo = Neo()
    query_person = 'MATCH (a:Person {{id: "{a1}"}}) SET a.nationality="American";'.format(a1=i)
    with neo.driver.session() as session:
        print(query_person)
        session.run(query_person)
    return "Updated successfully"


@app.route('/delete_record/<int:i>', methods=['DELETE'])
def delete(i):
    neo = Neo()
    query_person = 'MATCH (a:Person {{id: "{a1}"}}) DELETE a;'.format(a1=i)
    with neo.driver.session() as session:
        print(query_person)
        session.run(query_person)
    return "Deleted successfully"


if __name__ == "__main__":
    app.run(debug=True)

