from odoo import _, api, fields, models

class InheritedModel(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson_id', String="Properties", domain=[('state', 'in', ['new', 'offer_received'])])