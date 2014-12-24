# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009 Sharoon Thomas
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp.osv import osv, fields
from openerp.osv import fields
import logging
_logger = logging.getLogger(__name__)


class email_template(osv.osv):
    _inherit = "email.template"

    _columns = {
        'send_invoice_attachments': fields.boolean('Send Invoice Attachments?', help='On the Account Invoice email composition wizard, attach also all attachments related to a particluer Invoice'),      
    }
    def get_invoice_attachments(self, cr, uid, template_id, res_id, context=None):
        attachment_ids = self.pool.get('ir.attachment').search(cr, uid, [('res_model','=','account.invoice'),('res_id','=',res_id)], context=context)
        return attachment_ids

    def generate_email_batch(self, cr, uid, template_id, res_ids, context=None, fields=None):                  
        values = super(email_template, self).generate_email_batch(cr, uid, template_id, res_ids, context=context,fields=fields)
        template = self.get_email_template(cr, uid, template_id, res_ids[0], context)
        if template.send_invoice_attachments:
            invoice_attachment_ids = self.get_invoice_attachments(cr, uid, template_id, res_ids[0], context=context)
            values[res_ids[0]]['attachment_ids'].extend(invoice_attachment_ids)
        return values


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
