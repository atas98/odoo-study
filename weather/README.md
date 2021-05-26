# Create odoo addon weather:
## Chapter 1:
Model: _name - city.weather.
		
### Fields:
* city: Many2one,  'res.city', required, index (what is this for?), readonly (if state not draft),
* state: Selection (draft, confirmed),
* date: Date, required, index, readonly (if state not draft, use field attribute states),
* humidity: Float, rounding 2 signs (use odoo decimal_precision) required readonly (if state not draft), string - Celsius, help - Temperature in degrees centigrade,
* temperature_с: Float, rounding 2 signs (use odoo decimal_precision), required, readonly (if state not draft use field attribute states),
* uom_temperature_c: Many2one, 'uom.uom', default C (celsius degrees),  required readonly(all time),
* temperature_f: Float rounding 2 signs (use odoo decimal_precision),  compute - _compute_fahrenheit_temperature, string - Fahrenheit, help - temperature in degrees fahrenheit,
* uom_temperature_f: Many2one, 'uom.uom', default F (Fahrenheit degrees), required, readonly (all time).

### Constraints:
* sql constraint (restrict temperature and humidity, unique date -> city)
* api.constraint (restrict date more today)

### Views:
* tree: all fields except state,
* form: all fields except state (group by your UI experience), for field state use widget statusbar, make it clickable,
* search: city, date, group by city and state, filters temperature > 0 and temperature < 0 and dates ( month, year),

### Security:
* create groups weather_user include base.group_user, and  weather_manager include group weather_user,
* create users weather_user and weather_manager,
* setup ir.model.access.csv rules for weather_user read and weather_manager all.

Note: uoms and decimal precisions have to be created through data.

### Accessories: 
* https://www.odoo.com/documentation/14.0/developer/howtos/backend.html
* https://drive.google.com/file/d/1XZ0o8F37nO7tGnS5XmWKzgP86_EuAdI3/view?usp=sharing
