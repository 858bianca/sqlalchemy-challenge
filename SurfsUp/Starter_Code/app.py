# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
measurements= Base.classes.measurement
station= Base.classes.station

# Save references to each table


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
    """List all available API routes."""
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = session.query(measurements.date).order_by((measurements.date).desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    sel=[measurements.date, measurements.prcp]
    results= session.query(*sel).filter(measurements.date >= one_year_ago).all()

    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    sel = [measurements.station, func.count(measurements.id)]
    active_stations = session.query(*sel).group_by(measurements.station).order_by(func.count(measurements.id).desc()).all()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    sel=[measurements.tobs]
    results= session.query(*sel).filter(measurements.station == USC00519281).filter(measurements.date >= one_year_ago).\
    order_by(measurements.date).all()

    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start=None, end=None):
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
    
        sel = [func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)]
        results = session.query(*sel).order_by(func.count(measurements.id).desc()).all()

    else:
        sel = [func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)]
        results = session.query(*sel).filter(measurements.date <= start).\
        filter(measurements.date<=end).order_by(func.count(measurements.id).desc()).all()



    return jsonify()




    if __name__ == "__main__":
        app.run(debug=True)







