from odoo import fields, models, api


class EquipmentManager(models.Model):
    _name = 'equipment.manager'
    _description = 'Quản lý thiết bị công ty'

    name = fields.Char('Tên thiết bị', required=True)
    registration_date = fields.Date('Ngày đăng kiểm', help='Ngày kích hoạt thiết bị')
    equipment_management = fields.Many2one('res.partner', string='Quản lý thiết bị')
    tag = fields.Many2many(comodel_name='equipment.tag', string='Từ khóa')
