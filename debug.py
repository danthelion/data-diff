import logging

logging.basicConfig(level=logging.INFO)

from data_diff import connect_to_table, diff_tables

table1 = connect_to_table(
    db_info="duckdb:///Users/daniel.palma/Personal/data-diff/dev/ratings.csv",
    table_name="dd",
    key_column="userId",
)

table2 = connect_to_table(
    db_info="duckdb:///Users/daniel.palma/Personal/data-diff/dev/ratings.parquet",
    table_name="xx",
    key_column="userId",
)

for different_row in diff_tables(table1, table2, key_column="userId"):
    plus_or_minus, columns = different_row
    print(plus_or_minus, columns)

# Test
# poetry run python3 -m data_diff duckdb:///Users/daniel.palma/Personal/data-diff/dev/ratings.parquet ratings postgresql://postgres:Password1@localhost/postgres rating -k userid --verbose --debug
# poetry run python3 -m data_diff duckdb:///Users/daniel.palma/Personal/data-diff/dev/ratings.csv ratings postgresql://postgres:Password1@localhost/postgres rating -k userid --verbose --debug
