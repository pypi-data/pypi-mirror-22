#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Windows Event Log resources classes."""

import unittest

from winevtrc import resources

from tests import test_lib as shared_test_lib


class EventLogProviderTest(shared_test_lib.BaseTestCase):
  """Tests for the Windows Event Log provider object."""

  def testSetCategoryMessageFilenames(self):
    """Tests the SetCategoryMessageFilenames function."""
    event_log_provider = resources.EventLogProvider(
        u'log_type', u'log_source', u'provider_guid')

    expected_category_message_files = [u'test1', u'test2', u'test3']

    event_log_provider.SetCategoryMessageFilenames(
        expected_category_message_files)
    self.assertEqual(
        event_log_provider.category_message_files,
        expected_category_message_files)

    event_log_provider.SetCategoryMessageFilenames(u'test1;test2;test3')
    self.assertEqual(
        event_log_provider.category_message_files,
        expected_category_message_files)

  def testSetEventMessageFilenames(self):
    """Tests the SetEventMessageFilenames function."""
    event_log_provider = resources.EventLogProvider(
        u'log_type', u'log_source', u'provider_guid')

    expected_event_message_files = [u'test1', u'test2', u'test3']

    event_log_provider.SetEventMessageFilenames(
        expected_event_message_files)
    self.assertEqual(
        event_log_provider.event_message_files,
        expected_event_message_files)

    event_log_provider.SetEventMessageFilenames(u'test1;test2;test3')
    self.assertEqual(
        event_log_provider.event_message_files,
        expected_event_message_files)

  def testSetParameterMessageFilenames(self):
    """Tests the SetParameterMessageFilenames function."""
    event_log_provider = resources.EventLogProvider(
        u'log_type', u'log_source', u'provider_guid')

    expected_parameter_message_files = [u'test1', u'test2', u'test3']

    event_log_provider.SetParameterMessageFilenames(
        expected_parameter_message_files)
    self.assertEqual(
        event_log_provider.parameter_message_files,
        expected_parameter_message_files)

    event_log_provider.SetParameterMessageFilenames(u'test1;test2;test3')
    self.assertEqual(
        event_log_provider.parameter_message_files,
        expected_parameter_message_files)


class MessageFileTest(shared_test_lib.BaseTestCase):
  """Tests for the Windows Event Log message file  object."""

  def testMessageTable(self):
    """Tests the AppendMessageTable and GetMessageTable functions."""
    message_file = resources.MessageFile(u'test')

    message_file.AppendMessageTable(5, u'1.2.3.4')

    message_table = message_file.GetMessageTable(5)
    self.assertIsNotNone(message_table)

    message_table = message_file.GetMessageTable(6)
    self.assertIsNone(message_table)

    message_tables = list(message_file.GetMessageTables())
    self.assertEqual(len(message_tables), 1)

  def testStringTable(self):
    """Tests the AppendStringTable and GetStringTable functions."""
    message_file = resources.MessageFile(u'test')

    message_file.AppendStringTable(5, u'1.2.3.4')

    string_table = message_file.GetStringTable(5)
    self.assertIsNotNone(string_table)

    string_table = message_file.GetStringTable(6)
    self.assertIsNone(string_table)

    string_tables = list(message_file.GetStringTables())
    self.assertEqual(len(string_tables), 1)


if __name__ == '__main__':
  unittest.main()
