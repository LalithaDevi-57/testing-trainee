from odoo import models, fields, api

class GarageCar(models.Model):
    _name = 'garage.car'
    _description = 'Garage Car'

    name = fields.Char(string="Car Name", required=True)
    brand = fields.Char(string="Brand")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    customer_id = fields.Many2one("res.partner", string="Customer")
    model_year = fields.Integer(string="Year")
    active = fields.Boolean(default=True)


    def create_garage_car(self):
        for record in self:
            self.env['garage.car'].create({
                'name': record.name + ' Copy',
                'brand': record.brand,
                'model_year': record.model_year,
            })
        # 2. READ method using browse()

    def get_car_by_id(self, car_id):
        car = self.env['garage.car'].browse(car_id)
        if car.exists():
            return f"Car: {car.name}, Brand: {car.brand}"
        return "Car not found."

        # 3. UPDATE method using write()

    def update_car_brand(self, car_id, new_brand):
        car = self.env['garage.car'].browse(car_id)
        if car.exists():
            car.write({'brand': new_brand})
            return f"Updated car {car.name} brand to {new_brand}"
        return "Car not found."

        # 4. DELETE method using unlink()

    def delete_car(self, car_id):
        car = self.env['garage.car'].browse(3)
        if car.exists():
            car.unlink()
            return "Car deleted."
        return "Car not found."

        # 5. SEARCH method

    def search_cars_by_brand(self, brand):
        return self.env['garage.car'].search([('brand', '=', brand)])

        # 6. SEARCH_COUNT method

    def count_recent_cars(self):
        return self.env['garage.car'].search_count([('year', '>=', 2020)])

        # 7. MAPPED method

    def get_all_car_names(self):
        cars = self.env['garage.car'].search([])
        return cars.mapped('name')

        # 8. FILTERED method

    def get_old_cars(self):
        cars = self.env['garage.car'].search([])
        return cars.filtered(lambda car: car.year < 2015)

        # 9. SORTED method

    def get_sorted_cars(self):
        cars = self.env['garage.car'].search([])
        return cars.sorted(key=lambda car: car.year)

        # 10. ENSURE_ONE method

    def ensure_only_one(self, car_id):
        car = self.env['garage.car'].browse(car_id)
        car.ensure_one()
        return car.name

        # 11. COPY method

    def duplicate_car(self, car_id):
        car = self.env['garage.car'].browse(car_id)
        return car.copy({'name': car.name + ' (Copy)'})

        # 12. EXISTS method

    def car_exists(self, car_id):
        return self.env['garage.car'].browse(car_id).exists()

        # 13. SUDO method

    def get_all_cars_as_admin(self):
        return self.env['garage.car'].sudo().search([])

        # 14. WITH_CONTEXT method

    def search_with_context(self):
        return self.env['garage.car'].with_context(active_test=False).search([])

        # 15. NAME_GET method

    def get_name_display(self):
        cars = self.env['garage.car'].search([])
        return cars.name_get()
