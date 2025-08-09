from decimal import Decimal
from .. import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_account = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True, order_by="desc(Transaction.date)")

    def __repr__(self):
        return f"<Account(name_account='{self.name_account}', balance={self.balance:.2f})>"
