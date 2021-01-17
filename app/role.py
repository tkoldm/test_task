from app import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)


    def __repr__(self):
        return f'<Role {self.id}>'