from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from sqlalchemy import create_engine,MetaData,String,Integer,Table,Column,Float


# Code for Database
engine = create_engine('sqlite:///my_database.db',echo=True)
meta = MetaData()
information = Table(
    'info',
    meta,
    Column('id',Integer,primary_key=True),
    Column('Name',String),
    Column('Author',String),
    Column('Rating',Float)
)

meta.create_all(engine)

conn = engine.connect()

# Code for form
class books(FlaskForm):
    book_name=StringField('Book Name')
    book_author=StringField('Book Author')
    book_rating=StringField('Book Rating')
    Add = SubmitField('Add Book')
    deletion = IntegerField('Enter the Book No You Wish to delete')
    deleting = SubmitField('Delete')
    
# Intializing the app
app = Flask(__name__)
app.config['SECRET_KEY']='secret_key'

# Routing the pages
@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add",methods=['GET','POST'])
def add():
    form = books()
    return render_template('add.html',form=form)

@app.route('/success',methods=['GET','POST'])
def success():
    form=books()
    name = form.book_name.data
    author  = form.book_author.data
    rating = form.book_rating.data
 
    # Adding Data to Database
    insert_statement=information.insert().values(Name=name,Author=author,Rating=rating)
    conn.execute(insert_statement)
    conn.commit()

# Selecting All the Values
    select_statement=information.select()
    result = conn.execute(select_statement).fetchall()
    length=len(result)
    conn.commit()

    return render_template('success.html',results=result,length=int(length),form=form)


# Deleting the Book
@app.route('/deletion',methods=['GET','POST'])
def deletion():
    form=books() 
    deletion = form.deletion.data
    deletion_statement=information.delete().where(information.c.id ==deletion)
    conn.execute(deletion_statement)
    conn.commit()  
    select_statement=information.select()
    result = conn.execute(select_statement).fetchall()
    length=len(result)
    conn.commit()
    return render_template('deletion.html',new_results=result,new_length=int(length),form=form)
   

   
    # Returing the page
if __name__ == "__main__":
    app.run(debug=True)

