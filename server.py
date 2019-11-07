from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re
from datetime import datetime
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "unicorn"
bcrypt = Bcrypt(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/storms/<int:storm_id>')
def showinfo(storm_id):

    data = {
	
	"storm_id" : storm_id

	}
    query = "SELECT * FROM ideas WHERE id = %(storm_id)s"
    mysql = connectToMySQL('ideas_db')
    idea = mysql.query_db(query, data)[0]

    data = {
	
	"storm_id" : storm_id

	}
    query = "select users.name from users  join likes  on likes.user_id = users.id join ideas on likes.idea_id = ideas.id where ideas.id = %(storm_id)s"
    mysql = connectToMySQL('ideas_db')
    guests = mysql.query_db(query, data)


    query = 'SELECT * FROM users WHERE id = %(id)s'
    data = {'id':session['user']}
    mysql = connectToMySQL('ideas_db')
    user = mysql.query_db(query, data)

    data = {
	
	"storm_id" : storm_id,
    'user_name':user[0]['name']

	}
    query = "select users.name from users  join likes  on likes.user_id = users.id join ideas on likes.idea_id = ideas.id where ideas.id = %(storm_id)s and users.name = %(user_name)s"
    mysql = connectToMySQL('ideas_db')
    going = mysql.query_db(query, data)






    



    return render_template('storm.html', idea = idea, guests = guests, going = going )

@app.route('/edit/<int:storm_id>')
def edit(storm_id):

    query = 'SELECT * FROM users WHERE id = %(id)s'
    data = {'id':session['user']}
    mysql = connectToMySQL('ideas_db')
    user = mysql.query_db(query, data)

    data = {
	
	"storm_id" : storm_id

	}
    query = "SELECT * FROM ideas WHERE id = %(storm_id)s"
    mysql = connectToMySQL('ideas_db')
    idea = mysql.query_db(query, data)[0]




    return render_template('edit.html', idea = idea, user = user )

@app.route('/update/<int:idea_id>',methods=['POST'])
def update(idea_id):

    name = request.form['name']
    error = False

    if(len(name) < 1):
     flash('Pleae Enter New Storm Name', 'error')
     error = True
    if(error):
        return redirect('/edit/'+ str(idea_id) )
    else:
    


        mysql = connectToMySQL('ideas_db')
        query= "UPDATE `ideas` SET `name` = %(name)s WHERE `id` = %(idea_id)s"
        data= {'idea_id': idea_id,
                'name' : name
        
        }

        mysql.query_db(query, data)


        return redirect('/mystorms')


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

@app.route('/signup')
def signup():
	return render_template('register.html')

@app.route('/home')
def home():
    query = "select * from ideas ORDER BY id DESC"
    mysql = connectToMySQL('ideas_db')
    ideas = mysql.query_db(query)

    
    query = 'SELECT * FROM users WHERE id = %(id)s'
    data = {'id':session['user']}
    mysql = connectToMySQL('ideas_db')
    user = mysql.query_db(query, data)




    return render_template('home.html', ideas = ideas, user = user)

@app.route('/mystorms')
def mystorms():


    
    query = 'SELECT * FROM users WHERE id = %(id)s '
    data = {'id':session['user']}
    mysql = connectToMySQL('ideas_db')
    user = mysql.query_db(query, data)

    query = 'select * from ideas Where creator =  %(name)s'
    data ={'name':user[0]['name']}
    mysql = connectToMySQL('ideas_db')
    myideas = mysql.query_db(query, data)






    return render_template('mystorms.html', myideas = myideas, user = user)

@app.route('/new')
def new():
    query = 'SELECT * FROM users WHERE id = %(id)s'
    data = {'id':session['user']}
    mysql = connectToMySQL('ideas_db')
    user = mysql.query_db(query, data)

    return render_template('create.html', user = user)

@app.route('/create', methods=['POST'])
def create():

    name = request.form['name']
    creator = request.form['creator']
    if(len(name) < 1):
        flash('Please Name Your Storm', 'error')

        return redirect('/new')
    

    mysql = connectToMySQL('ideas_db')
    query= "INSERT INTO ideas(name, creator, created_at, updated_at) \
            VALUES(%(name)s, %(creator)s, now(), now());"
    data= {'name': name,
          'creator': creator,
    }

    idea_id = mysql.query_db(query, data)


    return redirect('/success/'+ str(idea_id) )

@app.route('/success/<int:idea_id>')
def success(idea_id):

    data = {
	
	"idea_id" : idea_id

	}
    query = "SELECT * FROM ideas WHERE id = %(idea_id)s"
    mysql = connectToMySQL('ideas_db')
    idea = mysql.query_db(query, data)[0]


    return render_template('success.html', idea = idea)

@app.route('/delete/<int:idea_id>')
def delete(idea_id):

 

    mysql = connectToMySQL('ideas_db')
    query= "DELETE from ideas where id = %(idea_id)s"
    data= {'idea_id': idea_id
    
    }

    mysql.query_db(query, data)


    return redirect('/mystorms')

@app.route('/storms/join/<int:idea_id>')
def join(idea_id):


	
	data = {

	"idea_id" : idea_id,

	"user_id"	:	session['user'],
	
    }

	query = "INSERT INTO likes (idea_id, user_id) VALUES (%(idea_id)s,%(user_id)s);"
	mysql = connectToMySQL('ideas_db')
	mysql.query_db(query, data)

	return redirect('/home')

@app.route('/join/<int:idea_id>')
def ijoin(idea_id):


	
	data = {

	"idea_id" : idea_id,

	"user_id"	:	session['user'],
	
    }

	query = "INSERT INTO likes (idea_id, user_id) VALUES (%(idea_id)s,%(user_id)s);"
	mysql = connectToMySQL('ideas_db')
	mysql.query_db(query, data)

	return redirect('/storms/' + str(idea_id) )

@app.route('/unjoin/<int:idea_id>')
def unjoin(idea_id):


	
	data = {

	"idea_id" : idea_id,

	"user_id"	:	session['user'],
	
    }

	query = "Delete From likes where idea_id = %(idea_id)s and user_id = %(user_id)s;"
	mysql = connectToMySQL('ideas_db')
	mysql.query_db(query, data)

	return redirect('/storms/' + str(idea_id) )



@app.route('/login', methods=['POST'])
def login():
  email = request.form['email']
  password = request.form['password']
  matched_email = re.match(r'.+@\w+\.[a-z]{2,3}', email)
  error = False

  if(len(email) < 1 ):
    flash('Email is required', 'error')
    error =  True
  if( len(password) < 1 ):
    flash('Password is required', 'error')
    error =  True

  
  if(email is None or matched_email is None):
     flash('Email is invalid', 'error')
     error = True
    
  if(error):
        return redirect('/')


  else:
# Go to the DB find records with the matching email
    mysql = connectToMySQL('ideas_db')
    query_string = 'SELECT * from users WHERE email = %(email)s'
    data = {'email': email}
    result = mysql.query_db(query_string, data) # Return a list of matching user(dict)
    same_password = bcrypt.check_password_hash(result[0]['password'], password)

    
    if(result != [] and same_password):
        session['user'] = result[0]['id']
        return redirect('/home')
    else:
        flash('Invalid Password', 'error')
 
        return redirect('/')


@app.route('/register', methods=['POST'])
def register():

  name = request.form['name']
  email = request.form['email']
  password = request.form['password']
  password_confirmation = request.form['confirm_password']

  error = False
  # Validation start here
  if(name is None or len(name) < 3 ):
    flash('Name is too short', 'error')
    error = True



  # use regular expression to check the validity of the email
  matched_email = re.match(r'.+@\w+\.[a-z]{2,3}', email)

  # query the DB to see if there is any record with the input email?
  # if there is we dont want to create a new account
  mysql = connectToMySQL('ideas_db')
  query = 'SELECT * from users WHERE email = %(email)s'
  data = {'email': email}
  email_existed = mysql.query_db(query, data)

  if(email is None or matched_email is None):
     flash('Email is invalid', 'error')
     error = True
  
  if(email_existed):
     flash('Email already exists', 'error')
     error = True

  if(password == "" or password_confirmation == "" or password != password_confirmation):
    flash('Password and password confirmation is invalid', 'error')
    error =  True

  if( len(password) < 8 ):
    flash('Password is too short', 'error')
    error =  True

# Validation end

  if(error):
    return redirect('/signup')
  else:
    # Generate a hashed password
    pw_hash = bcrypt.generate_password_hash(password)

    # Create a new user in the DB with the information provided
    mysql = connectToMySQL('ideas_db')
    query= "INSERT INTO users(name, email, password, created_at, updated_at) \
            VALUES(%(name)s,%(email)s, %(password_hash)s, now(), now());"
    data= {'name': name,
          'email': email,
          'password_hash': pw_hash}
    mysql.query_db(query, data)
 
    # Redirect with a success flash
    flash('Successfully created a account!!!!', 'success')
    return redirect('/home')



if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)