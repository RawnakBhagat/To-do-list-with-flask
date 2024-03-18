from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

class Todo(db.Model):
    Sno = db.Column(db.Integer,primary_key=True)
    todo = db.Column(db.String(200),nullable=False)
    des = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default= datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.Sno} {self.todo} '

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        todo_task=request.form['todo']
        desc=request.form['des']
        todo = Todo(todo=todo_task,des=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html",alltodo=alltodo)
@app.route('/show')
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "this is show page"
@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
@app.route('/update/<int:Sno>',methods=['GET','POST'])
def update(Sno):
    if request.method == 'POST':
        todo_task=request.form['todo']
        desc=request.form['des']
        todo = Todo.query.filter_by(Sno=Sno).first()
        todo.todo = todo_task
        todo.des = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(Sno=Sno).first()
    return render_template("update.html",todo=todo)

if __name__ == '__main__':
    app.run(debug=True)   