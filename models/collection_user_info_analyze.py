# -*- coding: utf-8 -*-
import odoo

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CollectionUserInformationAnalyze(models.Model):
    _name = 'collection.user.info.analyze'
    _description = 'Collection User Information Analyze'
    _auto = False
    _table = 'collection_user_info_analyze'

    id = fields.Integer(string='ID')
    name = fields.Char(string="Name")
    latest_all_num = fields.Integer(string='Latest All Num')
    latest_all_unique_num = fields.Integer(string='Latest All UNum')
    latest_30_num = fields.Integer(string='Latest 30 Num')
    latest_30_unique_num = fields.Integer(string='Latest 30 UNum')
    latest_7_num = fields.Integer(string='Latest 7 Num')
    latest_7_unique_num = fields.Integer(string='Latest 7 UNum')
    latest_3_num = fields.Integer(string='Latest 3 Num')
    latest_3_unique_num = fields.Integer(string='Latest 3 UNum')
    today_num = fields.Integer(string='Today NUM')
    today_unique_num = fields.Integer(string='Today UNUM')


    @api.model
    def action_open_report(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'collection.user.info.analyze',
            'view_id': self.env.ref('online_collection_user.from_collection_user_info_analyze').id,
            'target': 'new',
            'context': self._context.copy(),
        }
    @api.model_cr
    def init(self):
        res = super(CollectionUserInformationAnalyze, self).init()
        create_index_sql = """
            DROP VIEW IF EXISTS collection_user_info_analyze;
            CREATE OR REPLACE VIEW collection_user_info_analyze AS 
            SELECT 
                1 AS id,
                'Collection User Info Analyze' AS name,
              COUNT(request_user) AS latest_all_num,
              COUNT(DISTINCT request_user) AS latest_all_unique_num,
              COUNT(request_user) FILTER (WHERE latest_login_time >= CURRENT_DATE - INTERVAL '30 days') AS latest_30_num,
              COUNT(DISTINCT request_user) FILTER (WHERE latest_login_time >= CURRENT_DATE - INTERVAL '30 days') AS latest_30_unique_num,
              COUNT(request_user) FILTER (WHERE latest_login_time >= CURRENT_DATE - INTERVAL '7 days') AS latest_7_num,
              COUNT(DISTINCT request_user) FILTER (WHERE latest_login_time >= CURRENT_DATE - INTERVAL '7 days') AS latest_7_unique_num,
              COUNT(request_user) FILTER (WHERE latest_login_time >= CURRENT_DATE - INTERVAL '3 days') AS latest_3_num,
              COUNT(DISTINCT request_user) FILTER (WHERE latest_login_time >= CURRENT_DATE - INTERVAL '3 days') AS latest_3_unique_num,
              COUNT(request_user) FILTER (WHERE latest_login_time >= to_timestamp(CURRENT_DATE::VARCHAR,'YYYY-MM-DD')) AS today_num,
              COUNT(DISTINCT request_user) FILTER (WHERE latest_login_time >= to_timestamp(CURRENT_DATE::VARCHAR,'YYYY-MM-DD')) AS today_unique_num
            FROM collection_user_info cui;
        """
        self._cr.execute(create_index_sql)
        return res
