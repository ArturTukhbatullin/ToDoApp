from flask import Flask, render_template, request,\
      redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Настройка базы данных SQLite
basedir = os.path.abspath(os.path.dirname(__file__))  # Путь к текущей директории
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')  # Путь к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях
app.secret_key = 'supersecretkey' 

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор задачи
    content = db.Column(db.String(200), nullable=False)  # Содержание задачи

    def __repr__(self):
        return f'{self.content}'
    
# Создание базы данных (если она не существует)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()  # Получаем все задачи из базы данных
    return render_template('index.html',title='Home', tasks=tasks) #title dont work

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    existing_task = Task.query.filter_by(content=task).first()
    if existing_task:
            flash('Эта задача уже существует!', 'error')  # Сообщение об ошибке
    else:
        # Создаем новую задачу и добавляем её в базу данных
        new_task = Task(content=task)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    task_content=request.form.get('task')
    existing_task = Task.query.filter_by(content=task_content).first()
    print(existing_task)
    if not task:
        flash("Задача не найдена!", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_content = request.form.get('task')
        if existing_task:
            flash('Эта задача уже существует!', 'error')  # Сообщение об ошибке
        else:
            if new_content:
                task.content = new_content
                db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)



@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)  # Находим задачу по ID
    if task:
        db.session.delete(task)  # Удаляем задачу
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)