#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import re

import six

import pytablewriter as ptw

from ._text_extractor import SqliteSchemaTextExtractorV0


class Header(object):
    ATTR_NAME = "Attribute name"
    DATA_TYPE = "Data type"
    PRIMARY_KEY = "Primary key"
    NOT_NULL = "Not NULL"
    UNIQUE = "Unique"
    INDEX = "Index"


class SqliteSchemaTableExtractorV0(SqliteSchemaTextExtractorV0):

    @property
    def verbosity_level(self):
        return 0

    @property
    def _table_writer_class(self):
        return ptw.RstSimpleTableWriter

    @property
    def _header_list(self):
        return (Header.ATTR_NAME, Header.DATA_TYPE)

    def get_table_schema_text(self, table_name):
        index_query_list = self._get_index_schema(table_name)

        value_matrix = []
        for attr_schema in self._get_attr_schema(table_name, "table"):
            values = {}
            attr_name = self._get_attr_name(attr_schema)
            re_index = re.compile(re.escape(attr_name))

            values[Header.ATTR_NAME] = attr_name
            values[Header.INDEX] = False

            for index_query in index_query_list:
                if re_index.search(index_query) is not None:
                    values[Header.INDEX] = True
                    break

            try:
                values[Header.DATA_TYPE] = self._get_attr_type(attr_schema)
            except IndexError:
                continue

            try:
                constraint = self._get_attr_constraints(attr_schema)
            except IndexError:
                continue

            values[Header.PRIMARY_KEY] = re.search(
                "PRIMARY KEY", constraint, re.IGNORECASE) is not None
            values[Header.NOT_NULL] = re.search(
                "NOT NULL", constraint, re.IGNORECASE) is not None
            values[Header.UNIQUE] = re.search(
                "UNIQUE", constraint, re.IGNORECASE) is not None

            value_matrix.append([
                values.get(header) for header in self._header_list
            ])

        writer = self._table_writer_class()
        writer.stream = six.StringIO()
        writer.table_name = self._get_display_table_name(table_name)
        writer.header_list = self._header_list
        writer.value_matrix = value_matrix
        writer._dp_extractor.const_value_mapping = {True: "X", False: ""}

        writer.write_table()

        return writer.stream.getvalue()

    def _get_display_table_name(self, table_name):
        return table_name


class SqliteSchemaTableExtractorV1(SqliteSchemaTableExtractorV0):

    @property
    def verbosity_level(self):
        return 1

    @property
    def _table_writer_class(self):
        return ptw.RstGridTableWriter

    @property
    def _header_list(self):
        return (
            Header.ATTR_NAME, Header.DATA_TYPE, Header.PRIMARY_KEY,
            Header.NOT_NULL, Header.UNIQUE, Header.INDEX,
        )

    def get_table_schema(self, table_name):
        return self._get_table_schema_v1(table_name)

    def _get_display_table_name(self, table_name):
        return "{:s} ({:d} records)".format(
            table_name, self.get_num_records(table_name))
