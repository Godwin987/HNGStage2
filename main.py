from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# INITIALIZE FLASK APP
app = Flask(__name__)
# CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CREATE A SESSION OBJECT
session = db.session


# PERSONS TABLE CONFIGURATION
class Persons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)


with app.app_context():
    db.create_all()

    # ADD A NEW PERSON
    @app.route('/api/', methods=['POST'])
    def add():
        # print(request.form.get("sockets"))
        new_person = Persons(
            name=request.form.get("name"),
        )
        db.session.add(new_person)
        db.session.commit()
        return jsonify(response={"success": "Successfully added a person."})

    # GET A PERSON
    @app.route('/api/<user_id>')
    def get_person(user_id):
        person = session.get(Persons, user_id)
        if not person:
            return jsonify(error={"Not Found": "Sorry, we don't have such a person in the database."})
        return jsonify(name=person.name)

    # UPDATE A PERSON
    @app.route('/api/<user_id>', methods=['PATCH'])
    def patch(user_id):
        if session.get(Persons, user_id):
            person = session.get(Persons, user_id)
            person.name = request.args.get("name")
            db.session.commit()
            # 200 OK
            return jsonify(success="Successfully updated the person record"), 200
        else:
            # 400 BAD REQUEST
            return jsonify(error={"Not Found": "Sorry, there's no one with that id."}), 400

    # DELETE A PERSON
    @app.route('/api/<user_id>', methods=['DELETE'])
    def delete(user_id):
        if session.get(Persons, user_id):
            person = session.get(Persons, user_id)
            session.delete(person)
            session.commit()
            return jsonify(success='Successfully Deleted Record'), 200


if __name__ == '__main__':
    app.run(debug=True)
