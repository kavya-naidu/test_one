from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('_name_')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Reddy%4096320@localhost:5433/amazon_app'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    age = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    data = Todo.query.all()
    context = []
    for dt in data:
        dd = {"id": dt.id, "usn": dt.usn, "name": dt.name, "age": dt.age}
        context.append(dd)
    print(context)
    # print("data: {}".format(data))
    return render_template('todo.html', todo=context)


@app.route('/add-task')
def add_task():
    return render_template('add_task.html')


@app.route('/submit', methods=['POST'])
def create_user(age=None):
    usn = request.form['usn']
    name = request.form['name']
    age = request.form['age']
    print(f"usn is: {usn}, name is: {name}, and age is: {age}")
    new_task = Todo(usn=usn, name=name, age=age)
    print("new_task: {}".format(new_task))
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('add_task'))


@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_user(id):
    task = Todo.query.get(id)
    print("task: {}".format(task))

    if not task:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    print(task.id)
    if not task:
        return jsonify({'message': 'task not found'}), 404

    if request.method == 'POST':
        task.usn = request.form['usn']
        task.name = request.form['name']
        task.age = request.form['age']

        try:
            db.session.commit()
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return "there is an issue while updating the record"
    return render_template('update.html', task=task)


if _name_ == '_main_':
    app.run(host='127.0.0.1', port=5002, debug=True)fr