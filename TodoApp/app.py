from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    todos = c.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['task']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/toggle-done/<int:todo_id>', methods=['POST'])
def toggle_done(todo_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT done FROM todos WHERE id = ?", (todo_id,))
    current_status = c.fetchone()[0]
    new_status = not current_status
    c.execute("UPDATE todos SET done = ? WHERE id = ?", (new_status, todo_id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)