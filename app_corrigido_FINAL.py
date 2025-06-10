
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersegredo'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'clientes.db')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        id_cliente = request.form.get('id')
        dados = (
            request.form.get('nome'),
            request.form.get('endereco'),
            request.form.get('bairro'),
            request.form.get('cep'),
            request.form.get('cidade'),
            request.form.get('uf'),
            request.form.get('cpf'),
            request.form.get('rg'),
            request.form.get('orgao_expedidor'),
            request.form.get('telefone'),
            request.form.get('processo'),
            request.form.get('data_inicial'),
            request.form.get('data_final'),
            request.form.get('justica_vara'),
            request.form.get('whatsapp')
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if id_cliente:
            dados += (id_cliente,)
            cursor.execute('''
                UPDATE clientes SET nome=?, endereco=?, bairro=?, cep=?, cidade=?, uf=?, cpf=?, rg=?, 
                orgao_expedidor=?, telefone=?, processo=?, data_inicial=?, data_final=?, justica_vara=?, 
                whatsapp=? WHERE id=?
            ''', dados)
        else:
            cursor.execute('''
                INSERT INTO clientes (nome, endereco, bairro, cep, cidade, uf, cpf, rg, orgao_expedidor,
                                      telefone, processo, data_inicial, data_final, justica_vara, whatsapp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', dados)

        conn.commit()
        conn.close()
        return redirect('/form')

    return render_template('form.html', cliente=None)

@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template('form.html', cliente=cliente)

@app.route('/imprimir/<int:id>', methods=['GET'])
def imprimir(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template('imprimir.html', cliente=cliente)

@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    nome = request.args.get('nome', '')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if nome:
        cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", ('%' + nome + '%',))
    else:
        cursor.execute("SELECT * FROM clientes")

    clientes = cursor.fetchall()
    conn.close()
    return render_template('pesquisar.html', clientes=clientes)

@app.route('/')
def index():
    return redirect('/form')

if __name__ == "__main__":
    app.run(debug=True)
