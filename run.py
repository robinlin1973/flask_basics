from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:325363@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_flask():
    return "Hello Flask"


@app.route('/new/')
def query_string(greeting = 'hello'):
    query_val = request.args.get('greeting',greeting)
    return '<h1>the greeting is:{0} </h1>'.format(query_val)


@app.route('/user/')
@app.route('/user/<name>')
def no_query_string(name = 'user'):
    return '<h1>hello there ! {} </h1>'.format(name)

#String
@app.route('/text/<string:name>')
def show_string(name):
    return '<h1>Here is a string: {} </h1>'.format(name)

#numbers
@app.route('/numbers/<int:num>')
def show_numbers(num):
    return '<h1>Here is a number: {} </h1>'.format(num)


#floats
@app.route('/add/<int:num1>/<int:num2>')
def adding(num1,num2):
    return '<h1>the sume is: {} </h1>'.format(num1+num2)


@app.route('/temp')
def using_templates():
    return render_template("hello.html")

#JUNJA TEMPLATES
@app.route('/watch')
def movies_2017():
    movie_list = [
        'autopsy of jane doe',
        'neon demon',
        'ghost in a shell',
        'kong: skull island',
        'john wick 2',
        'spiderman - homecoming'
    ]
    return render_template('movies.html',
                           movies=movie_list,
                           name = 'Harry'
                           )

@app.route('/table')
def movies_table():
    movie_dict = {
        'autopsy of jane doe':02.14,
        'neon demon':3.20,
        'ghost in a shell':1.50,
        'kong: skull island':3.50,
        'john wick 2':02.52,
        'spiderman - homecoming':1.48
    }
    return render_template('table_data.html',
                           movies=movie_dict,
                           name = 'Nina'
                           )

@app.route('/filters')
def filter_data():
    movie_dict = {
        'autopsy of jane doe':02.14,
        'neon demon':3.20,
        'ghost in a shell':1.50,
        'kong: skull island':3.50,
        'john wick 2':02.52,
        'spiderman - homecoming':1.48
    }
    return render_template('filter_data.html',
                           movies=movie_dict,
                           name = 'Nina',
                           films = 'a christmas carol' )

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(500),nullable=False,index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100),unique = True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime,default = datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer,db.ForeignKey('publication.id'))

    def __init__(self,title,author,avg_rating,format,image,num_pages,pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id


    def __repr__(self):
        return '{} by {}'.format(self.title,self.author)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)