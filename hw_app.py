import numpy as np

from datetime import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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
        f"Available Routes:<br/>"
        f"<a href = 'http://127.0.0.1/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href = 'http://127.0.0.1/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href = 'http://127.0.0.1/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href = 'http://127.0.0.1/api/v1.0/start_date'>/api/v1.0/start_date</a><br/>"
        f"<a href = 'http://127.0.0.1/api/v1.0/start_date/end_date'>/api/v1.0/start_date/end_date</a>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation ():
    """Return a percipitation value for each day for the last 12 months"""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    dt_last_date = dt.fromisoformat(last_date[0])
    last_year_date = dt_last_date - timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date > last_year_date).\
                    order_by(Measurement.date).all()

# Create a dictionary from the row data and append to a list of all_passengers
    date = [result[0] for result in results[:]]
    d = 0
    for d in date:
        d_dict= {}
        d_dict["percipitation"] = results.prcp
        date.append(d_dict)
        d+1
    return jsonify(date)

@app.route("/api/v1.0/stations")
def stations():
    """List of available stations"""

    results = session.query(Measurement.station).\
                    group_by(Measurement.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature ():

    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    dt_last_date = dt.fromisoformat(last_date[0])
    last_year_date = dt_last_date - timedelta(days=365)


    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date > last_year_date).\
                order_by(Measurement.date).all()
    
    temperature = list(np.ravel(results))

    return jsonify(temperature)


@app.route("/api/v1.0/<start_date>")
def startdate(start_date):

    """find the Min, Max and Average temperatures for the range after the starting date 
    supplied by the user, or a 404 if not."""
    start_date= dt.datetime.strptime(start_date, '%Y-%m-%d')

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    stats = list(np.ravel(results))

    return jsonify(stats)


@app.route("/api/v1.0/<start_date>/<end_date>")
def startenddate(start_date, end_date):

    """find the Min, Max and Average temperatures for the range between starting date and ending 
    supplied by the user, or a 404 if not."""
    start_date= dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end_date, '%Y-%m-%d')

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    stats = list(np.ravel(results))

    return jsonify(stats)


if __name__ == "main":
    app.run(debug = True)