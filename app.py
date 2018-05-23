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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DataSets/belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)
#################################################



@app.route("/")
    #"""Return the dashboard homepage."""
    return render_template('index.html')
################################################################
@app.route('/names')
#    """List of sample names.

#    Returns a list of sample names in the format
#    [
#        "BB_940",
#        "BB_941",
#        "BB_943",
#        "BB_944",
#        "BB_945",
#        "BB_946",
#        "BB_947",
#        ...
#    ]

#    """
def names():
    state = session.query(Samples).statement
    df=pd.read_sql_query(state,session.bind)
    df.set_index('otu_id',inplace=True)
#    sampleNames = getSampleNames()
#    return json.dumps(sampleNames)
    return jsonify(list(df.columns))

################################################################
@app.route('/otu')
#    """List of OTU descriptions.

#    Returns a list of OTU descriptions in the following format

#    [
#        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
#        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
#        "Bacteria",
#        "Bacteria",
#        "Bacteria",
#        ...
#    ]
#    """
def otu():
    otu=list(np.ravel(results))
    return jsonify(list(otu))

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
def metadata_sample:
    sel = [Samples_Metadata.SAMPLEID, Samples_Metadata.ETHNICITY,
           Samples_Metadata.GENDER, Samples_Metadata.AGE,
           Samples_Metadata.LOCATION, Samples_Metadata.BBTYPE]
    for result in results:
        metadata_sample['SAMPLEID'] = result[0]
        metadata_sample['ETHNICITY'] = result[1]
        metadata_sample['GENDER'] = result[2]
        metadata_sample['AGE'] = result[3]
        metadata_sample['LOCATION'] = result[4]
        metadata_sample['BBTYPE'] = result[5]

    return jsonify(sample_metadata)
################################################################
@app.route('/wfreq/<sample>')
#    """Weekly Washing Frequency as a number.

#    Args: Sample in the format: `BB_940`

#    Returns an integer value for the weekly washing frequency `WFREQ`
#    """
def wfreq:
    filter(Samples_Metadata.SAMPLEID == sample[3:]).all()
    wfreq = np.ravel(results)

    return jsonify(int(wfreq[0]))

################################################################
@app.route('/samples/<sample>')
#    """OTU IDs and Sample Values for a given sample.
#
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
    state = session.query(Samples).statement
    df = pd.read_sql_query(state, session.bind)

    if sample not in df.columns:
        return jsonify(f"Error! Sample: {sample} Not Found!"), 400

    df = df[df[sample] > 1]

    df = df.sort_values(by=sample, ascending=0)

    data = [{
        "otu_ids": df[sample].index.values.tolist(),
        "sample_values": df[sample].values.tolist()
    }]
    return jsonify(data)
    if __name__ == "__main__":
     app.run(debug=True)
   

####resources:
#http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
#https://ucb.bootcampcontent.com/UCB-Coding-Bootcamp/UCBBEL201801DATA5-Class-Repository-DATA/blob/master/15-Interactive-Visualizations-and-Dashboards/3/Activities/Solved/07-Stu_Pet_Pals_Bonus/app.py
#https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
#https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
