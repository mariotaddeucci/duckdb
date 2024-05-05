import pytest

_ = pytest.importorskip("duckdb.experimental.spark")
from duckdb.experimental.spark.sql import SparkSession


class TestSparkSession(object):
    def test_spark_session_default(self):
        SparkSession.builder.getOrCreate()

    def test_spark_session(self):
        SparkSession.builder.master("local[1]").appName('SparkByExamples.com').getOrCreate()

    def test_new_session(self, spark: SparkSession):
        spark.newSession()

    @pytest.mark.skip(reason='not tested yet')
    def test_retrieve_same_session(self):
        spark = SparkSession.builder.master('test').appName('test2').getOrCreate()
        spark2 = SparkSession.builder.getOrCreate()
        # Same connection should be returned
        assert spark == spark2

    def test_config(self):
        # Usage of config()
        (
            SparkSession.builder.master("local[1]")
            .appName("SparkByExamples.com")
            .config("spark.some.config.option", "config-value")
            .getOrCreate()
        )

    @pytest.mark.skip(reason="enableHiveSupport is not implemented yet")
    def test_hive_support(self):
        # Enabling Hive to use in Spark
        (
            SparkSession.builder.master("local[1]")
            .appName("SparkByExamples.com")
            .config("spark.sql.warehouse.dir", "<path>/spark-warehouse")
            .enableHiveSupport()
            .getOrCreate()
        )

    def test_version(self, spark):
        version = spark.version
        assert version == '1.0.0'

    def test_get_active_session(self, spark):
        spark.getActiveSession()

    def test_read(self, spark):
        pass

    def test_write(self, spark):
        spark.sql('select 42')

    def test_read_stream(self, spark):
        pass

    def test_spark_context(self, spark):
        pass

    def test_sql(self, spark):
        spark.sql('select 42')

    def test_stop_context(self, spark):
        spark.stop()

    def test_table(self, spark):
        spark.sql('create table tbl(a varchar(10))')
        spark.table('tbl')

    def test_udf(self, spark):
        with pytest.raises(NotImplementedError):
            pass
