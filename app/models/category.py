from .. import db

class Category(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'user_id', name='_user_category_uc'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
