from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Ensure database file path is correct
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # New column for "Mark as Done"

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect('/')

# ✅ New route to mark a task as done
@app.route('/done/<int:task_id>')
def mark_done(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed  # Toggle task completion
        db.session.commit()
    return redirect('/')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        new_content = request.form.get('task')
        if new_content:
            task.content = new_content
            db.session.commit()
        return redirect('/')
    return render_template('edit.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
