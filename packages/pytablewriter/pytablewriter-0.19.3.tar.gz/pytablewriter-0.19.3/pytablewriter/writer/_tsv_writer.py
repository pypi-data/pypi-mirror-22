# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .._const import FormatName
from ._csv_writer import CsvTableWriter


class TsvTableWriter(CsvTableWriter):
    """
    A table writer class for tab separated values (TSV) format.

    :Examples:

        :ref:`example-tsv-table-writer`
    """

    @property
    def format_name(self):
        return FormatName.TSV

    def __init__(self):
        super(TsvTableWriter, self).__init__()

        self.column_delimiter = "\t"
