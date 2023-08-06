#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to generate documenation based on dtFabric format definitions."""

from __future__ import print_function
import argparse
import datetime
import logging
import os
import sys

from dtfabric import errors
from dtfabric import reader
from dtfabric import registry
from dtfabric.generators import output_writers
from dtfabric.generators import template_string


class AsciidocFormatDocumentGenerator(object):
  """Asciidoc format document generator."""

  _APPENDICES_TEMPLATE_FILE = u'appendices.asciidoc'
  _BODY_TEMPLATE_FILE = u'body.asciidoc'
  _OVERVIEW_TEMPLATE_FILE = u'overview.asciidoc'
  _PREFACE_TEMPLATE_FILE = u'preface.asciidoc'

  def __init__(self, templates_path):
    """Initializes a generator.

    Args:
      templates_path (str): templates path.
    """
    super(AsciidocFormatDocumentGenerator, self).__init__()
    self._definitions_registry = registry.DataTypeDefinitionsRegistry()
    self._templates_path = templates_path
    self._template_string_generator = template_string.TemplateStringGenerator()

  def _GenerateAppendices(self, output_writer):
    """Generates appendices.

    Args:
      output_writer (OutputWriter): output writer.
    """
    template_mappings = {}

    template_filename = os.path.join(
        self._templates_path, self._APPENDICES_TEMPLATE_FILE)

    self._template_string_generator.Generate(
        template_filename, template_mappings, output_writer)

    # TODO: generate references
    # TODO: generate GFDL

  def _GenerateBody(self, output_writer):
    """Generates a body.

    Args:
      output_writer (OutputWriter): output writer.
    """
    template_mappings = {}

    template_filename = os.path.join(
        self._templates_path, self._BODY_TEMPLATE_FILE)

    self._template_string_generator.Generate(
        template_filename, template_mappings, output_writer)

    self._GenerateOverview(output_writer)

    # TODO: generate chapter per structure

  def _GetFormatDefinitions(self):
    """Retrieves the format definition.

    Returns:
      FormatDefinition: format definition.
    """
    # pylint: disable=protected-access

    if not self._definitions_registry._format_definitions:
      raise RuntimeError(u'Missing format definition.')

    if len(self._definitions_registry._format_definitions) > 1:
      raise RuntimeError(u'Unsupported multiple format definitions.')

    return self._definitions_registry.GetDefinitionByName(
        self._definitions_registry._format_definitions[0])

  def _GenerateOverview(self, output_writer):
    """Generates the overview chapter.

    Args:
      output_writer (OutputWriter): output writer.
    """
    format_definition = self._GetFormatDefinitions()

    template_mappings = {}

    summary = format_definition.metadata.get(u'summary', None)
    if summary:
      template_mappings[u'summary'] = summary

    template_filename = os.path.join(
        self._templates_path, self._OVERVIEW_TEMPLATE_FILE)

    self._template_string_generator.Generate(
        template_filename, template_mappings, output_writer)

    # TODO: generate characteristics table
    # TODO: generate overview description

  def _GeneratePreface(self, output_writer):
    """Generates a preface.

    Args:
      output_writer (OutputWriter): output writer.
    """
    format_definition = self._GetFormatDefinitions()

    template_mappings = {
        u'title': format_definition.description}

    if format_definition.description:
      template_mappings[u'abstract'] = (
          u'This document contains information about the {0:s}'.format(
              format_definition.description))

    summary = format_definition.metadata.get(u'summary', None)
    if summary:
      template_mappings[u'summary'] = summary

    authors = format_definition.metadata.get(u'authors', None)
    if authors:
      template_mappings[u'authors'] = u', '.join(authors)

    keywords = format_definition.metadata.get(u'keywords', None)
    if authors:
      template_mappings[u'keywords'] = u', '.join(keywords)

    year = format_definition.metadata.get(u'year', None)
    if year:
      date = datetime.date.today()
      if year != date.year:
        copyright_years = u'{0:d}-{1:d}'.format(year, date.year)
      else:
        copyright_years = u'{0:d}'.format(year)

      template_mappings[u'copyright'] = copyright_years

    template_filename = os.path.join(
        self._templates_path, self._PREFACE_TEMPLATE_FILE)

    self._template_string_generator.Generate(
        template_filename, template_mappings, output_writer)

  def Generate(self):
    """Generates a format document."""
    output_writer = output_writers.StdoutWriter()

    self._GeneratePreface(output_writer)
    self._GenerateBody(output_writer)
    self._GenerateAppendices(output_writer)

  def ReadDefinitions(self, path):
    """Reads the definitions form file or directory.

    Args:
      path (str): path of the definition file.
    """
    definitions_reader = reader.YAMLDataTypeDefinitionsFileReader()
    definitions_reader.ReadFile(self._definitions_registry, path)


def Main():
  """The main program function.

  Returns:
    bool: True if successful or False if not.
  """
  argument_parser = argparse.ArgumentParser(description=(
      u'Generates documentation based on dtFabric format definitions.'))

  argument_parser.add_argument(
      u'source', nargs=u'?', action=u'store', metavar=u'PATH', default=None,
      help=u'name of the file containing the dtFabric format definitions.')

  options = argument_parser.parse_args()

  if not options.source:
    print(u'Source value is missing.')
    print(u'')
    argument_parser.print_help()
    print(u'')
    return False

  if not os.path.isfile(options.source):
    print(u'No such file: {0:s}'.format(options.source))
    print(u'')
    return False

  logging.basicConfig(
      level=logging.INFO, format=u'[%(levelname)s] %(message)s')

  # TODO: allow user to set templates path
  # TODO: detect templates path
  templates_path = os.path.join(u'data')

  source_generator = AsciidocFormatDocumentGenerator(templates_path)

  try:
    source_generator.ReadDefinitions(options.source)
  except errors.FormatError as exception:
    print(u'Unable to read definitions with error: {0:s}'.format(exception))
    return False

  source_generator.Generate()

  return True


if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
