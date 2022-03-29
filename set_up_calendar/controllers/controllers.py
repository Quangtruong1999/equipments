# -*- coding: utf-8 -*-
# from odoo import http


# class SetUpCalendar(http.Controller):
#     @http.route('/set_up_calendar/set_up_calendar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/set_up_calendar/set_up_calendar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('set_up_calendar.listing', {
#             'root': '/set_up_calendar/set_up_calendar',
#             'objects': http.request.env['set_up_calendar.set_up_calendar'].search([]),
#         })

#     @http.route('/set_up_calendar/set_up_calendar/objects/<model("set_up_calendar.set_up_calendar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('set_up_calendar.object', {
#             'object': obj
#         })
