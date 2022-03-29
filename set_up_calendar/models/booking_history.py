from odoo import fields, models, api


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
        string="Equipment_id",
        comodel_name="equipment.manager",
        required=True,
        ondelete="cascade",
    )
    calendar_event_id = fields.Many2one('calendar.event', 'Mã lịch sử dụng thiết bị',
                                        required=True, index=True, store=True)

    @api.model
    def create(self, values):
        return super(BookingHistory, self).create(values)

    def write(self, values):
        return super(BookingHistory, self).write(values)
