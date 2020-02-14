import datetime as dt 
from flask import Flask
from flask import jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

db_path = 'sqlite:///Resources/hawaii.sqlite'
engine = create_engine(db_path)
Base = automap_base()
Base.prepare(engine, reflect = True)


Measurement = Base.classes.measurement
Station = Base.classes.station 

app = Flask(__name__)




@app.route('/')
def home():
    """"
    Home page of Hawaii Climate Analysis API.
    """
    return "Welcome to the API"


@app.route('/api/v1.0/precipitation')
def precipitation():
    """
    Returns all of the precipitation data.
    """
    results = Session.query(Measurement.date, Measurement.prcp).all()
    data = {d: prcp for d, prcp in results}
    return jsonify(data)

@app.route('/api/v1.0/stations')
def stations():
    """
    Return the list of the stations.
    """
    results = Session.query(Station.station, Station.name).all()
    data = {station: name for station, name in results}
    return jsonify(data)

@app.route('/api/v1.0/tobs')
def last_year_tobs():
    """
    Returns the temperature data for the last year.
    """
    last_date = Session.query(func.max(Measurement.date))[0][0]
    y, m, d = int(last_date[:4]), int(last_date[5:7]), int(last_date[8:])
    end_date = dt.date(y, m, d)
    start_date = end_date - dt.timedelta(days=365)
    results = Session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start_date).all()
    data = {d: tobs for d, tobs in results}
    return jsonify(data)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def stats(start=None, end=None):
    fields = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs),
    ]
    if not start and not end:
        results = Session.query(*fields).all()
    else:
        if not end:
            results = Session.query(*fields).\
            filter(Measurement.date >= start).all()
        else:
            resuls = Session.query(*fields).\
            filter(Measurement.date)>= start).\
            filter(Measurement.date <= end).all()
    
    data = {
        'tmin': results[0][0],
        'tmax': results[0][1],
        'tavg': results[0][2],
    }
    return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True)