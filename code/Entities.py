# -*- coding: utf-8 -*-
from databases import Neo


class Person:

    def __init__(self, p_id, p_name, p_alias, p_email, p_nationality):
        self.id = p_id
        self.name = p_name
        self.alias = p_alias
        self.email = p_email
        self.nationality = p_nationality


class Organization:

    def __init__(self, o_group_id, o_name):
        self.group_id = o_group_id
        self.name = o_name


class Membership:

    def __init__(self, m_id, m_group_id):
        self.id = m_id
        self.group_id = m_group_id
