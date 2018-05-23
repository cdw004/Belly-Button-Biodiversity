import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DataSets/belly_button_biodiversity.sqlite"
#db = SQLAlchemy(app)
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
Sample = Base.classes.samples
OTU = Base.classes.otu
Metadata = Base.classes.samples_metadata
session = Session(engine)

session = Session(engine)

#################################################
@app.route("/")
#"""Return the dashboard homepage."""
def home():
    return render_template('index.html')
################################################################
@app.route('/names')
#    """List of sample names.

#    Returns a list of sample names in the format
#    [
#        "BB_940",
#        "BB_947",
#        ...
#    ]
#    """
def names():
    samp_names = session.query(Samples).statement
    samp_df=pd.read_sql_query(samp_names,session.bind)
    samp_df.set_index('otu_id',inplace=True)
    return jsonify(list(samp_df.columns))

################################################################
@app.route('/otu')
#    """List of OTU descriptions.

#    Returns a list of OTU descriptions in the following format

#    [
#        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
#        "Bacteria",
#        ...
#    ]
#    """
def otu():
    otus = session.query(OTU).statement
    otus_df=pd.read_sql_query(otus,session.bind)
    otus_df.set_index('otu_id',inplace=True)
    return jsonify(list(otus_df))
################################################################
@app.route('/metadata/<sample>')
#    """MetaData for a given sample.

#    Args: Sample in the format: `BB_940`

#    Returns a json dictionary of sample metadata in the format

#    {
#        AGE: 24,
#        BBTYPE: "I",
#        ETHNICITY: "Caucasian",
#        GENDER: "F",
#        LOCATION: "Beaufort/NC",
#        SAMPLEID: 940
#    }
#    """
def metadata(sample):
    samp_meta = session.query(Metadata).statement
    samp_meta_df=pd.read_sql_query(samp_meta,session.bind)
    samp_num=int(sample.split("_")[1])
    selected_sample = samp_meta_df.loc[samp_meta_df["SAMPLEID"] == samp_num, :]
    json_selected_sample = selected_sample.to_json(orient='records')
    return json_selected_sample
################################################################
@app.route('/wfreq/<sample>')
#    Weekly Washing Frequency as a number.
#    Args: Sample in the format: `BB_940`
#    Returns an integer value for the weekly washing frequency `WFREQ`
def metadata(sample):
    samp_meta = session.query(Metadata).statement
    samp_meta_df=pd.read_sql_query(samp_meta,session.bind)
    samp_num=int(sample.split("_")[1])
    selected_sample = samp_meta_df.loc[samp_meta_df["SAMPLEID"] == samp_num, :]
    wfreq = selected_sample["WFREQ"].values[0]
    return f"{wfreq}"
################################################################
@app.route('/samples/<sample>')
#    """OTU IDs and Sample Values for a given sample.
#    Sort your Pandas DataFrame (OTU ID and Sample Value)
#    in Descending Order by Sample Value
#    Return a list of dictionaries containing sorted lists  for `otu_ids`
#    and `sample_values`
#    [
#        {
#            otu_ids: [
#                1166,
#                2858,
#                481,
#                ...
#            ],
#            sample_values: [
#                163,
#                126,
#                113,
#                ...
#            ]
#        }
#    ]
#    """
def samples(sample):
    otus = session.query(OTU).statement
    otus_df=pd.read_sql_query(otus,session.bind)
    otus_df.set_index('otu_id',inplace=True)
    samp_names = session.query(Samples).statement
    samp_df=pd.read_sql_query(samp_names,session.bind)
    samp_df.set_index('otu_id',inplace=True)
    sel_samp = samp_df[sample]
    otus_id = samp_df['otu_id']
    sel_df = pd.select({
        "otus_id":otu_ids,
        "samples":sel_samp
    })

    sorted_df = sel_df.sort_values(by=['samples'], ascending=False)
    sorted_otus = {"otu_ids": list(sorted_df['otu_ids'].values)}
    sorted_samples = {"sample_values": list(sorted_df['samples'].values)}
    for i in range(len(sorted_otus["otu_ids"])):
        sorted_otus["otu_ids"][i] = int(sorted_otus["otu_ids"][i])
    for i in range(len(sorted_samples["sample_values"])):
        sorted_samples["sample_values"][i] = int(sorted_samples["sample_values"][i])
    results = [sorted_otus, sorted_samples, list(all_otus_df["lowest_taxonomic_unit_found"])]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)

####resources:
#http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
#https://ucb.bootcampcontent.com/UCB-Coding-Bootcamp/UCBBEL201801DATA5-Class-Repository-DATA/blob/master/15-Interactive-Visualizations-and-Dashboards/3/Activities/Solved/07-Stu_Pet_Pals_Bonus/app.py
#https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
#https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
