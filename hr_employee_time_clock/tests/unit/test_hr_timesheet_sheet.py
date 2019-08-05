# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase
from datetime import datetime, timedelta, date
from odoo import api, fields, models, _


class TestTimesheet(TransactionCase):

    def test_timesheet_1(self):
        '''
        Method for testing base function of Timesheet
        '''
        # Create a timesheet project with the test
        test_timesheet = self.env['hr_timesheet_sheet.sheet'].create({
                            'employee_id': 2,
                            'date_from': datetime.now().replace(day=1),
                            'date_to': datetime.now().replace(day=30)
        })
        # check creation timesheet
        self.assertEqual(test_timesheet.state, 'draft')
        print('Test timesheet was succesfull created!')

        # Write a timesheet project with the test
        test_timesheet.write({
                            'employee_id': 2,
                            'date_from': datetime.now().replace(day=5),
                            'date_to': datetime.now().replace(day=25)
        })
        # check creation timesheet
        self.assertEqual(test_timesheet.date_from, '2019-08-05')
        self.assertEqual(test_timesheet.date_to, '2019-08-25')
        print('Test timesheet was succesfull rewrite!')

        print('Your test was succesfull!')