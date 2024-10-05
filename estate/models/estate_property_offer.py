from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"
    _order = "price desc"
    
    price = fields.Float(required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = record.create_date.date()
                delta = (record.date_deadline - create_date).days
                record.validity = delta

    def action_accept(self):
        if self.property_id.state == 'sold':
            raise UserError("Невозможно принять предложение для проданной недвижимости.")
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = 'offer_accepted'

    def action_refuse(self):
        self.status = 'refused'

    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", string='Property Type')

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if property.offer_ids and max(property.offer_ids.mapped('price')) >= vals['price']:
            raise UserError("Новое предложение должно быть выше текущего максимального предложения.")
        property.state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Цена должна быть позитивной, то есть больше нуля')
    ]