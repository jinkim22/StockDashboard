import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import flash,Flask,session, request, render_template, g, redirect, Response, url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

app.secret_key = 'coms4111'

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://mh4142:0804@35.196.73.133/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS traders (
  id serial primary key,
  username text,
  password text,
  trade_freq text
);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():
 
  print(request.args)


  return render_template("index.html")


@app.route('/register', methods = ['POST'])
def register():
    username = request.form['firstn']
 #   return username
    password = request.form['password']
    password2 = request.form['password2']
    row =  g.conn.execute('SELECT * FROM traders WHERE username = %s',(username))
    account = row.fetchone()
    print(account)
    if account:
        flash("\nUsername exist!")
        return redirect('/')
    elif password == password2:
        g.conn.execute('INSERT INTO traders(username,password) VALUES (%s,%s)',(username,password))
        return redirect(url_for('login'))
    else:
        return render_template("index.html")

@app.route('/login', methods = ['POST','GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        row =  g.conn.execute('SELECT * FROM traders WHERE username = %s',(username))
        account = row.fetchone()
       

        if account is None:
            flash("Username does not exist")

            return redirect(url_for('login'))
        elif password != account['password']:
            
            print(account['password'])
            flash("Username or Password is incorrect")
            return redirect(url_for('login'))
        elif password == account['password']:
            session['logged'] = True
            session['id'] = account['id']
            session['username']= account['username']
            return redirect(url_for('portfolio'))

        #    return account['password']

    return render_template('login.html')

@app.route("/portfolio", methods = ['GET','POST'])
def portfolio():
    if 'logged' in session:
       # logins = True
        row = g.conn.execute('SELECT * FROM portfolios WHERE user_id = %s',session['id'])
       # account = row.fetchone()
        print(row)
        return render_template("portfolio.html",data = row, user_id = session['id'])
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods = ['GET'])
def logout():
    session.pop('logged')
    session.pop('id')
    session.pop('username')
    return redirect(url_for('login'))

@app.route("/createp",methods = ['GET','POST'])
def createp():
    return render_template("createp.html")

@app.route("/insertp",methods = ['POST','GET'])
def insertp():
    if 'logged' in session:
        name = request.form['name']
        description = request.form['description']

        g.conn.execute('INSERT INTO portfolios(name,description,user_id) VALUES (%s,%s,%s)',(name,description,session['id']))
        return redirect(url_for('portfolio'))

@app.route("/portfolio_contents", methods=['POST'])
def portfolio_contents():
    portfolio_id = request.form['portfolio_id']
    row = g.conn.execute('SELECT * FROM has_a_list_of h LEFT JOIN companies c ON h.ticker=c.ticker WHERE portfolio_id = %s',portfolio_id)

    print("p_id",portfolio_id)
    return render_template('list_company.html',portfolio_id = portfolio_id,data =row)

@app.route("/insert_cpn",methods = ['GET','POST'])
def insert_cpn():
    if 'logged' in session:
        ticker = request.form['ticker']
        portfolio_id = request.form['portfolio_id']
        g.conn.execute('INSERT INTO has_a_list_of(portfolio_id,ticker) VALUES (%s,%s)',portfolio_id,ticker)
        return redirect(url_for('portfolio'))

@app.route("/add_company",methods = ['POST','GET'])
def add_company():
    print("hello")
    portfolio_id = request.form['portfolio_id']
    print(portfolio_id)
    row = g.conn.execute('SELECT * FROM companies WHERE ticker NOT IN(SELECT ticker FROM has_a_list_of WHERE portfolio_id = %s)',portfolio_id)
    return render_template("add_ticker.html",data=row,portfolio_id=portfolio_id)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

