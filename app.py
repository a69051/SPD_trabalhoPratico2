from flask import Flask, request, jsonify, render_template_string
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="my-db-instance.cz0iyo8cq59b.us-east-1.rds.amazonaws.com",
        database="initial_db",
        user="postgres",
        password="12345678"
    )
    return conn

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>SPD - Trabalho Prático 2</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
          body {
            background-color: #eef2f3;
            font-family: Arial, sans-serif;
          }
          .navbar {
            background-color: #343a40;
            padding: 1rem;
          }
          .navbar-brand, .nav-link {
            color: #ffffff !important;
          }
          .navbar-nav .nav-item + .nav-item {
            margin-left: 1rem;
          }
          .container {
            margin-top: 50px;
          }
          .jumbotron {
            background-color: #ffffff;
            padding: 2rem 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          }
          .btn-custom {
            background-color: #ff5722;
            color: white;
            border-radius: 30px;
            margin: 10px;
            padding: 10px 20px;
            font-size: 1.2rem;
          }
          .btn-custom:hover {
            background-color: #e64a19;
          }
          .btn-secondary-custom {
            background-color: #9c27b0;
            color: white;
            border-radius: 30px;
            margin: 10px;
            padding: 10px 20px;
            font-size: 1.2rem;
          }
          .btn-secondary-custom:hover {
            background-color: #7b1fa2;
          }
          .btn-success-custom {
            background-color: #4caf50;
            color: white;
            border-radius: 30px;
            margin: 10px;
            padding: 10px 20px;
            font-size: 1.2rem;
          }
          .btn-success-custom:hover {
            background-color: #388e3c;
          }
        </style>
      </head>
      <body>
        <nav class="navbar navbar-expand-lg navbar-dark">
          <a class="navbar-brand" href="#">SPD - Trabalho Prático 2</a>
          <div class="collapse navbar-collapse">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item"><a class="nav-link" href="/produtos_stock">Produtos e Stock</a></li>
              <li class="nav-item"><a class="nav-link" href="/utilizadores">Listar Utilizadores</a></li>
              <li class="nav-item"><a class="nav-link" href="/produtos_validade">Produtos por Data de Validade</a></li>
            </ul>
          </div>
        </nav>
        <div class="container">
          <div class="jumbotron text-center">
            <h1 class="display-4">Bem-vindo à App Flask</h1>
            <p class="lead">Use as rotas para acessar as funcionalidades:</p>
            <hr class="my-4">
            <p class="lead">
              <a class="btn btn-custom" href="/produtos_stock" role="button">Listar Produtos e Stock</a>
              <a class="btn btn-secondary-custom" href="/utilizadores" role="button">Listar Utilizadores</a>
              <a class="btn btn-success-custom" href="/produtos_validade" role="button">Listar Produtos por Data de Validade</a>
            </p>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
      </body>
    </html>
    '''

@app.route('/produtos_stock', methods=['GET'])
def produtos_stock():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT DISTINCT ON (p.nome_produto, u.nome) p.nome_produto, u.nome, p.quantidade 
        FROM produtos p 
        JOIN utilizadores u ON p.id_utilizador = u.id
        ORDER BY p.nome_produto, u.nome;
    ''')
    produtos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string('''
    <!doctype html>
    <html lang="pt">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Produtos e Stock</title>
        <link href="https://stackpath.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
          body {
            background-color: #eef2f3;
            font-family: Arial, sans-serif;
          }
          .container {
            margin-top: 50px;
          }
          .btn-primary-custom {
            background-color: #ff5722;
            color: white;
            border-radius: 30px;
            margin: 10px;
            padding: 10px 20px;
            font-size: 1.2rem;
          }
          .btn-primary-custom:hover {
            background-color: #e64a19;
          }
          .table-striped tbody tr:nth-of-type(odd) {
            background-color: rgba(0, 0, 0, 0.05);
          }
          .table-hover tbody tr:hover {
            color: #212529;
            background-color: rgba(0, 0, 0, 0.075);
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1 class="mb-4 text-center">Produtos e Stock</h1>
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Utilizador</th>
                <th>Quantidade</th>
              </tr>
            </thead>
            <tbody>
              {% for produto in produtos %}
              <tr>
                <td>{{ produto[0] }}</td>
                <td>{{ produto[1] }}</td>
                <td>{{ produto[2] }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
          <div class="text-center">
            <a class="btn btn-primary mt-3" href="/">Voltar</a>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
      </body>
    </html>
    ''', produtos=produtos)

@app.route('/utilizadores', methods=['GET'])
def utilizadores():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, nome, produto_associado 
        FROM utilizadores;
    ''')
    utilizadores = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string('''
    <!doctype html>
    <html lang="pt">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Utilizadores</title>
        <link href="https://stackpath.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
          body {
            background-color: #eef2f3;
            font-family: Arial, sans-serif;
          }
          .container {
            margin-top: 50px;
          }
          .btn-primary-custom {
            background-color: #9c27b0;
            color: white;
            border-radius: 30px;
            margin: 10px;
            padding: 10px 20px;
            font-size: 1.2rem;
          }
          .btn-primary-custom:hover {
            background-color: #7b1fa2;
          }
          .table-striped tbody tr:nth-of-type(odd) {
            background-color: rgba(0, 0, 0, 0.05);
          }
          .table-hover tbody tr:hover {
            color: #212529;
            background-color: rgba(0, 0, 0, 0.075);
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1 class="mb-4 text-center">Utilizadores</h1>
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Produto Associado</th>
              </tr>
            </thead>
            <tbody>
              {% for utilizador in utilizadores %}
              <tr>
                <td>{{ utilizador[0] }}</td>
                <td>{{ utilizador[1] }}</td>
                <td>{{ utilizador[2] }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
          <div class="text-center">
            <a class="btn btn-primary mt-3" href="/">Voltar</a>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
      </body>
    </html>
    ''', utilizadores=utilizadores)

@app.route('/produtos_validade', methods=['GET'])
def produtos_validade():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT DISTINCT ON (nome_produto, data_validade) nome_produto, data_validade, quantidade 
        FROM produtos 
        ORDER BY data_validade;
    ''')
    produtos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string('''
    <!doctype html>
    <html lang="pt">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Produtos por Data de Validade</title>
        <link href="https://stackpath.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
          body {
            background-color: #eef2f3;
            font-family: Arial, sans-serif;
          }
          .container {
            margin-top: 50px;
          }
          .btn-primary-custom {
            background-color: #4caf50;
            color: white;
            border-radius: 30px;
            margin: 10px;
            padding: 10px 20px;
            font-size: 1.2rem;
          }
          .btn-primary-custom:hover {
            background-color: #388e3c;
          }
          .table-striped tbody tr:nth-of-type(odd) {
            background-color: rgba(0, 0, 0, 0.05);
          }
          .table-hover tbody tr:hover {
            color: #212529;
            background-color: rgba(0, 0, 0, 0.075);
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1 class="mb-4 text-center">Produtos por Data de Validade</h1>
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Data de Validade</th>
                <th>Quantidade</th>
              </tr>
            </thead>
            <tbody>
              {% for produto in produtos %}
              <tr>
                <td>{{ produto[0] }}</td>
                <td>{{ produto[1] }}</td>
                <td>{{ produto[2] }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
          <div class="text-center">
            <a class="btn btn-primary mt-3" href="/">Voltar</a>
          </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
      </body>
    </html>
    ''', produtos=produtos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
