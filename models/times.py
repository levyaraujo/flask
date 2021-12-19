from alchemy import db


class TeamModel(db.Model):
    __tablename__ = 'times'
    time_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(50))
    libertadores = db.Column(db.Integer)
    brasileiro = db.Column(db.Integer)
    fundacao = db.Column(db.Integer)
    cidade = db.Column(db.String(40))

    def __init__(self, time_id, nome, libertadores, brasileiro, fundacao,
                 cidade):
        self.time_id = time_id
        self.nome = nome
        self.libertadores = libertadores
        self.brasileiro = brasileiro
        self.fundacao = fundacao
        self.cidade = cidade

    def json(self):
        return {
            'time_id': self.time_id,
            'nome': self.nome,
            'libertadores': self.libertadores,
            'brasileiro': self.brasileiro,
            'fundacao': self.fundacao,
            'cidade': self.cidade
        }

    @classmethod
    def find_team(cls, time_id):
        time = cls.query.filter_by(time_id=time_id).first(
        )  # SELECT * FROM times WHERE time_id = $time_id
        if time:
            return time
        return None

    def save_team(self):
        db.session.add(self)
        db.session.commit()

    def update_team(self, nome, libertadores, brasileiro, fundacao, cidade):
        self.nome = nome
        self.libertadores = libertadores
        self.brasileiro = brasileiro
        self.fundacao = fundacao
        self.cidade = cidade

    def delete_team(self):
        db.session.delete(self)
        db.session.commit()