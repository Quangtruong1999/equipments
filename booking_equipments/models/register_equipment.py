from datetime import timedelta, datetime

from odoo import fields, models, api
from odoo.http import request


class RegisterEquipment(models.Model):
    _name = 'register.equipment'
    _description = 'Đăng ký sử dụng thiết bị'
    _inherit = ['equipment.manager', 'equipment.tag']

    name = fields.Char('Mã đăng ký', compute='_compute_code', default="Đăng ký sử dụng thiết bị", readonly=True)
    start = fields.Datetime(
        'Bắt đầu vào', required=True, tracking=True, default=fields.Date.today,
        help="Ngày bắt đầu của việc mượn thiết bị")
    stop = fields.Datetime(
        'Kết thúc vào', required=True, tracking=True, default=lambda self: fields.Datetime.today() + timedelta(hours=1),
        compute='_compute_stop', readonly=False, store=True,
        help="Ngày kết thúc của việc mượn thiết bị")
    # start_date = fields.Date(
    #     'Bắt đầu vào', store=True, tracking=True,
    #     compute='_compute_dates', inverse='_inverse_dates')
    # stop_date = fields.Date(
    #     'Kết thúc vào', store=True, tracking=True,
    #     compute='_compute_dates', inverse='_inverse_dates')
    duration = fields.Float('Thời lượng', compute='_compute_duration', index=True, store=True)
    # comming soon
    all_day = fields.Boolean('Cả ngày', index=True, store=True)
    user_id = fields.Many2one('res.users', 'Người đăng kí', default=lambda self: self.env.user)
    location = fields.Char('Địa điểm', tracking=True, help="Địa điểm")
    register_line = fields.One2many('register.equipment.line', 'register_id',
                                    string='Register Line',
                                    opy=True,
                                    auto_join=True, index=True)
    equipments = fields.Many2many(
        comodel_name='equipment.manager',
        relation='register_equipment_x_equipment_manager',
        index=True,
        required=True,
        store=True
    )
    description = fields.Text('Mô tả', store=True, index=True)
    # comming soon
    # register_tags = fields.Many2many(
    #     comodel_name='equipment.tag',
    #     relation='register_equipment_x_equipment_tag',
    #     required=True,
    #     store=True
    # )

    register_tags = fields.Selection(
        [('hello', 'Hello')],
        string='Thẻ',
        index=True,
        store=True
    )

    @api.model
    def create(self, vals):
        print('values of order = ', vals)
        print('self  of order= ', self)
        # equipments = vals.get('equipments')[0][2]
        # for equip in equipments:
        #     line_tmp = {}
        #     equipment = request.env['register.equipment'].sudo().search([('id', '=', equip)])
        #     line_tmp['name'] = equipment.name
        #     line_tmp['start'] = vals.get('start')
        #     line_tmp['stop'] = vals.get('stop')
        #     line_tmp['duration'] = vals.get('duration')
        #     line_tmp['equipment_id'] = equipment.id
        # print('equipment = ', equipments)
        all_equip = self.env['equipment.manager']
        for equip in vals.get('equipments')[0][2]:
            print(equip)
            print('aaaa')
            value = {
                'start': vals.get('start'),
                'stop': vals.get('stop'),
                'all_day': vals.get('all_day'),
                'user_id': vals.get('user_id'),
                'location': vals.get('location'),
                'equipment_id': equip
            }
            print(value)
            self.env['booking.history'].create(value)
        return super(RegisterEquipment, self).create(vals)

    def write(self, vals):
        return super(RegisterEquipment, self).write(vals)

    def _get_duration(self, start, stop):
        """ Get the duration value between the 2 given dates. """
        print(type(start))
        print('stop: ', stop)
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)

    @api.depends('start', 'duration')
    def _compute_code(self):
        for i in self:
            self.name = "Thời gian đăng ký: " + str(datetime.now().day) + '/' + str(datetime.now().month) + '/' + \
                        str(datetime.now().year) + ' ' + str(datetime.now().time())
            print('self name = ', self.name)

    @api.depends('stop', 'start')
    def _compute_duration(self):
        for event in self:
            event.duration = self._get_duration(event.start, event.stop)

    @api.depends('start', 'duration')
    def _compute_stop(self):
        # stop and duration fields both depends on the start field.
        # But they also depends on each other.
        # When start is updated, we want to update the stop datetime based on
        # the *current* duration. In other words, we want: change start => keep the duration fixed and
        # recompute stop accordingly.
        # However, while computing stop, duration is marked to be recomputed. Calling `event.duration` would trigger
        # its recomputation. To avoid this we manually mark the field as computed.
        duration_field = self._fields['duration']
        self.env.remove_to_compute(duration_field, self)
        for event in self:
            # Round the duration (in hours) to the minute to avoid weird situations where the event
            # stops at 4:19:59, later displayed as 4:19.
            event.stop = event.start and event.start + timedelta(minutes=round((event.duration or 1.0) * 60))
            if event.all_day:
                event.stop -= timedelta(seconds=1)

    @api.depends('all_day', 'start', 'stop')
    # @api.depends('start', 'stop')
    def _compute_dates(self):
        """ Adapt the value of start_date(time)/stop_date(time)
            according to start/stop fields and allday. Also, compute
            the duration for not allday meeting ; otherwise the
            duration is set to zero, since the meeting last all the day.
        """
        for meeting in self:
            if meeting.all_day and meeting.start and meeting.stop:
                meeting.start_date = meeting.start.date()
                meeting.stop_date = meeting.stop.date()
            else:
                meeting.start_date = False
                meeting.stop_date = False

    def _inverse_dates(self):
        """ This method is used to set the start and stop values of all day events.
            The calendar view needs date_start and date_stop values to display correctly the allday events across
            several days. As the user edit the {start,stop}_date fields when allday is true,
            this inverse method is needed to update the  start/stop value and have a relevant calendar view.
        """
        for meeting in self:
            if meeting.all_day:
                # Convention break:
                # stop and start are NOT in UTC in allday event
                # in this case, they actually represent a date
                # because fullcalendar just drops times for full day events.
                # i.e. Christmas is on 25/12 for everyone
                # even if people don't celebrate it simultaneously
                enddate = fields.Datetime.from_string(meeting.stop_date)
                enddate = enddate.replace(hour=18)

                startdate = fields.Datetime.from_string(meeting.start_date)
                startdate = startdate.replace(hour=8)  # Set 8 AM

                meeting.write({
                    'start': startdate.replace(tzinfo=None),
                    'stop': enddate.replace(tzinfo=None)
                })
