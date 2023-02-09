import pytest

from mkpkg.lib.tabular import tabular


def test_tabular_all():
    valid_table = """| ================================= |
| Header | Header | Header | Header |
| ------ | ------ | ------ | ------ |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
| ================================= |
"""
    table = [
        ["Header", "Header", "Header", "Header"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"]
    ]
    assert tabular(table) == valid_table


def test_tabular_no_roof():
    valid_table = """| Header | Header | Header | Header |
| ------ | ------ | ------ | ------ |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
"""
    table = [
        ["Header", "Header", "Header", "Header"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"]
    ]
    assert tabular(table, roof='') == valid_table


def test_tabular_no_ceiling():
    valid_table = """| ================================= |
| Header | Header | Header | Header |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
| ================================= |
"""
    table = [
        ["Header", "Header", "Header", "Header"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"]
    ]
    assert tabular(table, ceiling='') == valid_table


def test_tabular_no_roof_no_ceiling():
    valid_table = """| Header | Header | Header | Header |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
|  item  |  item  |  item  |  item  |
"""
    table = [
        ["Header", "Header", "Header", "Header"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"]
    ]
    assert tabular(table, ceiling='', roof='') == valid_table

