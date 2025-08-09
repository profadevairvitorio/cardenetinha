from datetime import datetime, timezone
from sqlalchemy import event, update
from .. import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    type = db.Column(db.String(7), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='transactions', lazy=True)

    def __repr__(self):
        return f"<Transaction(description='{self.description}', amount={self.amount:.2f}, type='{self.type}')>"

@event.listens_for(Transaction, 'after_insert')
def update_account_balance(mapper, connection, target):
    from .account import Account
    account_id = target.account_id
    amount = target.amount
    transaction_type = target.type

    current_balance_result = connection.execute(
        db.select(Account.balance).where(Account.id == account_id)
    ).scalar_one_or_none()

    if current_balance_result is None:
        return

    current_balance = current_balance_result
    new_balance = current_balance

    if transaction_type == 'entrada':
        new_balance += amount
    elif transaction_type == 'saida':
        if current_balance < amount:
            raise ValueError("Saldo insuficiente para realizar a transação.")
        new_balance -= amount

    connection.execute(
        update(Account).where(Account.id == account_id).values(balance=new_balance)
    )
