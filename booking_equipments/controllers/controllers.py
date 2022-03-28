# -*- coding: utf-8 -*-
# from odoo import http


# class BookingEquipments(http.Controller):
#     @http.route('/booking_equipments/booking_equipments', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_equipments/booking_equipments/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_equipments.listing', {
#             'root': '/booking_equipments/booking_equipments',
#             'objects': http.request.env['booking_equipments.booking_equipments'].search([]),
#         })

#     @http.route('/booking_equipments/booking_equipments/objects/<model("booking_equipments.booking_equipments"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_equipments.object', {
#             'object': obj
#         })
