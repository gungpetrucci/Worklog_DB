import unittest
from unittest.mock import patch
from peewee import *
from os import remove
from playhouse.test_utils import test_database

import worklog_DB

TEST_DB =SqliteDatabase('worklog.db')
TEST_DB.connect()
TEST_DB.create_table(worklog_DB.Entry, safe=True)

Entry = worklog_DB.Entry

ENTRIES = [
    {
        'entry_id' : 1,
        'employee' : 'Steve Jobs',
        'date' : '20121025',
        'taskname' : 'Making new iPhone7',
        'timespent' : 450,
        'detail' : 'Coding a test file for the new phone'
    },
    {
        'entry_id' : 2,
        'employee' : 'Bill Gates',
        'date' : '20100811',
        'taskname' : 'Telephone meeting',
        'timespent' : 25,
        'detail' : 'Meeting so bored'
        },
    {
        'entry_id' : 3,
        'employee' : 'Mark Zuckerberg',
        'date' : '20140105',
        'taskname' : 'Family time',
        'timespent' : 125,
        'detail' : 'Good morning!'
        }
    ]

for row in ENTRIES:
    Entry.create(**row)


class WorklogTest(unittest.TestCase):
        

    def test_data_entry(self):
        self.assertEqual('Steve Jobs', Entry.get(Entry.entry_id == 1).employee)
        self.assertEqual('Making new iPhone7', Entry.get(Entry.entry_id == 1).taskname)
        self.assertEqual(450, Entry.get(Entry.entry_id == 1).timespent)
        self.assertIn('Coding a test file for the new phone', Entry.get(Entry.entry_id == 1).detail)

    def test_check_id_true(self):
        assert worklog_DB.id_check(1) == True
        assert worklog_DB.id_check('error') == 2
        assert worklog_DB.id_check(999999) == False

    def test_id_generator(self):

        max_id = 0
        for row in Entry:
            if row.entry_id > max_id:
                max_id = row.entry_id
        assert worklog_DB.id_generator() == max_id+1


    def test_search_employee(self):
        with patch('builtins.input', side_effect=['jobs']):
            self.assertEqual(len(worklog_DB.search_employee()), 1)
        with patch('builtins.input', side_effect=['berg']):
            self.assertEqual(len(worklog_DB.search_employee()), 1)
        with patch('builtins.input', side_effect=['df']):
            self.assertEqual(worklog_DB.search_employee(), None)


    def test_search_date(self):
        with patch('builtins.input', side_effect=['20100801', '20121026']):
            self.assertEqual(len(worklog_DB.search_date()), 2)
        with patch('builtins.input', side_effect=['20140101', '20140126']):
            self.assertEqual(len(worklog_DB.search_date()), 1)
        with patch('builtins.input', side_effect=['201460101', '20160126']):
            self.assertEqual(worklog_DB.search_date(), None)
            

    def test_search_minute(self):
        with patch('builtins.input', side_effect=['25', '30']):
            self.assertEqual(len(worklog_DB.search_minute()), 1)
        with patch('builtins.input', side_effect=['500', '1000']):
            self.assertEqual(worklog_DB.search_minute(), None)

    def test_search_pattern(self):
        with patch('builtins.input', side_effect=['\w+']):
            self.assertEqual(len(worklog_DB.search_pattern()), 3)
        with patch('builtins.input', side_effect=['\w+\d']):
            self.assertEqual(len(worklog_DB.search_pattern()), 1)
        with patch('builtins.input', side_effect=['\d\d\d']):
            self.assertEqual(worklog_DB.search_pattern(), None)

    def test_search_text(self):
        with patch('builtins.input', side_effect=['phone']):
            self.assertEqual(len(worklog_DB.search_text()), 2)
        with patch('builtins.input', side_effect=['morning']):
            self.assertEqual(len(worklog_DB.search_text()), 1)
        with patch('builtins.input', side_effect=['ing']):
            self.assertEqual(len(worklog_DB.search_text()), 3)
        with patch('builtins.input', side_effect=['mlp']):
            self.assertEqual(worklog_DB.search_text(), None)
        

             

        
if __name__ == '__main__':
    unittest.main()


        
                                
        
