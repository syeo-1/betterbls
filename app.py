from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Float, String, Integer
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
    __tablename__ = 'county_42660'

    occupation_code = db.Column(db.String(20), nullable=False, primary_key=True)
    occupation_title = db.Column(db.String(20), nullable=False)
    level = db.Column(db.String(20), nullable=False)
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

@app.route('/data', methods=['GET'])
def data():
    if request.method == 'GET':
        # queries a list of WageData objects
        # where each WageData object represents a row from
        # a specified county wage data table
        wage_data_list = WageData.query.order_by(WageData.annual_mean_wage_usd).all()

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


if __name__ == "__main__":
    app.run(debug=True)