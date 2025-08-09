from .. import db

class FinancialPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    type = db.Column(db.String(7), nullable=False)
    plan_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='financial_plans', lazy=True)

    def __repr__(self):
        return f"<FinancialPlan(description='{self.description}', amount={self.amount:.2f}, type='{self.type}')>"
