from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
api = Api(app)

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', back_populates='questionnaire', cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'ouverte' ou 'qcm'
    choices = db.Column(db.String(500))  # Options séparées par des virgules pour QCM
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=False)
    questionnaire = db.relationship('Questionnaire', back_populates='questions')

questionnaire_model = api.model("Questionnaire", {
    "id": fields.Integer,
    "title": fields.String,
    "questions": fields.List(fields.Nested(api.model("Question", {
        "id": fields.Integer,
        "text": fields.String,
        "type": fields.String,
        "choices": fields.String,
    })))
})

questionnaire_input_model = api.model("QuestionnaireInput", {
    "title": fields.String(required=True)
})

question_model = api.model("Question", {
    "id": fields.Integer,
    "text": fields.String,
    "type": fields.String,
    "choices": fields.String,
    "questionnaire_id": fields.Integer
})

question_input_model = api.model("QuestionInput", {
    "text": fields.String(required=True),
    "type": fields.String(required=True),
    "choices": fields.String,
    "questionnaire_id": fields.Integer(required=True)
})

ns = api.namespace("api", description="Gestion des questionnaires")

@ns.route("/questionnaires")
class QuestionnaireCollection(Resource):
    @ns.marshal_list_with(questionnaire_model)
    def get(self):
        return Questionnaire.query.all()

    @ns.expect(questionnaire_input_model, validate=True)
    @ns.marshal_with(questionnaire_model)
    def post(self):
        questionnaire = Questionnaire(title=api.payload['title'])
        db.session.add(questionnaire)
        db.session.commit()
        return questionnaire, 201

@ns.route("/questionnaires/<int:id>")
@ns.response(404, "Questionnaire non trouvé")
class QuestionnaireItem(Resource):
    @ns.marshal_with(questionnaire_model)
    def get(self, id):
        questionnaire = Questionnaire.query.get(id)
        if not questionnaire:
            abort(404, message="Questionnaire non trouvé")
        return questionnaire

    def delete(self, id):
        questionnaire = Questionnaire.query.get(id)
        if not questionnaire:
            abort(404, message="Questionnaire non trouvé")
        db.session.delete(questionnaire)
        db.session.commit()
        return {}, 204

    @ns.expect(questionnaire_input_model, validate=True)
    @ns.marshal_with(questionnaire_model)
    def put(self, id):
        questionnaire = Questionnaire.query.get(id)
        if not questionnaire:
            abort(404, message="Questionnaire non trouvé")

        # Mettre à jour le titre du questionnaire
        questionnaire.title = api.payload['title']
        db.session.commit()
        return questionnaire


@ns.route("/questions")
class QuestionCollection(Resource):
    @ns.marshal_list_with(question_model)
    def get(self):
        return Question.query.all()

    @ns.expect(question_input_model, validate=True)
    @ns.marshal_with(question_model)
    def post(self):
        questionnaire = Questionnaire.query.get(api.payload['questionnaire_id'])
        if not questionnaire:
            abort(404, message="Questionnaire non trouvé")
        question = Question(
            text=api.payload['text'],
            type=api.payload['type'],
            choices=api.payload.get('choices', None),
            questionnaire_id=api.payload['questionnaire_id']
        )
        db.session.add(question)
        db.session.commit()
        return question, 201

@ns.route("/questions/<int:id>")
@ns.response(404, "Question non trouvée")
class QuestionItem(Resource):
    @ns.marshal_with(question_model)
    def get(self, id):
        question = Question.query.get(id)
        if not question:
            abort(404, message="Question non trouvée")
        return question

    def delete(self, id):
        question = Question.query.get(id)
        if not question:
            abort(404, message="Question non trouvée")
        db.session.delete(question)
        db.session.commit()
        return {}, 204

    @ns.expect(question_input_model, validate=True)
    @ns.marshal_with(question_model)
    def put(self, id):
        question = Question.query.get(id)
        if not question:
            abort(404, message="Question non trouvée")

        # Mettre à jour la question
        question.text = api.payload['text']
        question.type = api.payload['type']
        question.choices = api.payload.get('choices', None)
        db.session.commit()
        return question

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
