from odoo import fields, models, api


class ResgisterEquipmentLine(models.Model):
    _name = 'register.equipment.line'
    _description = 'Danh sách các thiết bị'

    register_id = fields.Many2one('register.equipment', string='Register Reference', required=True,
                                 ondelete='cascade', index=True, copy=False)
    name = fields.Char('Thiết bị', required=True)
    start = fields.Datetime(
        'Bắt đầu vào', required=True, tracking=True, default=fields.Date.today,
        help="Ngày bắt đầu của việc mượn thiết bị")
    stop = fields.Datetime(
        'Kết thúc vào', required=True, tracking=True, readonly=False, store=True,
        help="Ngày kết thúc của việc mượn thiết bị")
    duration = fields.Float('Thời lượng', index=True, store=True)
    # comming soon
    all_day = fields.Boolean('Cả ngày', index=True, store=True)
    user_id = fields.Many2one('res.users', 'Người đăng kí', default=lambda self: self.env.user)
    location = fields.Char('Địa điểm', tracking=True, help="Địa điểm")
    equipment_id = fields.Many2one('register.equipment', string='Equipment Reference', required=True,
                                 ondelete='cascade', index=True, copy=False)

    @api.model
    def _prepare_add_missing_fields(self, values):
        """ Deduce missing required fields from the onchange """
        res = {}
        onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id']
        if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
            line = self.new(values)
            line.product_id_change()
            for field in onchange_fields:
                if field not in values:
                    res[field] = line._fields[field].convert_to_write(line[field], line)
        return res


    @api.model
    def create(self, values):
        return super(ResgisterEquipmentLine, self).create(values)

    def write(self, values):
        print('values of order line = ', values)
        print('self  of order line= ', self)
        return super(ResgisterEquipmentLine, self).write(values)
    #
    # @api.model_create_multi
    # def create(self, vals_list):
    #
    #     return self.create(ResgisterEquipmentLine).create(vals_list)
