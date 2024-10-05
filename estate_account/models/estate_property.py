from odoo import _, api, fields, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def state_do_sold(self):
        print('Estate Property Sold Action Triggered')

        result = super(EstateProperty, self).state_do_sold()

        partner = self.buyer_id
        
        if partner:
            move_vals = {
                'partner_id': partner.id,
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': [
                    (0, 0, {
                        'name': 'Комиссия за продажу недвижимости (6% от цены)',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Административные сборы',
                        'quantity': 1,
                        'price_unit': 100.00,
                    })
                ]
            }
            invoice = self.env['account.move'].create(move_vals)
            print(f"Счёт-фактура создана с ID: {invoice.id}")

        return result