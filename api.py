from flask import Flask
from flask import *
from settings import *
import sqlite3

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# query string is of the following format
# 'http://localhost:5000/jobs?name=<STRING>&id=<STRING>&...'
# name = <string>
# id = <string>
# other parameters = (date posted?, zipcode?, education?, etc.)


@app.route('/jobs')
def get_jobs():
    c = get_db().cursor()

    # Build the query string
    query = 'SELECT * FROM listings'
    join_str = ' WHERE '

    # Get the parameters from the url
    name = request.args.get('name')
    id_num = request.args.get('id')
    city = request.args.get('city')
    state = request.args.get('state')
    industry = request.args.get('industry')
    company = request.args.get('company')
     
    # Build the query string by appending values
    # city state industry company 
   
    if name is not None:
        query += join_str + ('name = %s' % (name))
        join_str = ' AND '
    if id_num is not None:
        query += join_str + ('id = %s' % (id_num))
        join_str = ' AND '
    if city is not None:
        query += join_str + ('city = %s' % (city))
        join_str = ' AND '
    if state is not None:
        query += join_str + ('state = %s' % (state))
        join_str = ' AND '
    if industry is not None:
        query += join_str + ('industry = %s' % (industry))
        join_str = ' AND '
    if company is not None:
        query += join_str + ('company = %s' % (company))
        join_str = ' AND '

    for row in c.execute(query):
        print row

    # Build a list with the tuples returned from sqlite and return a json
    return jsonify({'jobs': '\n'.join([', '.join(r) for r in c])})

if __name__ == "__main__":
    app.run(debug=True)
