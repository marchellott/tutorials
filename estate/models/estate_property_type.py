from odoo import fields, models

class EstatePropertiesType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('name_field_unique', 
        'unique(name)',
        'Choose another value - it has to be unique!')
    ]

    property_ids = fields.One2many('estate.property', 'property_type_id', String="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    offer_count = fields.Integer(
        string="Number of Offers",
        compute="_compute_offer_count"
    )

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([
                ('property_type_id', '=', record.id)
            ])

    def action_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }