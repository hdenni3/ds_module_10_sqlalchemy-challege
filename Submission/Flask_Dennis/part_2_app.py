import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# # Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# # Declare a Base using `automap_base()`
Base = automap_base()
# # Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# # Print all of the classes mapped to the Base
Base.classes.keys()

# # The Purpose of this Class is to separate out any Database logic
# class SQLHelper():
#     #################################################
#     # Database Setup
#     #################################################

#     # define properties
#     def __init__(self):
#         self.engine = create_engine("sqlite:///hawaii.sqlite")
#         self.Base = None

#         # automap Base classes
#         self.init_base()

#     def init_base(self):
#         # reflect an existing database into a new model
#         self.Base = automap_base()
#         # reflect the tables
#         self.Base.prepare(autoload_with=self.engine)

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

# Station Query
@app.route("/api/v1.0/stations")
def stations(): 
    stations  = session.query(Station.station).distinct().all()

    print(stations)

    session.close()
    list(np.ravel(stations))
    return jsonify(list(np.ravel(stations)))

# Tobs Query
@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()

    session.close()
    return jsonify(list(np.ravel(tobs)))

# Query for Start and End Temps

@app.route("/api/v1.0/temp/<start_date>")
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def temperature_stats(start_date=None, end_date=None):
    """Return TMIN, TAVG, TMAX for a given date range."""
    # Select statement for temperature statistics
    temp_stats = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end_date:
        # Convert start_date string to datetime object
        date_start = dt.datetime.strptime(start_date, "%m%d%Y")
        
        # Query temperature stats for dates greater than or equal to start_date
        query_results = session.query(*temp_stats).\
            filter(Measurement.date >= date_start).all()
        
        # Close the session
        session.close()
# Unravel results into a 1D array and convert to a list
        temperature_data = list(np.ravel(query_results))
        
        # Return the results as JSON
        return jsonify(temperature_data)
    
    # If both start_date and end_date are provided
    # Convert start_date and end_date strings to datetime objects
    date_start = dt.datetime.strptime(start_date, "%m%d%Y")
    date_end = dt.datetime.strptime(end_date, "%m%d%Y")
    
    # Query temperature stats for the specified date range
    query_results = session.query(*temp_stats).\
        filter(Measurement.date >= date_start).\
        filter(Measurement.date <= date_end).all()
    
    # Close the session
    session.close()
    
    # Unravel results into a 1D array and convert to a list
    temperature_data = list(np.ravel(query_results))
    
    # Return the results as JSON with a descriptive key
    return jsonify(temperature_stats=temperature_data)



# Run the App
if __name__ == '__main__':
    app.run(debug=True)
