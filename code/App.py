# -*- coding: utf-8 -*-
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class App:
    def __init__(self, url, user, pwd):
        self.driver = GraphDatabase.driver(url, auth=(user, pwd))

    def close(self):
        self.driver.close()

    def create_nodes(self, person):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_nodes, person)
            for record in result:
                print("Created nodes {p1}".format(p1=record['p1']))

    @staticmethod
    def _create_and_return_nodes(tx, person):
        query = ("CREATE (p1:Person {name: $person.name})")
        result = tx.run(query, person.name)
        try:
            return [{"Person": record["p1"]["name"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}".format(query=query, exception=exception))
            raise
