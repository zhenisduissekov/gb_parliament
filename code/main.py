# -*- coding: utf-8 -*-
import csv
import App
import Person
import Membership
import Organization
from neo4j import GraphDatabase
from elasticsearch import Elasticsearch


def cleanNeo4j():
    Q = 'MATCH (n) DETACH DELETE n'
    print(Q)
    with driver.session() as session:
        session.run(Q)


def insertNeo4j(person, organization, membership, limit=100):
    query_person = 'MERGE (a:Person {{id: "{a1}",name: "{a2}", sort_name: "{a3}", email: "{a4}", nationality: "GB"}})'.format(
        a1=person.id, a2=person.name, a3=person.alias, a4=person.email)
    query_organization = 'MERGE (b:Organization {{group_id: "{a1}", name: "{a2}"}})'.format(
        a1=organization.group_id, a2=organization.name)
    query_membership = 'MATCH (a:Person), (b:Organization) CREATE (a)-[r:MEMBERSHIP]->(b) RETURN type(r)'
    with driver.session() as session:
        session.run(query_person)
        session.run(query_organization)
        # session.run(query_membership)


driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "a123456+"))
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# cleanNeo4j()
print('start')
with open('gb_parliament.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    for row in csv.DictReader(file):

        print(row)
        person = Person.Person(row['id'], row['name'], row['sort_name'], row['email'], 'GB')
        organization = Organization.Organization(row['group_id'], row['group'])
        membership = Membership.Membership(row['id'], row['group_id'])
        print(organization.group_id, organization.name)
        insertNeo4j(person, organization, membership)







