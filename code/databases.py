# -*- coding: utf-8 -*-
from neo4j import GraphDatabase
from elasticsearch import Elasticsearch
import json
import yaml


#   for loading configuration to connect to our dbs
def load_configs():
    with open('config.yaml') as file:
        return yaml.safe_load(file)


#   to work with Neo4j DB: initialize connection, close it, insert data, clear from data
class Neo:

    def __init__(self):
        config = load_configs()
        neo_url, neo_user, neo_pwd = config['neo4j']['url'], config['neo4j']['username'], config['neo4j']['password']
        self.driver = GraphDatabase.driver(neo_url, auth=(neo_user, neo_pwd))

    def close(self):
        self.driver.close()

# Insert person data into a Neo4j db using queries
    def insertPersonNeo4j(self, neo_person):
        query_person = \
            'MERGE (a:Person {{id: "{a1}",name: "{a2}", sort_name: "{a3}", email: "{a4}", nationality: "GB"}});' \
            .format(a1=neo_person.id, a2=neo_person.name, a3=neo_person.alias, a4=neo_person.email)
        with self.driver.session() as session:
            session.run(query_person)

# Insert organization data into a Neo4j db using queries
    def insertOrganizationNeo4j(self, neo_organization):
        query_organization = \
            'MERGE (b:Organization {{group_id: "{a1}", name: "{a2}"}});'\
            .format(a1=neo_organization.group_id, a2=neo_organization.name)
        with self.driver.session() as session:
            session.run(query_organization)

# Insert membership data into a Neo4j db using queries
    def insertMembershipNeo4j(self, neo_membership):
        query_membership = \
            'MATCH (a:Person{{id:"{a1}"}}) MATCH(b:Organization{{group_id: "{a2}"}}) MERGE (a)-[:MEMBER_IN]->(b);'\
            .format(a1=neo_membership.id, a2=neo_membership.group_id)
        with self.driver.session() as session:
            session.run(query_membership)

        # Create person data into a Neo4j db using queries
        def createPersonNeo4j(self, neo_person):
            query_person = \
                'CREATE (a:Person {{id: "{a1}",name: "{a2}", sort_name: "{a3}", email: "{a4}", nationality: "GB"}});' \
                    .format(a1=neo_person.id, a2=neo_person.name, a3=neo_person.alias, a4=neo_person.email)
            with self.driver.session() as session:
                session.run(query_person)

        # Create organization data into a Neo4j db using queries
        def createOrganizationNeo4j(self, neo_organization):
            query_organization = \
                'CREATE (b:Organization {{group_id: "{a1}", name: "{a2}"}});' \
                    .format(a1=neo_organization.group_id, a2=neo_organization.name)
            with self.driver.session() as session:
                session.run(query_organization)

        # Create membership data into a Neo4j db using queries
        def createMembershipNeo4j(self, neo_membership):
            query_membership = \
                'MATCH (a:Person{{id:"{a1}"}}) MATCH(b:Organization{{group_id: "{a2}"}}) CREATE (a)-[:MEMBER_IN]->(b);' \
                    .format(a1=neo_membership.id, a2=neo_membership.group_id)
            with self.driver.session() as session:
                session.run(query_membership)

# remove record
    def removeRecordNeo4j(self, document, keyword):
        query = f'MATCH (n:{document}{{id:"{keyword}"}}) DETACH DELETE n'
        print(query)
        with self.driver.session() as session:
            session.run(query)

# remove everything from db
    def cleanNeo4j(self):
        query = 'MATCH (n) DETACH DELETE n'
        with self.driver.session() as session:
            session.run(query)

    # execute some query at db
    def execute_neo_query(self, query, out):
        with self.driver.session() as session:
            result = session.run(query + out)
            result_list = []
            for record in result:
                rel = record[out]
                result_list.append(rel)
        return result_list


#   to work with ElasticSearch DB: initialize connection, close it, insert data, clear from data
class ES:

    def __init__(self):
        config = load_configs()
        es_url, es_port = config['es']['url'], config['es']['port']
        self.driver = Elasticsearch([{'host': es_url, 'port': es_port}])

    def close(self):
        self.driver.close()

    def insertPersonES(self, es_person):
        es_person_json = json.dumps(es_person.__dict__)
        self.driver.index(index="person", id=es_person.id, body=es_person_json)

    def insertOrganizationES(self, es_organization):
        es_organization_json = json.dumps(es_organization.__dict__)
        self.driver.index(index="organizations", id=es_organization.group_id, body=es_organization_json)

    def insertMembershipES(self, es_membership):
        es_membership_json = json.dumps(es_membership.__dict__)
        self.driver.index(index="memberships", id=es_membership.id, body=es_membership_json)

    def findall(self, f_index="person", keyword={"match_all": {}}):
        query = {"query": keyword}
        temp = self.driver.search(index=f_index, body=query, size=999)
        result = []
        print(temp)
        for i in temp['hits']['hits']:
            result.append(i['_source']['name'])
        return result

    def cleanES(self):
        self.driver.indices.delete(index='people', ignore=[400, 404])
        self.driver.indices.delete(index='organizations', ignore=[400, 404])
        self.driver.indices.delete(index='memberships', ignore=[400, 404])

    def count_recordsES(self):
        res_people = self.driver.count(index='people', ignore=[400, 404])
        res_organizations = self.driver.count(index='organizations', ignore=[400, 404])
        return res_people['count'], res_organizations['count']

# remove record
    def removeRecordES(self, index, doc):
        print('hello')
        print(doc)
        self.driver.indices.delete(index=index, body=doc)
        print('bye')
