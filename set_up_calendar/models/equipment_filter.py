# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EquipmentFilter(models.Model):
    _name = 'equipment.filters'
    _description = 'Equipment Filters'

    user_id = fields.Many2one('res.users', 'Me', required=True, default=lambda self: self.env.user)
    equipment_id = fields.Many2one('equipment.manager','Tên thiết bị', required=True)
    equipment_checked = fields.Boolean('Checked', default=True,
        help="This field is used to know if the equipment is checked in the filter of the calendar view for the user_id.")

    # _sql_constraints = [
    #     ('user_id_equipment_id_unique', 'UNIQUE(user_id, equipment_id)', 'A user cannot have the same contact twice.')
    # ]

    @api.model
    def unlink_from_equipment_id(self, equipment_id):
        return self.search([('equipment_id', '=', equipment_id)]).unlink()
