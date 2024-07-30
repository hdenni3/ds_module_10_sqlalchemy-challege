import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Print all of the classes mapped to the Base
Base.classes.keys()

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )

# SQL Queries
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Last Year's precipitation Data
    #Date from 1 year ago on the last date in the database
    one_year_before = dt.date(2017,8,23) - dt.timedelta(days = 365)

    #Query for last year's precipitation
    precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_before).all()

    session.close()
    precip = {date: prcp for date, prcp in precip_scores}
    return jsonify(precip)





# @app.route("/api/v1.0/precipitation_raw")
# def passengers_raw():
#     data = sql.query_precipitation_raw()
#     return(jsonify(data))

# # start should be in format 2016-08-23
# @app.route("/api/v1.0/<start>")
# def tobs_start_orm(start):
#     data = sql.query_tobs_start_orm(start)
#     return(jsonify(data))

# # start should be in format 2016-08-23
# @app.route("/api/v1.0/<start>/<end>")
# def tobs_start_end_raw(start, end):
#     data = sql.query_tobs_start_end_raw(start, end)
#     return(jsonify(data))


# Run the App
if __name__ == '__main__':
    app.run(debug=True)
