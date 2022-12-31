# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config

import csv
from datetime import datetime
from random import randint
from sqlalchemy.orm.mapper import configure_mappers

from apps.authentication.models import Users
from apps.home.models import Data
from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
from apps.rooms.models import Rooms

DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)


# Inner command
def load_cmd(aUseRandomValues=None):
    if aUseRandomValues:
        print(' >>> Randomize Values ')
    else:
        print(' >>> Use Values from input file ')

    # Create Tables (if not exist)
    db.create_all()

    # Truncate
    db.session.query(Data).delete()
    db.session.commit()

    with open('media/transactions_data.csv', newline='') as csvfile:

        csvreader = csv.reader(csvfile)  # load file
        header = next(csvreader)  # ignore header (1st line)

        '''
        Expected format: 
            HEADER: product_code,product_info,value,currency,type
            SAMPLE: Lenovo_Ideapad_3i, Lenovo Ideapad 3i 14.0inch FHD Laptop,9.5,euro,transaction

            product_code (string)  : Lenovo_Ideapad_3i
            product_info (string)  : Lenovo Ideapad 3i 14.0inch FHD Laptop
            value        (integer) : 9 
            currency     (string)  : usd, eur 
            type         (string)  : transaction (hardoded)
        '''

        iter = 0  # used for timestamp
        for row in csvreader:

            iter += 1

            if len(row) != 5:
                print(' >>> Error parsing line (' + str(iter) + ') -> ' + ' '.join([str(elem) for elem in row]))
                continue

            item_code = row[0]
            item_name = row[1]

            if aUseRandomValues:
                item_value = randint(5, 100)
            else:
                item_value = row[2]

            item_currency = row[3]
            item_type = row[4]

            # randomize in the past the transaction date
            # The distribuition range ~1 month
            item_ts = datetime.utcnow().timestamp() - (2 * iter * randint(5, 10) * 3600)
            item_ts = int(item_ts)

            _data = Data(code=item_code, name=item_name, value=item_value, currency=item_currency, type=item_type,
                         ts=item_ts)

            db.session.add(_data)

        db.session.commit()


@app.cli.command("load_data")
def load_data():
    return load_cmd()


@app.cli.command("load_random_data")
def load_data():
    return load_cmd(True)


@app.template_filter('ctime')
def timectime(s):
    return datetime.utcfromtimestamp(s).strftime('%Y-%m-%d')


@app.cli.command("load_users_data")
def load_users_data():
    with open('media/users_data.csv', newline='') as csvfile:

        csvreader = csv.reader(csvfile)  # load file
        header = next(csvreader)  # ignore header (1st line)

        '''
        Expected format: 
            HEADER: id,username,email,email_token_key,password,account_status
            SAMPLE: 1, test,pleasesayhi@163.com,email_token,1506b743abcdcad716719abdeff02fbc0d242713738f6965114e2ca57654d0c0688a311cedf125f37fe41422436e78f7c0ca0c5d2d0c48f66b5852d16ede31bad828bd000f81efe76f45abe4e1960816f55eea5169c18e2ddf05d8bc536454a2,1
        
        '''

        iter = 0  # used for timestamp
        for row in csvreader:

            iter += 1

            if len(row) != 6:
                print(' >>> Error parsing line (' + str(iter) + ') -> ' + ' '.join([str(elem) for elem in row]))
                continue

            id = row[0]
            username = row[1]
            email = row[2]
            email_token_key = row[3]
            password = row[4]
            account_status = row[5] == '1'

            _users = Users(username=username, email=email, email_token_key=email_token_key, password=password,
                           account_status=account_status)

            db.session.add(_users)

        db.session.commit()


@app.cli.command("load_rooms_data")
def load_rooms_data():
    with open('media/rooms_data.csv', newline='', encoding='utf-8') as csvfile:

        csvreader = csv.reader(csvfile)  # load file
        header = next(csvreader)  # ignore header (1st line)

        '''
        Expected format: 
            HEADER: title,country,state,city,address,max_guest,category,price,bedroom,washroom,bed,detail,title_photo,photos,phone,tags,check_tips,create_date,status,views,loves,users_id
            SAMPLE: 
            title: 西門捷運2分鐘-特色斜窗浴缸雙人房型-24h櫃台
            
            
        '''

        iter = 0  # used for timestamp
        for row in csvreader:

            iter += 1

            if len(row) != 22:
                print(' >>> Error parsing line (' + str(iter) + ') -> ' + ' '.join([str(elem) for elem in row]))
                continue

            title = row[0]
            country = row[1]
            state = row[2]
            city = row[3]
            address = row[4]
            max_guest = row[5]
            category = row[6]
            price = row[7]
            bedroom = row[8]
            washroom = row[9]
            bed = row[10]
            detail = row[11]
            title_photo = row[12]
            photos = row[13]
            phone = row[14]
            tags = row[15]
            check_tips = row[16]
            create_date = row[17]
            status = row[18]
            views = randint(5, 100)
            loves = randint(5, 100)
            users_id = row[21]

            _rooms = Rooms(title=title, country=country,
                           state=state, city=city, address=address, max_guest=max_guest,
                           category=category, price=price, bedroom=bedroom,
                           washroom=washroom, bed=bed, detail=detail,
                           title_photo=title_photo, photos=photos,
                           phone=phone, tags=tags, check_tips=check_tips,
                           create_date=create_date, status=status, views=views,
                           loves=loves, users_id=users_id)

            db.session.add(_rooms)

        db.session.commit()


if __name__ == "__main__":
    app.run()
