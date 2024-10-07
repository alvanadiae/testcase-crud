from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Setup database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# Route for showing all items (Read)
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Route for adding a new item (Create)
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Route for editing an item (Update)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cursor.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM items WHERE id = ?', (id,))
    item = cursor.fetchone()
    conn.close()
    return render_template('edit.html', item=item)

# Route for deleting an item (Delete)
@app.route('/delete/<int:id>')
def delete_item(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)