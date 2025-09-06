import os
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash
from dotenv import load_dotenv
import pandas as pd

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
DB_PATH = os.path.join(os.path.dirname(__file__), 'orders.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client TEXT,
                    date TEXT,
                    status TEXT,
                    manager TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    message TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()


@app.route('/')
@app.route('/orders')
def list_orders():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, client, date, status, manager FROM orders')
    orders = c.fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)


@app.route('/import', methods=['GET', 'POST'])
def import_excel():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('Файл не выбран')
            return redirect(request.url)
        try:
            df = pd.read_excel(file)
            conn = sqlite3.connect(DB_PATH)
            for _, row in df.iterrows():
                conn.execute('INSERT INTO orders (client, date, status, manager) VALUES (?, ?, ?, ?)',
                             (row.get('client'), str(row.get('date')), row.get('status'), row.get('manager')))
            conn.commit()
            conn.close()
            flash('Импорт завершен')
        except Exception as e:
            flash(f'Ошибка импорта: {e}')
        return redirect(url_for('list_orders'))
    return render_template('import.html')


@app.route('/order/new', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        client = request.form['client']
        date = request.form['date']
        status = request.form['status']
        manager = request.form['manager']
        conn = sqlite3.connect(DB_PATH)
        conn.execute('INSERT INTO orders (client, date, status, manager) VALUES (?, ?, ?, ?)',
                     (client, date, status, manager))
        conn.commit()
        conn.close()
        return redirect(url_for('list_orders'))
    return render_template('new_order.html')


@app.route('/order/<int:order_id>/chat', methods=['GET', 'POST'])
def order_chat(order_id):
    conn = sqlite3.connect(DB_PATH)
    if request.method == 'POST':
        message = request.form['message']
        conn.execute('INSERT INTO chat (order_id, message, timestamp) VALUES (?, ?, ?)',
                     (order_id, message, datetime.now().isoformat()))
        conn.commit()
    c = conn.cursor()
    c.execute('SELECT message, timestamp FROM chat WHERE order_id = ? ORDER BY id', (order_id,))
    messages = c.fetchall()
    conn.close()
    return render_template('chat.html', messages=messages, order_id=order_id)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
