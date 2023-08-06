import os
import unittest
import pytest
import numpy as np

from pyspark import RDD
from pyspark.serializers import AutoBatchedSerializer
from geopyspark.avroserializer import AvroSerializer
from geopyspark.avroregistry import AvroRegistry
from geopyspark.tests.base_test_class import BaseTestClass


def decoder(x):
    tup_decoder = AvroRegistry.tuple_decoder
    tile_decoder = AvroRegistry.tile_decoder

    return tup_decoder(x, key_decoder=tile_decoder)

def encoder(x):
    tup_encoder = AvroRegistry.tuple_encoder
    tile_encoder = AvroRegistry.tile_encoder

    return tup_encoder(x, key_encoder=tile_encoder)


class TupleSchemaTest(BaseTestClass):
    extents = [
        {'xmin': 0, 'ymin': 0, 'xmax': 1, 'ymax': 1},
        {'xmin': 1, 'ymin': 2, 'xmax': 3, 'ymax': 4},
        {'xmin': 5, 'ymin': 6, 'xmax': 7, 'ymax': 8}
    ]

    arrs = [
        {'data': np.array([0, 1, 2, 3, 4, 5]).reshape(1, 3, 2), 'no_data_value': -2147483648},
        {'data': np.array([0, 1, 2, 3, 4, 5]).reshape(1, 2, 3), 'no_data_value': -2147483648},
        {'data': np.array([0, 1, 2, 3, 4, 5]).reshape(1, 6, 1), 'no_data_value': -2147483648}
    ]

    sc = BaseTestClass.geopysc.pysc._jsc.sc()
    ew = BaseTestClass.geopysc.pysc._jvm.geopyspark.geotrellis.tests.schemas.TupleWrapper

    tup = ew.testOut(sc)
    java_rdd = tup._1()

    ser = AvroSerializer(tup._2(), decoder, encoder)
    rdd = RDD(java_rdd, BaseTestClass.geopysc.pysc, AutoBatchedSerializer(ser))
    collected = rdd.collect()

    @pytest.mark.skipif('TRAVIS' in os.environ,
                         reason="Encoding using methods in Main causes issues on Travis")
    def test_encoded_tuples(self):
        s = self.rdd._jrdd_deserializer.serializer

        encoded = self.rdd.map(lambda x: encoder(x))
        actual_encoded = encoded.collect()

        expected_encoded = [
            {'_1': AvroRegistry.tile_encoder(self.arrs[0]), '_2': self.extents[0]},
            {'_1': AvroRegistry.tile_encoder(self.arrs[1]), '_2': self.extents[1]},
            {'_1': AvroRegistry.tile_encoder(self.arrs[2]), '_2': self.extents[2]}
        ]

        for actual, expected in zip(actual_encoded, expected_encoded):
            self.assertDictEqual(actual, expected)

    def test_decoded_tuples(self):
        expected_tuples = [
            (self.arrs[0], self.extents[0]),
            (self.arrs[1], self.extents[1]),
            (self.arrs[2], self.extents[2])
        ]

        for actual, expected in zip(self.collected, expected_tuples):
            (actual_tile, actual_extent) = actual
            (expected_tile, expected_extent) = expected

            self.assertTrue((actual_tile['data'] == expected_tile['data']).all())
            self.assertDictEqual(actual_extent, expected_extent)


if __name__ == "__main__":
    unittest.main()
