# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from databases import Neo, ES

app = Flask(__name__)

courses = [{'name': 'algebra', 'code': 'ALG-101', 'course_id': '0'},
           {'name': 'math', 'code': 'MATH-101', 'course_id': '1'},
           {'name': 'english', 'code': 'ENG-101', 'course_id': '2'}]


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


@app.route('/')
def index():
    i_result_neo = execute_neo_query('MATCH (n) RETURN count(n) as count', 'count')
    countPeople, countOrganizations = execute_es_query()
    i_result = '<h1>Total records</h1><h2>Records in Neo4j db: ' + \
           str(i_result_neo) + '</h2>' + \
           '<h2>Records in Elasticsearch db: ' + \
           str(countPeople + countOrganizations) + ' (People = ' + str(countPeople) + '), (Organizations = '+ \
           str(countOrganizations) + ')</h2>' + \
           '<button onClick=>Отправить</button>'
    return i_result


@app.route('/query', methods=["GET", "POST"])
def get_query():
    return {"variables": ["upper_25", "upper_50", "upper_75", "upper_90", "upper_95"]}


@app.route('/records/<int:course_id>', methods=["GET"])
def get_course(course_id):
    return jsonify({'course': courses[course_id]})


@app.route('/neo_records', methods=["GET"])
def neo_records():
    n_results = execute_neo_query('MATCH (a) RETURN ', 'a.name')
    result_str = ""
    for e in n_results:
        result_str += '<p>' + e + '</p>'
    return result_str


def put(self, id):
    pass

def delete(self, id)

if __name__ == "__main__":
    app.run(debug=True)

