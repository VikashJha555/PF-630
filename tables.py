from flask_table import Table, Col
 
class Results(Table):
    id = Col('Id', show=False)
    First_Name = Col('first_name')
    Last_Name = Col('last_name')
    Phone = Col('phone')
    Email = Col('email')
    Password = Col('password')
    Confirm_Password = Col('confirm')