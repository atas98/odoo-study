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


## Chapter 2:
Main goal: Create a wizard to upload weather from csv file.

### Models:
Model: _name - upload.weather.wizard

#### Fields: 
* weather_file: Binary, required,
* weather_file_name: Char,
* parsed: Boolean,
* uploaded: Boolean,
* weather_line_ids: One2many, ‘upload.weather.wizard.line’


Model: _name: upload.weather.wizard.line
	
#### Fields:
* upload_weather_wizard_id: Many2one, upload.weather.wizard, readonly,
* city_name: Char, readonly,
* temperature_c: Char, readonly,
* humidity: Char, readonly,
* date: Char, readonly,
* error_description: Char, readonly, restrict size (attribute size),
* can_load: Boolean
_Set defaults for boolean fields._
	
### Methods:
**parse_weather_file:**

    Have to parse the file and create weather wizard lines based on data.
    Have to include differenе handlers for various exceptions that may occur during file parsing.
    can_load field have to be False if we can not transform data from file to needed data type.
    error_description field contains exception human readable description for all exceptions.
    Fields for wizard lines are Char to show the user the real values that are taken from the file.
**upload_weather:**

    Have to create weather records for city.weather model if it does not exist for city and date.
    Have to create a city if it does not exist.
    Have to upload only data where the field can_load is True.
	
### View:
    First we show the field file and button cancel. If we have an attached file we have to show the button Parse Data.
    Press button Parse Data and show field weather_line_ids and button Upload Weather but button Parse Data has to be invisible. 
    Press button Upload Weather. Create weather records and show only weather_line_ids that are not created (have errors).
    Buttons Upload Weather and Cancel make it invisible. Button Ok is visible.
    Pressing Ok will refresh the page.

_Note: Keys of csv file: city,date,temperature,humidity. Create city records for Ukraine._

### Accessories:
https://odooforbeginnersblog.wordpress.com/2017/03/05/how-to-create-wizards-in-odoo/
https://www.odoo.com/documentation/14.0/developer/howtos/backend.html#wizards
https://www.odoo.com/ru_RU/forum/pomoshch-1/widgets-in-odoo-13-158814
https://swapon.me/2018/07/18/widgets-in-odoo/
https://odoo-dev.readthedocs.io/en/latest/widgets/field_widgets.html
