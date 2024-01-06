# -*- coding: utf-8 -*-
import odoo

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CollectionUserInformation(models.Model):
    _name = 'collection.user.info'
    _description = 'Collection User Information'

    request_user = fields.Integer(string='User ID', required=True)
    request_ip = fields.Char(string='Request IP', required=True)
    request_login = fields.Char(string='Request Login', required=True)
    request_db = fields.Char(string='Request Database', required=True)
    fast_login_time = fields.Datetime(string='Fast Login Time')
    latest_login_time = fields.Datetime(string='Latest Login Time')

    @api.model_cr
    def init(self):
        res = super(CollectionUserInformation, self).init()
        create_index_sql = """
            CREATE UNIQUE INDEX IF NOT EXISTS collect_user_info_request_unique_seq
            ON collection_user_info(request_ip, request_db, request_user, request_login);
        """
        self._cr.execute(create_index_sql)
        return res

class CollectionUserInformationHistory(models.Model):
    _name = 'collection.user.info.history'
    _inherit = 'collection.user.info'
    _description = 'Collection User History information '
