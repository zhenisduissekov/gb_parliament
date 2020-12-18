# -*- coding: utf-8 -*-
from neo4j import GraphDatabase
from elasticsearch import Elasticsearch
import json
from test_connection import TestConnection
import yaml


def load_configs():
    with open('config.yaml') as file:
        return yaml.safe_load(file)


class Neo:

    def __init__(self):
        config = load_configs()
        neo_url, neo_user, neo_pwd = config['neo4j']['url'], config['neo4j']['username'], config['neo4j']['password']
        self.driver = GraphDatabase.driver(neo_url, auth=(neo_user, neo_pwd))
        # TestConnection.test_neo4j_connection(driver)

    def close(self):
        self.driver.close()

    # Inserting data into a Neo4j db using queries
    def insertNeo4j(self, neo_person, neo_organization, neo_membership):
        query_person = \
            'MERGE (a:Person {{id: "{a1}",name: "{a2}", sort_name: "{a3}", email: "{a4}", nationality: "GB"}});' \
            .format(a1=neo_person.id, a2=neo_person.name, a3=neo_person.alias, a4=neo_person.email)
        query_organization = \
            'MERGE (b:Organization {{group_id: "{a1}", name: "{a2}"}});'\
            .format(a1=neo_organization.group_id, a2=neo_organization.name)
        query_membership = \
            'MATCH (a:Person{{id:"{a1}"}}) MATCH(b:Organization{{group_id: "{a2}"}}) MERGE (a)-[:MEMBER_IN]->(b);'\
            .format(a1=neo_membership.id, a2=neo_membership.group_id)
        with self.driver.session() as session:
            session.run(query_person)
            session.run(query_organization)
            session.run(query_membership)

    def cleanNeo4j(self):
        query = 'MATCH (n) DETACH DELETE n'
        with self.driver.session() as session:
            session.run(query)

    def execute_neo_query(self, query, out):
        with self.driver.session() as session:
            result = session.run(query + out)
            result_list = []
            for record in result:
                rel = record[out]
                result_list.append(rel)
        return result_list


class ES:

    def __init__(self):
        config = load_configs()
        es_url, es_port = config['es']['url'], config['es']['port']
        self.driver = Elasticsearch([{'host': es_url, 'port': es_port}])
        # TestConnection.test_es_connection(self)  # TODO: finish with testing

    def close(self):
        self.driver.close()

    def insertES(self, es_person, es_organization, es_membership):
        es_person_json = json.dumps(es_person.__dict__)
        es_organization_json = json.dumps(es_organization.__dict__)
        es_membership_json = json.dumps(es_membership.__dict__)
        self.driver.index(index="people", id=es_person.id, body=es_person_json)
        self.driver.index(index="organizations", id=es_organization.group_id, body=es_organization_json)
        self.driver.index(index="memberships", id=es_membership.id, body=es_membership_json)

    def search(self, f_index="people", keyword={"match_all": {}}):
        query = {"query": keyword}
        f_result = self.driver.search(index=f_index, body=query, size=999)
        return f_result, len(f_result)

    def cleanES(self):
        self.driver.indices.delete(index='people', ignore=[400, 404])
        self.driver.indices.delete(index='organizations', ignore=[400, 404])
        self.driver.indices.delete(index='memberships', ignore=[400, 404])

    def count_recordsES(self):
        res_people = self.driver.count(index='people', ignore=[400, 404])
        res_organizations = self.driver.count(index='organizations', ignore=[400, 404])
        return res_people['count'], res_organizations['count']
