from .database_types import *
from .base import ThreadedDatabase, import_helper
from .base import (
    MD5_HEXDIGITS,
    CHECKSUM_HEXDIGITS,
    _CHECKSUM_BITSIZE,
    TIMESTAMP_PRECISION_POS,
)


@import_helper("duckdb")
def import_duckdb():
    import duckdb

    return duckdb


class DuckDb(ThreadedDatabase):
    TYPE_CLASSES = {
        "TIMESTAMPTZ": TimestampTZ,
        "TIMESTAMP": Timestamp,
        "DOUBLE": Float,
        "REAL": Float,
        "DECIMAL": Decimal,
        "INTEGER": Integer,
        "BIGINT": Integer,
        "VARCHAR": Text,
        "UUID": Native_UUID,
    }
    ROUNDS_ON_PREC_LOSS = True

    def __init__(self, *, thread_count, **kw):
        self._args = kw

        super().__init__(thread_count=thread_count)

    def create_connection(self):
        ddb = import_duckdb()
        conn = ddb.connect(database=":memory:")
        # Create a schema and  table from the input file.
        conn.execute("CREATE SCHEMA dd;")
        conn.execute(
            f"CREATE TABLE dd.{self._args['table_name']} AS SELECT * FROM '{self._args['file_path']}';"
        )
        return conn

    def quote(self, s: str):
        return s

    def md5_to_int(self, s: str) -> str:
        return f"('x' || substring(md5({s}), {1+MD5_HEXDIGITS-CHECKSUM_HEXDIGITS}))::bit({_CHECKSUM_BITSIZE})::bigint"

    def to_string(self, s: str):
        return f"{s}::varchar"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        if coltype.rounds:
            return f"to_char({value}::timestamp({coltype.precision}), 'YYYY-mm-dd HH24:MI:SS.US')"

        timestamp6 = f"to_char({value}::timestamp(6), 'YYYY-mm-dd HH24:MI:SS.US')"
        return f"RPAD(LEFT({timestamp6}, {TIMESTAMP_PRECISION_POS+coltype.precision}), {TIMESTAMP_PRECISION_POS+6}, '0')"

    def normalize_number(self, value: str, coltype: FractionalType) -> str:
        return self.to_string(f"{value}::decimal(38, {coltype.precision})")

    def parse_table_name(self, name: str) -> DbPath:
        return name

    def select_table_schema(self, path: DbPath) -> str:
        return f"SELECT column_name, data_type, datetime_precision, numeric_precision, numeric_scale FROM information_schema.columns WHERE table_name = '{self._args['table_name']}';"
