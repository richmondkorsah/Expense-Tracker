from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False) 
    amount = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Expense %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        expense_item = request.form['item']
        expense_category = request.form['category']
        expense_amount = float(request.form['amount']) 
        expense_amount = round(expense_amount, 2) 

        new_expense = Expense(item=expense_item, category=expense_category, amount=expense_amount)

        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the expense'
    else:
        expenses = Expense.query.order_by(Expense.date_added).all()
        return render_template('index.html', expenses=expenses)


@app.route('/delete/<int:id>')
def delete(id):
    expense_to_delete = Expense.query.get_or_404(id)

    try:
        db.session.delete(expense_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this expense'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.item = request.form['item']
        expense.category = request.form['category']
        expense.amount = request.form['amount']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the expense'
    else:
        return render_template('update.html', expense=expense)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
