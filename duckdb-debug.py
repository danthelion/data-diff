import duckdb

con = duckdb.connect(database=":memory:")

PATH = '/Users/daniel.palma/Personal/data-diff/dev/ratings.csv'



ctas = con.execute(f"CREATE TABLE dd AS SELECT * FROM '{PATH}';")

#res = con.execute(f"SELECT * FROM 'dd';")

schema = con.execute("SELECT * FROM information_schema.columns WHERE table_name = 'dd';")

for r in schema.fetchall():
    print(dict([x for x in zip([c[0] for c in con.description], r)]))



