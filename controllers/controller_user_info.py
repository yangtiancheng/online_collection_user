# -*- coding: utf-8 -*-

import odoo
from odoo import http
from odoo.http import request
from odoo import exceptions, _
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, route, Response
from odoo.addons.bus.controllers.main import BusController
from odoo.addons.web.controllers.main import Home


class BusControllerInherit(BusController):
    # 存活检测 longpolling
    @route()
    def poll(self, channels, last, options=None):
        self.collection_current_users()
        res = super(BusControllerInherit, self).poll(channels, last, options)
        return res
    @staticmethod
    def collection_current_users():
        request_ip = request.httprequest.remote_addr
        request_db = request.httprequest.session.db
        request_user = request.httprequest.session.uid
        request_login = request.httprequest.session.login

        try:
            conn = odoo.sql_db.db_connect(request_db)
            with conn.cursor() as cr:
                sql = """
                    insert into collection_user_info(request_ip, request_db, request_user, request_login, fast_login_time, latest_login_time)
                    values (%s, %s, %s, %s, now(), now())
                    on conflict (request_ip, request_db, request_user, request_login) do update set latest_login_time = now();
                """
                cr.execute(sql, (request_ip, request_db, request_user, request_login))
        except Exception as e:
            raise e

class HomeInherit(Home):
    # 记录登录或者session存在时自动登录的情况
    @http.route()
    def web_client(self, s_action=None, **kw):
        res = super(HomeInherit, self).web_client(s_action, **kw)
        if isinstance(res, Response) and res.status_code == 200:
            BusControllerInherit.collection_current_users()
        return res



