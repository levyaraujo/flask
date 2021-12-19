from flask_restful import Resource, reqparse
from models.times import TeamModel
from flask_jwt_extended import jwt_required


class Times(Resource):
    def get(self):
        return {'times': [team.json() for team in TeamModel.query.all()]}


class Time(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome',
                            type=str,
                            required=True,
                            help="The field 'nome' cannot be blank")
    argumentos.add_argument('libertadores',
                            type=int,
                            required=True,
                            help="The field 'libertadores' cannot be blank")
    argumentos.add_argument('brasileiro',
                            type=int,
                            required=True,
                            help="The field 'brasileiro' cannot be blank")
    argumentos.add_argument('fundacao',
                            type=int,
                            required=True,
                            help="The field 'fundacao' cannot be blank")
    argumentos.add_argument('cidade')

    def get(self, time_id):
        team = TeamModel.find_team(time_id)
        if team:
            return team.json()
        return {'message': f'{time_id} not found'}, 404

    @jwt_required()
    def post(self, time_id):
        if TeamModel.find_team(time_id):
            return {
                'message': 'Team id {} already exists.'.format(time_id)
            }, 400

        dados = Time.argumentos.parse_args()
        team = TeamModel(time_id, **dados)
        try:
            team.save_team()
        except:
            return {
                'message':
                f'An internal error ocurred trying to save {time_id}'
            }, 500
        return team.json()

    @jwt_required()
    def put(self, time_id):
        dados = Time.argumentos.parse_args()

        team = TeamModel.find_team(time_id)
        if team:
            team.update_team(**dados)
            team.save_team()
            return team.json(), 200

        new_team = TeamModel(time_id, **dados)
        try:
            team.save_team()
        except:
            return {
                'message':
                f'An internal error ocurred trying to save {time_id}'
            }, 500
        return new_team.json(), 201  #created

    @jwt_required()
    def delete(self, time_id):
        time = TeamModel.find_team(time_id)
        if time:
            try:
                time.delete_team()
            except:
                {
                    'message':
                    f'An internal error ocurred trying to delete {time_id}'
                }, 500
            return {'message': f'{time_id} was deleted.'}

        return f'{time_id} not found.', 404
