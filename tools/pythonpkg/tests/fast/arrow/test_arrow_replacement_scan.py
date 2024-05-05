import os

import duckdb
import pytest

try:
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq

    can_run = True
except Exception:
    can_run = False


class TestArrowReplacementScan(object):
    def test_arrow_table_replacement_scan(self, duckdb_cursor):
        if not can_run:
            return

        parquet_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "userdata1.parquet")
        userdata_parquet_table = pq.read_table(parquet_filename)
        userdata_parquet_table.to_pandas()

        con = duckdb.connect()

        for i in range(5):
            assert con.execute("select count(*) from userdata_parquet_table").fetchone() == (1000,)
            assert con.execute("select count(*) from df").fetchone() == (1000,)

    def test_arrow_table_replacement_scan_view(self, duckdb_cursor):
        if not can_run:
            return

        parquet_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "userdata1.parquet")
        userdata_parquet_table = pq.read_table(parquet_filename)

        con = duckdb.connect()

        con.execute("create view x as select * from userdata_parquet_table")
        del userdata_parquet_table
        with pytest.raises(
            duckdb.CatalogException,
            match="Table with name userdata_parquet_table does not exist",
        ):
            assert con.execute("select count(*) from x").fetchone()

    def test_arrow_dataset_replacement_scan(self, duckdb_cursor):
        if not can_run:
            return
        parquet_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "userdata1.parquet")
        pq.read_table(parquet_filename)
        ds.dataset(parquet_filename)

        con = duckdb.connect()
        assert con.execute("select count(*) from userdata_parquet_dataset").fetchone() == (1000,)
