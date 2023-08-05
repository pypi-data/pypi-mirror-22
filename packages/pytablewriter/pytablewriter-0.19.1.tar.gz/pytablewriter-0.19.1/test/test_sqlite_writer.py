# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
from decimal import Decimal
import itertools

from pytablereader import TableData
import pytest

import pytablereader as ptr
import pytablewriter as ptw

from .data import (
    header_list,
    value_matrix,
    mix_header_list,
    mix_value_matrix,
    value_matrix_iter
)


inf = Decimal('Infinity')
nan = None

Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="tablename",
        header=header_list,
        value=value_matrix,
        expected=TableData(
            "tablename",
            ["a", "b", "c", "dd", "e"],
            [
                [1, 123.1, "a", 1,   1],
                [2, 2.2, "bb", 2.2, 2.2],
                [3, 3.3, "ccc", 3,   "cccc"],
            ])
    ),
    Data(
        table="mix_data",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=TableData(
            "mix_data",
            [
                'i', 'f', 'c', 'if', 'ifc', 'bool',
                'inf', 'nan', 'mix_num', 'time',
            ],
            [
                [
                    1, "1.1", 'aa', 1, 1, 1, inf,
                    nan, 1, '2017-01-01T00:00:00',
                ],
                [
                    2, "2.2", 'bbb', "2.2", "2.2", 0, inf, nan,
                    inf, '2017-01-02 03:04:05+09:00',
                ],
                [
                    3, "3.33", 'cccc', -3, 'ccc', 1, inf,
                    nan, nan, '2017-01-01T00:00:00',
                ],
            ])
    ),
    Data(
        table="infnan",
        header=["inf", "nan"],
        value=[
            [inf, float("nan")],
            ["inf", "nan"],
            ["INF", "NAN"],
            ["INFINITY", "inf"],
        ],
        expected=TableData(
            "infnan",
            ["inf", "nan"],
            [
                [inf, nan],
                [inf, nan],
                [inf, nan],
                [inf, inf],
            ]
        )
    ),
]

exception_test_data_list = [
    Data(
        table="",
        header=header_list,
        value=value_matrix,
        expected=ptw.EmptyTableNameError
    ),
    Data(
        table="dummy",
        header=[],
        value=value_matrix,
        expected=ptw.EmptyHeaderError
    ),
    Data(
        table="dummy",
        header=None,
        value=value_matrix,
        expected=ptw.EmptyHeaderError
    ),
    Data(
        table="dummy",
        header=[],
        value=[],
        expected=ptw.EmptyTableDataError
    ),
    Data(
        table="dummy",
        header=header_list,
        value=[],
        expected=ptw.EmptyValueError
    ),
]


class Test_SqliteTableWriter_write_table:

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ]
    )
    def test_normal(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.sqlite")

        writer = ptw.SqliteTableWriter()
        writer.open(str(test_file_path))
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()
        writer.close()

        print("!!", value)

        loader = ptr.SqliteFileLoader(str(test_file_path))

        for tabledata in loader.load():
            #expected_dump = ptw.dump_tabledata(expected)
            #actual_dump = ptw.dump_tabledata(tabledata)

            print("expected:\n{}".format(expected))
            print("actual:\n{}".format(tabledata))

            assert tabledata == expected

            """
            print("expected:\n{}".format(expected_dump))
            print("actual:\n{}".format(actual_dump))

            assert actual_dump == expected_dump
            """

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ]
    )
    def test_exception(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.sqlite")

        writer = ptw.SqliteTableWriter()
        writer.open(str(test_file_path))
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_SqliteTableWriter_write_table_iter:

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                TableData(
                    table_name=u'tablename',
                    header_list=[u'ha', u'hb', u'hc'],
                    record_list=[
                        [1.0, 2.0, 3.0],
                        [11.0, 12.0, 13.0],
                        [1.0, 2.0, 3.0],
                        [11.0, 12.0, 13.0],
                        [101.0, 102.0, 103.0],
                        [1001.0, 1002.0, 1003.0],
                    ]),
            ]
        ])
    def test_normal(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.sqlite")

        writer = ptw.SqliteTableWriter()
        writer.open(str(test_file_path))
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        writer.close()

        loader = ptr.SqliteFileLoader(str(test_file_path))

        for tabledata in loader.load():
            assert tabledata == expected

    """
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ]
    )
    def test_exception_null_sheet(
            self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.sqlite")

        writer = ptw.SqliteTableWriter()
        writer.table_name = table
        writer.open(str(test_file_path))
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(IOError):
            writer.write_table_iter()
    """
