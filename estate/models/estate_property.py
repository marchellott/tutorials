from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate property module"
    _order = "id desc"

    name = fields.Char('Name', required=True)
    description = fields.Text()
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(copy=False, default=lambda self: (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        required=True,
        copy=False,
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Float(compute="_compute_total", readonly=True)
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", readonly=True)
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def state_do_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Проданную недвижимость нельзя отменить.")
            record.state = 'canceled'
        return True
    
    def state_do_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Отмененная недвижимость не может быть продана.")
            record.state = 'sold'
        return True
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Ожидаемая цена должна быть позитивной, то есть больше нуля'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'Цена должна быть позитивной, то есть больше нуля')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price > 0:  # Only check if selling price is set
                # Compare selling price and 90% of expected price using float_compare
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:
                    raise ValidationError(_("The selling price cannot be less than 90% of the expected price."))
                
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count", store=True)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property in self:
            property.offer_count = len(property.offer_ids)

    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("Нельзя удалить недвижимость, если она не в состоянии 'Новое' или 'Отменено'.")