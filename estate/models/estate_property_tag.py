from odoo import fields, models

class EstatePropertiesTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_field_unique', 
        'unique(name)',
        'Choose another value - it has to be unique!')
    ]