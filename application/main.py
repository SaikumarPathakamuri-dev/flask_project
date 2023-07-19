from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import Schema,fields
# from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root123@localhost/sai1234"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    discription = db.Column(db.String(255))
    email_id=db.Column(db.String(120))
    education=db.relationship('Education',backref='user')

class Education(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

class userSchema(Schema):
    id=fields.Integer()
    name=fields.String()
    discription=fields.String()
    email_id=fields.String()
class EducationSchema(Schema):
    id=fields.Integer()
    name=fields.String()
    user_id=fields.Integer()
@app.route('/get_users',methods=['GET'])
def get_all():
    data=User.query.all()
    serializer=userSchema(many=True)
    serialized_data=serializer.dump(data)
    return jsonify (
        serialized_data
    )

@app.route('/add_user',methods=['POST'])
def post_user():
    data=request.get_json()
    education = data['education']
    new_User=User(name=data.get('name'),discription=data.get('discription'),email_id=data.get('email_id'))
    db.session.add(new_User)
    db.session.commit()
    for i in education:
        new_education=Education(name=i.get('name'),user_id=i.get('user_id'))
        db.session.add(new_education)
        db.session.commit()
    return ("created successfully")

@app.route('/get_user/<int:id>',methods=['GET'])
def get_user_by_id(id):
    user=User.query.get(id)
    education=Education.query.filter_by(user_id=id)
    serializer_user=userSchema()
    serializer_edu=EducationSchema()
    data_user=serializer_user.dump(user)
    data_education_list=serializer_edu.dump(education,many=True)
    data_user['education'] = data_education_list 
    return jsonify(
     data_user
    )

@app.route('/update_user/<int:id>',methods=['PUT'])
def update_user_by_id(id):
    user=User.query.get_or_404(id)
    data=request.get_json()
    user.name=data.get('name')
    user.discription=data.get('discription')
    db.session.commit()
    serializer=userSchema()
    json_output=serializer.dump(user)
    return jsonify(
        json_output
    )

@app.route("/")
def pradeep():
    return "pradeep"

if __name__ == '__main__':
    app.run(debug=True,)
