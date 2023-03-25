""" Tabular
Author:      Perry Bunn
email:       perry.bunn@noaa.gov
Description: This file is the methods called when mkpkg formats 2d list to
             tables
"""

from math import floor, ceil


def tabular(d2_array: list[list], ceiling="-", roof='=', walls='|') -> str:
    """
    Flow
    1. for row in 2d array enumerate
      a. check that width is consistent
      b. for column in row enumerate
        i. update max column width
    2. for each row
      a. for column in row
       i. make aligned version_flag of column text
      b. make row text with walls
    3. return table text

    Parameters
    ----------
    d2_array
    ceiling
    roof
    walls

    Returns
    -------
    str
    """
    columns = -1
    table_width = -1
    max_column_width = {}
    for i, row in enumerate(d2_array):
        if columns == -1:
            columns = len(row)
            table_width = columns * 2 + 1
        else:
            assert columns == len(row)
        # max_column_width[i] = 0
        for j, column in enumerate(row):
            if max_column_width.get(j, None) is None:
                max_column_width[j] = 0
            if max_column_width.get(j) < len(column):
                # Add the difference to the table width
                table_width = table_width + (len(column) - max_column_width[j])
                max_column_width[j] = len(column)
            # else:
            #     table_width = table_width + len(column)

    table = ''
    if roof.strip():
        table = f"{walls} {roof*(table_width+columns - 4)} {walls}\n"
    for i, row in enumerate(d2_array):
        row_text = f"{walls}"
        head_text = f"{walls}"
        for j, column in enumerate(row):
            if ceiling:
                head_text = f"{head_text} {ceiling*max_column_width[j]} {walls}"
            left_space = floor((max_column_width[j] - len(column)) / 2)
            right_space = ceil((max_column_width[j] - len(column)) / 2)
            col = f"{' '*left_space} {column} {' '*right_space}"
            row_text = f"{row_text}{col}{walls}"
        if ceiling and i == 1:
            table = f"{table}{head_text}\n"
        table = f"{table}{row_text}\n"
    if roof.strip():
        table = f"{table}{walls} {roof*(table_width+columns - 4)} {walls}\n"
    return table

# 0         1         2         3
# 0123456789012345678901234567890123456
#   012345
# | Header | Header | Header | Header |
# | ------ | ------ | ------ | ------ |
# |  item  |  item  |  item  |  item  |
# |  item  |  item  |  item  |  item  |
# |  item  |  item  |  item  |  item  |
# |  item  |  item  |  item  |  item  |


def main():
    """ entry point for quick testing """
    table = [
        ["Header", "Header", "Header", "Header"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"],
        ["item", "item", "item", "item"]
    ]
    print(tabular(table))


if __name__ == '__main__':
    main()
