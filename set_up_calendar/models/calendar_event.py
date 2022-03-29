from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class CalendarEvent(models.Model):
    # _name = 'set.up.calender'
    _inherit = 'calendar.event'
    _description = 'Description'

    equipment = fields.Many2many(
        comodel_name='equipment.manager',
        column1='',
        column2='id',
        string='Equipment',
        index=True,
        store=True
    )

    # còn lỗi
    def check_duplicate(self, start, stop, values):
        print('check check check')
        print(start)
        print(stop)
        all_record_booking = self.env['booking.history'].sudo().search(
            ['|','&',('start', '>=', start),  ('start', '<=', stop),'&', ('start', '<=', start), ('stop', '>=', start)]
        )

        for eq in all_record_booking:
            if eq.equipment_id.ids[0] in values:
                return False
        print('all_record_booking = ', all_record_booking)
        # print('start = ', datetime.fromisoformat(start))
        # if all_record_booking:
        #     return False
        return True

    @api.model
    def create(self, vals):
        print('values of order = ', vals)
        print('equipments get = ', vals.get('equipment')[0][2])
        if not self.check_duplicate(vals.get('start'), vals.get('stop'), vals.get('equipment')[0][2]):
            raise UserError(_("Trùng lịch"))

        result = super(CalendarEvent, self).create(vals)
        print('result = ', result)
        for equip in vals.get('equipment')[0][2]:
            value = {
                'start': vals.get('start'),
                'stop': vals.get('stop'),
                'duration': vals.get('duration'),
                'user_id': vals.get('user_id'),
                'equipment_id': equip,
                'calendar_event_id': result.id
            }
            print('value = ', value)
            self.env['booking.history'].create(value)
        return result

    def write(self, vals):
        ### Cập nhật sau phần chỉnh sửa thêm thiết bị
        # print('values of write = ', vals)
        # print('self = ', self)
        # print('equipments get write = ', vals.get('equipment')[0][2])
        # for equip in vals.get('equipment')[0][2]:
        #     all_record_booking = self.env['booking.history'].sudo().search([])
        #     print('all_record_booking = ', all_record_booking)
        #     for equipment in vals.get('equipment')[0][2]:
        #         for record in all_record_booking:
        #             if self.id == record.calendar_event_id.id:
        #                 if equipment != record.equipment_id.id:
        #                     if (self.start >= record.start and record.stop >= self.start) or (
        #                             self.stop >= record.stop and self.stop >= record.start):
        #                         raise UserError(_("Thiết bị %s đã được sử dụng", record.equipment_id.name))
        #             else:
        #                 if equipment == record.equipment_id.id:
        #                     if (self.start >= record.start and record.stop >= self.start) or (
        #                             self.stop >= record.stop and self.stop >= record.start):
        #                         raise UserError(_("Thiết bị này đã được sử dụng"))
        #
        #     value = {
        #         # 'start': vals.get('start'),
        #         # 'stop': vals.get('stop'),
        #         # 'duration': vals.get('duration'),
        #         # 'user_id': vals.get('user_id'),
        #         # 'equipment_id': equip,
        #         # 'calendar_event_id': result.id
        #     }
        #     print(value)
        #     self.env['booking.history'].create(value)

        ### Kết thúc cập nhật sau phần chỉnh sửa thêm thiết bị
        return super(CalendarEvent, self).write(vals)
