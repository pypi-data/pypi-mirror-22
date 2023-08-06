# -*- coding: utf-8 -*-
"""Tests for the dtFabric helper objects."""

import unittest

from dtfabric.runtime import fabric

from tests import test_lib


class DataTypeFabricTest(test_lib.BaseTestCase):
  """Data type fabric tests."""

  @test_lib.skipUnlessHasTestFile([u'integer.yaml'])
  def testInitialize(self):
    """Tests the __init__ function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    with open(definitions_file, 'rb') as file_object:
      yaml_definition = file_object.read()

    factory = fabric.DataTypeFabric(yaml_definition=yaml_definition)
    self.assertIsNotNone(factory)


if __name__ == '__main__':
  unittest.main()
