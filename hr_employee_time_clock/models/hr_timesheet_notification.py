# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 - now Bytebrand Outsourcing AG (<http://www.bytebrand.net>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class HrTimesheetDh(models.Model):

    _inherit = 'hr_timesheet_sheet.sheet'

    @api.multi
    def check_last_day(self):
        for sheet in self:
            function_call = True
            ctx = self.env.context.copy()
            ctx['online_analysis'] = True
            data = self.with_context(ctx).attendance_analysis(
                timesheet_id=sheet.id, function_call=function_call)
            values = []
            keys = (_('Date'), _('Duty Hours'), _('Worked Hours'),
                    _('Difference'), _('Running'))
            a = ('previous_month_diff', 'hours', 'total')
            for k in a:
                v = data.get(k)
                if isinstance(v, list):
                    for res in v:
                        values.append([res.get(key) for key in keys])

                    date_format, time_format = self._get_user_datetime_format()
                    sheet_date_to = datetime.strptime(values[-1][0], date_format).date()
                    if sheet_date_to == datetime.today().date():
                        ir_model_data = self.env['ir.model.data']
                        template_id = \
                            ir_model_data.get_object_reference(
                                'hr_employee_time_clock',
                                'email_template_last_day_notification')[1]
                        mail_template = self.env['mail.template'].browse(
                            template_id)
                        mail_template.send_mail(res_id=sheet.id,
                                                force_send=True)

    @api.model
    def recompute_last_day_notification(self):
        hr_timesheet_sheets = self.env['hr_timesheet_sheet.sheet'].search([
            ('state', '!=', 'done')])
        for hr_timesheet_sheet in hr_timesheet_sheets:
            hr_timesheet_sheet.check_last_day()