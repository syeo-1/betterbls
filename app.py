from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Float, String, Integer
from sqlalchemy import desc
from datetime import datetime
import json
import jsonpickle

app = Flask(__name__)
# 3 slashes is relative path
# 4 slashes is an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wage_stats.db'
db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Integer, default=0)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow())

#     def __repr__(self) -> str:
#         return f'<Task {self.id}>'

class WageData(db.Model):
    __tablename__ = 'county_wage_data'

    occupation_code = db.Column(db.String(20), nullable=False, primary_key=True)
    occupation_title = db.Column(db.String(20), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    county_code = db.Column(db.String(20))
    employment = db.Column(db.Integer)
    employment_rse_percent = db.Column(db.Float)
    employment_per_1000_jobs = db.Column(db.Float)
    location_quotient = db.Column(db.Float)
    median_hourly_wage_usd = db.Column(db.Float)
    mean_hourly_wage_usd = db.Column(db.Float)
    annual_mean_wage_usd = db.Column(db.Integer)
    mean_wage_rse_percent = db.Column(db.Float)

    def __repr__(self) -> str:
        return f'<Task {self.occupation_code}>'

def db_retrieval(wage_data_list):
    json_list = []
    useless_key = '_sa_instance_state'
    for wage_data_class_instance in wage_data_list:
        wage_data_dict = wage_data_class_instance.__dict__

        # get rid of key just representing db connection information
        # which isn't useful for displayed data
        wage_data_dict.pop(useless_key, None)

        # add the data to the list after removing key
        json_list.append(wage_data_dict)

    # convert the list to a json object and return
    # (cannot return as a raw list!!!)
    return json.dumps(json_list)

def general_query_func(data):
    try:
        return db_retrieval(data)
    except Exception as e:
        print(str(e))
        return 'An error has occured'

def read_data(try_except_func, data):
    return try_except_func(data)

@app.route('/data/<county_code>', methods=['GET'])
def all_county_data(county_code):
    if request.method == 'GET':
        # queries a list of WageData objects
        # where each WageData object represents a row from
        # a specified county wage data table
        # filter it by county_code that's passed in the url
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.county_code == county_code)
        )

@app.route('/data/sortDescending/medianHourlyWage', methods=['GET'])
def descending_median_hourly_wage():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.median_hourly_wage_usd != None).
            order_by(desc(WageData.median_hourly_wage_usd)).all()
        )

@app.route('/data/sortDescending/meanHourlyWage', methods=['GET'])
def descending_mean_hourly_wage():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.mean_hourly_wage_usd != None).
            order_by(desc(WageData.mean_hourly_wage_usd)).all()
        )

@app.route('/data/sortDescending/annualWage', methods=['GET'])
def descending_annaul_wage():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.annual_mean_wage_usd != None).
            order_by(desc(WageData.annual_mean_wage_usd)).all()
        )

@app.route('/data/sortDescending/employmentPerThousand', methods=['GET'])
def descending_employment_per_1000():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.employment_per_1000_jobs != None).
            order_by(desc(WageData.employment_per_1000_jobs)).all()
        )

@app.route('/data/ascendingDescending/medianHourlyWage', methods=['GET'])
def ascending_median_hourly_wage():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.median_hourly_wage_usd != None).
            order_by(WageData.median_hourly_wage_usd).all()
        )

@app.route('/data/sortAscending/meanHourlyWage', methods=['GET'])
def ascending_mean_hourly_wage():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.mean_hourly_wage_usd != None).
            order_by(WageData.mean_hourly_wage_usd).all()
        )
@app.route('/data/sortAscending/annualWage', methods=['GET'])
def ascending_annaul_wage():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.annual_mean_wage_usd != None).
            order_by(WageData.annual_mean_wage_usd).all()
        )

@app.route('/data/sortAscending/employmentPerThousand', methods=['GET'])
def ascending_employment_per_1000():
    if request.method == 'GET':
        return read_data(
            general_query_func,
            WageData.query.filter(WageData.employment_per_1000_jobs != None).
            order_by(WageData.employment_per_1000_jobs).all()
        )


# have a route where user can pass in field to order by and choose descending or ascending!!!
# for example, would be really good to be able to sort by employment per 1000 descending
# followed by sort by a wage column descending
# that way can see which occupation has jobs available with decent pay!!!

# should be able to eventually search by occupation title in UI
# maybe map to occupation_code

# eventually filter by state and occupation

# need a table for state, county code (like a meta table?)


if __name__ == "__main__":
    app.run(debug=True)