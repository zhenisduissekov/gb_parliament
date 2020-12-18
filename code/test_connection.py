# -*- coding: utf-8 -*-
import unittest
import logging


class TestConnection(unittest.TestCase):

    def test_neo4j_connection(driver):
        try:
            with driver.session() as session:
                session.run("Match () Return 1 Limit 1")
            logging.info("Connection with Neo4j is ok")
        except Exception as e:
            logging.error(f'Connection problem with Neo4j- {e}', exc_info=True)

    def test_es_connection(self):
        if not self.driver.ping():
            raise ValueError("ElasticSearch connection failed")
        else:
            logging.info('ElasticSearch connection successful')


if __name__ == "__main__":
    unittest.main()
