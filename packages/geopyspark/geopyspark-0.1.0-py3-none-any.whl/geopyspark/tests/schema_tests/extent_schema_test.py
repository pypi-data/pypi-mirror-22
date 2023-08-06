import unittest
import pytest

from pyspark import RDD
from pyspark.serializers import AutoBatchedSerializer
from geopyspark.avroserializer import AvroSerializer
from geopyspark.tests.base_test_class import BaseTestClass


class ExtentSchemaTest(BaseTestClass):
    ew = BaseTestClass.geopysc._jvm.geopyspark.geotrellis.tests.schemas.ExtentWrapper

    tup = ew.testOut(BaseTestClass.geopysc.sc)
    java_rdd = tup._1()
    ser = AvroSerializer(tup._2())

    rdd = RDD(java_rdd, BaseTestClass.geopysc.pysc, AutoBatchedSerializer(ser))
    collected = rdd.collect()

    expected_extents = [
        {"xmin": 0.0, "ymin": 0.0, "xmax": 1.0, "ymax": 1.0},
        {"xmin": 1.0, "ymin": 2.0, "xmax": 3.0, "ymax": 4.0},
        {"xmin": 5.0, "ymin": 6.0, "xmax": 7.0, "ymax": 8.0}
    ]

    @pytest.fixture(scope='class', autouse=True)
    def tearDown(self):
        yield
        BaseTestClass.geopysc.pysc._gateway.close()

    def result_checker(self, actual_result, expected_result):
        for actual, expected in zip(actual_result, expected_result):
            self.assertDictEqual(actual, expected)

    def test_encoded_extents(self):
        encoded = self.rdd.map(lambda s: s)
        actual_encoded = encoded.collect()

        self.result_checker(actual_encoded, self.expected_extents)

    def test_decoded_extents(self):
        self.result_checker(self.collected, self.expected_extents)


if __name__ == "__main__":
    unittest.main()
    BaseTestClass.geopysc.pysc.stop()
