from odoo import fields, models, api


class EquipmentTag(models.Model):
    _name = 'equipment.tag'
    _description = 'Equipment tag'


    name = fields.Char('Tag name', required=True, translate=True)
    description = fields.Text('Mô tả')

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists !")]
