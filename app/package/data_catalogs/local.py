import duckdb

class DataCatalog:
    @staticmethod
    def profile(path:str):
        with duckdb.connect() as conn:
            query = f"DESCRIBE '{path}';"
            records = conn.execute(query).fetchall()
            records = [r[:2] for r in records]
            # fields = [d[0] for d in conn.description[:2]]
            # profile = [dict(zip(fields, r)) for r in records]
            # fields = [d[0] for d in conn.description[:2]]
            profile = [{"field_name": r[0], "data_type": r[1]} for r in records]
        return profile