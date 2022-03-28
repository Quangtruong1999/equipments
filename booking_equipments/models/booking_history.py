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
    duration = fields.Float('Thời lượng', compute='_compute_duration', index=True, store=True)
    all_day = fields.Boolean('Cả ngày', index=True, store=True)
    user_id = fields.Many2one('res.users', 'Người đăng kí', default=lambda self: self.env.user)
    location = fields.Char('Địa điểm', tracking=True, help="Địa điểm")
    equipment_id = fields.Many2one(
        string="Equipment_id",
        comodel_name="equipment.manager",
        required=True,
        ondelete="cascade",
    )

    #
    # register_equip = fields.Many2one('register.equipment', string='Register Reference', required=True,
    #                              ondelete='cascade', index=True, copy=False)

    @api.model
    def create(self, values):
        print('values: ', values)
        return super(BookingHistory, self).create(values)

    def write(self, values):
        print('values of order line = ', values)
        print('self  of order line= ', self)
        return super(BookingHistory, self).write(values)

    def _get_duration(self, start, stop):
        """ Get the duration value between the 2 given dates. """
        print(type(start))
        print('stop: ', stop)
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)

    @api.depends('stop', 'start')
    def _compute_duration(self):
        for event in self:
            event.duration = self._get_duration(event.start, event.stop)
