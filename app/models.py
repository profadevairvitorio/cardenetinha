from decimal import Decimal
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import event, update
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_account = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=Decimal('0.00'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True, order_by="desc(Transaction.date)")

    def __repr__(self):
        return f"<Account(name_account='{self.name_account}', balance={self.balance:.2f})>"


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


class Category(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'user_id', name='_user_category_uc'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Category(name='{self.name}')>"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='goal', uselist=False)

    @property
    def current_amount(self):
        return self.account.balance if self.account else Decimal('0.00')

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

class FinancialPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    type = db.Column(db.String(7), nullable=False)  # 'entrada' or 'despesa'
    plan_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='financial_plans', lazy=True)

    def __repr__(self):
        return f"<FinancialPlan(description='{self.description}', amount={self.amount:.2f}, type='{self.type}')>"


@event.listens_for(Transaction, 'after_insert')
def update_account_balance(mapper, connection, target):
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