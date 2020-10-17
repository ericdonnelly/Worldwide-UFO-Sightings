from flask import Flask, render_template, redirect, jsonify, request
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from scipy.stats import ttest_ind
import sqlite3

# Creating a SQL Alchemy ORM
engine = create_engine("sqlite:///database/database.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# table names
ufo_data = Base.classes.ufo_data
state_stats = Base.classes.state_stats
merge_again = Base.classes.merge_again

# should print table names
print(Base.classes.keys())

app = Flask(__name__)

@app.route("/")
def welcome():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "latitude": result[0], "longitude": result[1]}
        big_list.append(obj)
    
    return render_template('index.html')
    #return render_template('index.html', data=big_list)


@app.route("/heatmap")
def heatmap():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "latitude": result[0], "longitude": result[1]}
        big_list.append(obj)
    
    # #debug
    # print(big_list[0:10])

    
    return render_template('heat.html')


@app.route('/heatmapdata')
def heatmapdata():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "latitude": result[0], "longitude": result[1]}
        big_list.append(obj)
    
    # #debug
    # print(big_list[0:10])

    data=jsonify(big_list)
    
    return data

@app.route("/drugs")
def drugs():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    return render_template('drugs.html')


@app.route('/drugsdata1')
def drugsdata1():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(state_stats.name, state_stats.sightings,\
        state_stats.drug_deaths).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "state_name": result[0], "state_sightings": result[1],\
            "state_drug_deaths": result[2]}
        big_list.append(obj)
    
    data=jsonify(big_list)
    
    return data

@app.route('/drugsdata2')
def drugsdata2():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude,\
        ufo_data.datetime, ufo_data.city, ufo_data.shape, ufo_data.comments,\
            ufo_data.duration_hours, ufo_data.year, ufo_data.month,\
                ).filter((ufo_data.year == 2014) & (ufo_data.month < 3))

    session.close()

    big_list = []

    for result in results:

        obj = {
            'latitude': result[0],
            'longitude': result[1],
            'datetime': result[2],
            'city': result[3],
            'shape': result[4],
            'comments': result[5],
            'duration_hours': result[6],
            'year': result[7],
            'month': result[8]
        }
        
        big_list.append(obj)

    data=jsonify(big_list)
    return data


@app.route("/d3")
def d3():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    return render_template('d3.html')


@app.route("/d3data")
def d3data():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(\
    merge_again.death_rate,\
    merge_again.population,\
    merge_again.state_sightings,\
    merge_again.smokes,\
    merge_again.fireball,\
    merge_again.light,\
    merge_again.triangle,\
    merge_again.state_abb).all()
 
    session.close()

    big_list = []

    for result in results:

        obj = {
            'death_rate': result[0],
            'population': result[1],
            'state_sightings': result[2],
            'smokes': result[3],
            'fireball': result[4],
            'light': result[5],
            'triangle': result[6],
            'state_abb': result[7]
        }
        
        big_list.append(obj)

    data=jsonify(big_list)
    
    return data


@app.route("/explore")
def explore():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    return render_template('explore.html')


@app.route("/exploredata")
def exploredata():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(
        ufo_data.datetime,
        ufo_data.city,
        ufo_data.state,
        ufo_data.country,
        ufo_data.shape,
        ufo_data.duration,
        ufo_data.duration_hours,
        ufo_data.comments,
        ufo_data.date_posted,
        ufo_data.latitude,
        ufo_data.longitude,
        ufo_data.year,
        ufo_data.month)\
        .filter((ufo_data.year == 2014) & (ufo_data.month < 3)).all()

    session.close()

    print(results[0:10])

    data=jsonify(results)
    return data


if __name__ == '__main__':
    app.run(debug=True)