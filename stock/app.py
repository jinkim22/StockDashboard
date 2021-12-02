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

@app.route('/signup')
def signup():
 
#  print(request.args)


  return render_template("register.html")

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
        return redirect('/signup')
    elif password == password2:
        g.conn.execute('INSERT INTO traders(username,password, pwd.password) VALUES (%s,%s,ARRAY[%s])',(username,password,password))
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
            session['trade_freq']=account['trade_freq']
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
        row1 = g.conn.execute('SELECT array_length((pwd).QA, 1) AS total FROM traders WHERE id = %s',session['id'])
        account1 = row1.fetchone()
        if account1['total'] == None:
             return render_template("security.html",data = row, user_id = session['id'])
        return render_template("portfolio.html",data = row, user_id = session['id'])
    else:
        return redirect(url_for('login'))

@app.route("/security", methods = ['GET','POST'])
def security():
    if request.method == 'POST':
        Q1 = request.form['Q1']
        A1 = request.form['A1']
        Q2 = request.form['Q2']
        A2 = request.form['A2']
        Q3 = request.form['Q3']
        A3 = request.form['A3']
        

        
        g.conn.execute('UPDATE traders SET pwd.QA = ARRAY[[%(a)s, %(b)s]] WHERE id = %(c)s ',{"a":Q1, "b":A1, "c":session['id']})
        
        print(Q1)
        print(A1)
        g.conn.execute('UPDATE traders SET pwd.QA = (pwd).QA || ARRAY[[%(a)s , %(b)s]] WHERE id = %(c)s', {"a":Q2, "b":A2, "c":session['id']})
        g.conn.execute('UPDATE traders SET pwd.QA = (pwd).QA || ARRAY[[%(a)s , %(b)s]] WHERE id = %(c)s', {"a":Q3, "b":A3, "c":session['id']})
    if 'logged' in session:
        print(" it is loc")
    else:
        print(" no it is notr ")
    
    return redirect(url_for('portfolio'))

@app.route("/forgot", methods = ['POST','GET'])
def forgot():
    return render_template("reset.html")


@app.route("/reset", methods = ['POST','GET'])
def reset():
    
    if request.method == 'POST':
        username = request.form['username']
        Q1 = request.form['Q1']
        A1 = request.form['A1']
        Q2 = request.form['Q2']
        A2 = request.form['A2']
        Q3 = request.form['Q3']
        A3 = request.form['A3']

        row =  g.conn.execute('SELECT * FROM traders WHERE username = %s',(username))
        account = row.fetchone()
       

        if account is None:
            flash("Username does not exist")

            return redirect(url_for('reset'))
        else:
            row1 = g.conn.execute('SELECT (pwd).QA[1][1] AS q1 FROM traders WHERE username = %s',(username))
            rowA1 = g.conn.execute('SELECT (pwd).QA[1][2] AS a1 FROM traders WHERE username = %s',(username))
            account1 = row1.fetchone()
            answer1 = rowA1.fetchone()

            row2 = g.conn.execute('SELECT (pwd).QA[2][1] AS q2 FROM traders WHERE username = %s',(username))
            rowA2 = g.conn.execute('SELECT (pwd).QA[2][2] AS a2 FROM traders WHERE username = %s',(username)) 
            account2 = row2.fetchone()
            answer2 = rowA2.fetchone()
            
            row3 = g.conn.execute('SELECT (pwd).QA[3][1] AS q3 FROM traders WHERE username = %s',(username))
            rowA3 = g.conn.execute('SELECT (pwd).QA[3][2] AS a3 FROM traders WHERE username = %s',(username))
            account3 = row3.fetchone()
            answer3 = rowA3.fetchone()
            
            print("q1 is:",account1['q1'])
            if account1['q1'] != Q1 or answer1['a1']!=A1:

                flash("Incorrect answer a1!")
                print("they are the same")
                return redirect(url_for('forgot'))
           
            print("q1 is:",account1['q1'], Q1, " ", answer1['a1'], A1)
            if account2['q2'] != Q2 or answer2['a2']!=A2:

                flash("Incorrect answer a2!")
                return redirect(url_for('forgot'))
           
           
           
            print("q2 is:",account2['q2'], Q2, " ", answer2['a2'], A2)
            if account3['q3'] != Q3 or answer3['a3']!=A3:
                flash("Incorrect answer a3!")
                return redirect(url_for('forgot'))
     #           session['reset'] = True
    #            session['id'] = account['id']
   #             session['username']= account['username']
  #              session['trade_freq']=account['trade_freq']
            #return redirect(url_for('portfolio'))

           
            print("q3 is:",account3['q3'], Q3, " ", answer3['a3'], A3)
            return render_template("password.html")
    
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

@app.route("/portfolio_contents", methods=['POST','GET'])
def portfolio_contents():
     
    if request.method == 'POST':
        performance = request.form['performance']
        pname = request.form['pname']
        portfolio_id = request.form['portfolio_id']
    else:
        portfolio_id = session['pid']
        pname = session['pname']
        performance = session['performance']
    row = g.conn.execute('SELECT * FROM has_a_list_of h LEFT JOIN companies c ON h.ticker=c.ticker WHERE portfolio_id = %s',portfolio_id)
    row2 = g.conn.execute('SELECT * FROM has_a_history_of h LEFT JOIN transactions t ON h.transaction_id=t.transaction_id WHERE portfolio_id = %s',portfolio_id)
    row3 = g.conn.execute('SELECT * FROM portfolio_audit WHERE portfolio_id = %s',portfolio_id)

    account = row.fetchone()   
    print("performacne ", performance)
    access = 1
#    account = None
    if account is None:
        access = 0
        print("emmty")
    account2 = row2.fetchone()
    access2 = 1
    if account2 is None:
        access2 = 0
     #   print("access ",access2)
  #  print("trans  :",account2['transaction_id'])
    
    account3 = row3.fetchone()
    access3 = 1
    if account3 is None:
        access3 = 0
    k = float(performance) 
    print("k ",k)
  #  row = g.conn.execute('SELECT * FROM has_a_list_of h LEFT JOIN companies c ON h.ticker=c.ticker WHERE portfolio_id = %(mv)s',{"mv":portfolio_id,})
    row2 = g.conn.execute('SELECT * FROM has_a_history_of h LEFT JOIN transactions t ON h.transaction_id=t.transaction_id WHERE portfolio_id = %s ORDER BY time DESC',portfolio_id)
#    for r in row2:
     #   print("trer ", r['ticker'])
 #       print("transaction ", r['transaction_id'])
    row = g.conn.execute('SELECT *, number_of_shares_suggested/total*100 AS Allocation FROM (SELECT * FROM has_a_list_of h LEFT JOIN (SELECT c.portfolio_id AS pd, sum(c.number_of_shares_suggested) AS total FROM (SELECT * FROM has_a_list_of h LEFT JOIN companies c ON h.ticker=c.ticker WHERE portfolio_id = %(d)s) AS c GROUP BY c.portfolio_id) AS c ON h.portfolio_id=c.pd) AS h LEFT JOIN companies c ON h.ticker=c.ticker WHERE portfolio_id = %(d)s',{"d":portfolio_id})
    
    row3 = g.conn.execute('SELECT * FROM portfolio_audit WHERE portfolio_id = %s ORDER BY entrydate DESC',portfolio_id)

  #  for i in row4:
   #     print("stock n.", i['stock_name'])
#    print("p_id",portfolio_id)
    return render_template('list_company.html',data3= row3,access3 = access3, pname=pname,portfolio_id = portfolio_id,k=k,data =row,access=access,data2 = row2,access2 =access2, performance=performance )
@app.route("/remove_cpn",methods = ['GET','POST'])
def remove_cpn():
     
    if request.method == 'POST':
        portfolio_id = request.form['portfolio_id']
        ticker = request.form['ticker']
        pname = request.form['pname']
        performance = request.form['performance']
        g.conn.execute('DELETE FROM has_a_list_of WHERE portfolio_id = %(p)s AND ticker = %(t)s',{"p":portfolio_id,"t":ticker})
                
        session['pid'] = portfolio_id
        session['pname'] = pname
        session['performance'] = performance
        
        return redirect(url_for('portfolio_contents'))

@app.route("/insert_cpn",methods = ['GET','POST'])
def insert_cpn():
    if 'logged' in session:
        ticker = request.form['ticker']
        portfolio_id = request.form['portfolio_id']
        pname = request.form['pname']
        performance = request.form['performance']
        session['pid'] = portfolio_id
        session['pname'] = pname
        session['performance'] = performance
        g.conn.execute('INSERT INTO has_a_list_of(portfolio_id,ticker) VALUES (%s,%s)',portfolio_id,ticker)
        return redirect(url_for('portfolio_contents'))

@app.route("/add_company",methods = ['POST','GET'])
def add_company():
    print("hello")
    portfolio_id = request.form['portfolio_id']
    print(portfolio_id)
    pname = request.form['pname']
    performance = request.form['performance']
    row = g.conn.execute('SELECT * FROM companies WHERE ticker NOT IN(SELECT ticker FROM has_a_list_of WHERE portfolio_id = %s)',portfolio_id)
    return render_template("add_ticker.html",data=row,portfolio_id=portfolio_id, performance=performance, pname=pname)

@app.route("/price_history",methods = ['GET','POST'])
def price_history():
    ticker = request.form['ticker']
    row = g.conn.execute('SELECT * FROM price_history WHERE ticker = %s ORDER BY time DESC',ticker)
    return render_template("price_history.html",data = row)

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

