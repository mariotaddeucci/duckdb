from datetime import time, timezone
import pytest
import datetime

pandas = pytest.importorskip("pandas")


class TestTimeTz(object):
    def test_time_tz(self, duckdb_cursor):
        pandas.DataFrame({"col1": [time(1, 2, 3, tzinfo=timezone.utc)]})

        sql = 'SELECT * FROM df'

        duckdb_cursor.execute(sql)

        res = duckdb_cursor.fetchall()
        assert res == [(datetime.time(1, 2, 3, tzinfo=datetime.timezone.utc),)]
