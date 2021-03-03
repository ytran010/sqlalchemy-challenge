
import numpy as np
import datetime as dt
from datetime import timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List of all routes that are available."""
    return (
        f"Welcome to my API! Here is a list of all available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
    """Return a list of dates and prcp"""
    # Query all passengers
    date_prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>='2016-08-23', Measurement.date<='2017-08-23').\
        order_by(Measurement.date.desc())

    session.close()

    # Convert list of tuples into normal list
    all_dates_prcp = []
    for date, prcp in date_prcp_results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["precipitation"] = prcp
        all_dates_prcp.append(date_prcp_dict)

    return jsonify(all_dates_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    station_results = session.query(Station.station)

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in station_results:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)


    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>='2016-08-23', Measurement.date<='2017-08-23',\
               Measurement.station=='USC00519281')

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature_observation"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
def insert_start_date(start):

    session = Session(engine)


    start_results = session.query(func.min(Measurement.tobs), \
        func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).all()

    session.close()

    all_start = []
    for min, avg, max in start_results:
        start_dict = {}
        start_dict["temp_min"] = min
        start_dict["temp_avg"] = avg
        start_dict["temp_max"] = max
        all_start.append(start_dict)

        return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
def insert_start_end_date(start,end):
    session = Session(engine)

    

    start_end_results = session.query(func.min(Measurement.tobs), \
        func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date>=start, Measurement.date<=end).all()

    session.close()

    all_start_end = []
    for min, avg, max in start_end_results:
        start_end_dict = {}
        start_end_dict["temp_min"] = min
        start_end_dict["temp_avg"] = avg
        start_end_dict["temp_max"] = max
        all_start_end.append(start_end_dict)

        return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True)
