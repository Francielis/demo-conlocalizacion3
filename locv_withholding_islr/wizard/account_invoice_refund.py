# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from odoo import models


class AccountInvoiceRefund(models.TransientModel):

    """Refunds invoice"""

    _inherit = 'account.invoice.refund'

    def validate_wh(self):
        """ Method that validate if invoice has non-yet processed INCOME
        withholds.
        return: True: if invoice is does not have wh's or it does have and
                      those ones are validated.
                False: if invoice is does have and those wh's are not yet
                       validated.
        """
        if self._context is None:
            context = {}
        res = []
        inv_obj = self.env['account.invoice']

        res.append(super(AccountInvoiceRefund, self).validate_wh())
        res.append(inv_obj.validate_wh_income_done())
        return all(res)

AccountInvoiceRefund()
