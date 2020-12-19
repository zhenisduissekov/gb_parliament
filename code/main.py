# -*- coding: utf-8 -*-
from Entities import Person, Organization, Membership
import csv
import databases
import logger


def gb_parliament():
    counter = 0
    filename = 'gb_parliament.csv'
    # setup logger
    logging = logger.logger_config(with_file=False)
    logging.info('\n\nProgram starts..')

    # setup db connections and clean from previous data
    appES = databases.ES()
    appNeo = databases.Neo()
    appNeo.cleanNeo4j()
    # appES.cleanES()

    with open(filename, 'r') as file:
        logging.info("Reading the file {a}".format(a=filename))
        for row in csv.DictReader(file):
            person = Person(row['id'], row['name'], row['sort_name'], row['email'], 'GB')  # creating objects
            organization = Organization(row['group_id'], row['group'])
            membership = Membership(row['id'], row['group_id'])
            appNeo.insertPersonNeo4j(person)
            appNeo.insertOrganizationNeo4j(organization)
            appNeo.insertMembershipNeo4j(membership)
            appES.insertPersonES(person)
            appES.insertOrganizationES(organization)
            appES.insertMembershipES(membership)
            counter += 1

    # close connections
    appES.close()
    appNeo.close()
    logging.info(f"Records read from a file: {counter}")


if __name__ == "__main__":
    counter = 0
    gb_parliament()

