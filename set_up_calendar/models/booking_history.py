from datetime import datetime, timedelta, date

from odoo import fields, models, api, exceptions


class BookingHistory(models.Model):
    _name = 'booking.history'
    _description = 'Xem lịch sử đặt thiết bị'

    start = fields.Datetime(
        string='Bắt đầu vào',
        required=True,
        index=True,
        store=True
    )
    stop = fields.Datetime(
        string='Kết thúc vào',
        required=True,
        index=True,
        store=True
    )
    duration = fields.Float('Thời lượng/h', help='Đơn vị tính bằng h', index=True, store=True)
    user_id = fields.Many2one('res.users', 'Người đăng kí', default=lambda self: self.env.user)
    equipment_id = fields.Many2one(
        string="Tên thiết bị",
        comodel_name="equipment.manager",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(related='equipment_id.name', string='Tên thiết bị')
    calendar_event_id = fields.Many2one('calendar.event', 'Mã lịch sử dụng thiết bị',
                                        required=True, index=True, store=True)

    @api.model
    def create(self, values):
        print(values.get('start'))
        print(type(values.get('start')))
        start = datetime.strptime(values.get('start'), '%Y-%m-%d %H:%M:%S')
        stop = datetime.strptime(values.get('stop'), '%Y-%m-%d %H:%M:%S')
        print(start)
        print(type(start))
        if stop < start:
            raise exceptions.UserError('lỗi tạo')
        return super(BookingHistory, self).create(values)

    def write(self, values):
        return super(BookingHistory, self).write(values)
