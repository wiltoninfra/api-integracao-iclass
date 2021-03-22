from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Configuração com banco de dados Mysql
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'apidb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Inicia instância MYSQL
mysql = MySQL(app)

# Rota para Inicio
@app.route('/')
def index():
    return render_template('home.html')

# Rota para listar aulas cadastradas
@app.route('/classes')
def classes():
    # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    # Query para buscar aulas no banco de dados
    result = cur.execute("SELECT * FROM classes")
    classes = cur.fetchall()
    if result > 0:
        return render_template('classes.html', classes=classes)
    else:
        msg = 'Nenhuma aula cadastrada'
        return render_template('classes.html', msg=msg)
    # Fecha conexão com banco de dados
    cur.close()

# Mostrar informações sobre uma aula cadastrada
@app.route('/classe/<string:id>/')
def classe(id):
    # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    # Query para buscar aulas no banco de dados
    result = cur.execute("SELECT * FROM classes WHERE id = %s", [id])
    classe = cur.fetchone()
    return render_template('classe.html', classe=classe)

# Rota para listat clientes cadastrados
@app.route('/clients')
def clients():
    # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    # Query para buscar clientes no banco de dados
    result = cur.execute("SELECT * FROM clients")
    clients = cur.fetchall()
    if result > 0:
        return render_template('clients.html', clients=clients)
    else:
        msg = 'Nenhum cliente cadastrado'
        return render_template('clients.html', msg=msg)
    # Fecha conexão com banco de dados
    cur.close()

# Rota para visualizar um cliente por vez
@app.route('/client/<string:id>/')
def client(id):
    # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    # Query para buscar cliente especifico no banco de dados 
    result = cur.execute("SELECT * FROM clients WHERE id = %s", [id])
    client = cur.fetchone()
    return render_template('client.html', client=client)

# Class para registro de usuários na área ADM
class RegisterForm(Form):
    """
    Classe registro de usuários novos.
    """    
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='As senhas não coincidem')
    ])
    confirm = PasswordField('Confirme sua senha')

# Rota para registrar um novo administrador do I-Class
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
       # Cria conexão com Mysql (Banco de Dados)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)',
                    (name, email, username, password))
        # Realiza commit no banco de dados
        mysql.connection.commit()
        # Fecha conexão com banco de dados
        cur.close()
        flash('Você agora está registrado e pode fazer login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Rota para realizar login na área ADM
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Pega informações passadas no formulário de login
        username = request.form['username']
        password_candidate = request.form['password']
       # Cria conexão com Mysql (Banco de Dados)
        cur = mysql.connection.cursor()
        # Busca usuário por username
        result = cur.execute(
            'SELECT * FROM users WHERE username = %s', [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('Agora você está logado', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Login inválido'
                return render_template('login.html', error=error)
                # Fecha conexão com banco de dados
            cur.close()
        else:
            error = 'Nome de usuário não encontrado'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Verifica se usuário esta logado
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Não autorizado, faça o login para acessar', 'danger')
            return redirect(url_for('login'))
    return wrap

# Reliza ação de sair do sistema
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Você está desconectado agora', 'success')
    return redirect(url_for('login'))

# Rota para exibir dasboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
   # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM classes")
    classes = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', classes=classes)
    else:
        msg = 'Nenhuma aula cadastrada'
        return render_template('dashboard.html', msg=msg)
        # Fecha conexão com banco de dados
    cur.close()

# Class para cadastro de novos clientes (Alunos/Professores)
class RegisterClient(Form):
    """
    Classe cadastro de novos clientes (Alunos/Professores).
    """       
    name = StringField('Nome completo', [validators.Length(min=1, max=50)])
    email = StringField('E-mail', [validators.Length(min=6, max=50)])    
    mobile = StringField('Celular', [validators.Length(min=6, max=50)])
    cpf = StringField('Nº documento', [validators.Length(min=6, max=50)])
    dtbirth = StringField('Data de nascimento', [validators.Length(min=6, max=50)])   
    zipcode = StringField('Cep', [validators.Length(min=6, max=50)]) 
    street = StringField('Rua', [validators.Length(min=6, max=50)])  
    city = StringField('Cidade', [validators.Length(min=6, max=50)])           
    ppay = StringField('Preferência de pagamento', [validators.Length(min=6, max=50)])  
    typeclient = StringField('Tipo do cliente', [validators.Length(min=6, max=50)]) 
    username = StringField('Usuário', [validators.Length(min=4, max=25)])   
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='As senhas não coincidem')
    ])
    confirm = PasswordField('Confirme sua senha')

# Rota para cadastro de novo aluno/professor
@app.route('/add_client', methods=['GET', 'POST'])
@is_logged_in
def add_clients():
    form = RegisterClient(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        mobile = form.mobile.data
        cpf = form.cpf.data                
        dtbirth = form.dtbirth.data
        zipcode = form.zipcode.data
        street = form.street.data
        city = form.city.data    
        ppay = form.ppay.data             
        typeclient = form.typeclient.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
       # Cria conexão com Mysql (Banco de Dados)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clients(name, email, mobile, cpf, dtbirth, zipcode, street, city, ppay, typeclient, username, password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (name, email, mobile, cpf, dtbirth, zipcode, street, city, ppay, typeclient, username, password))
        mysql.connection.commit()
        # Fecha conexão com banco de dados
        cur.close()
        flash('Agora você é cliente e pode fazer login', 'success')
        return redirect(url_for('home'))
    return render_template('add_client.html', form=form)

# Classe para cadastro de novas aulas
class ClasseForm(Form):
    """
    Classe cadastro de novas aulas.
    """       
    title = StringField('Título', [validators.Length(min=6, max=50)])
    description = TextAreaField('Descrição', [validators.Length(min=30)])
    teacher = StringField('Nome Professor', [validators.Length(min=6, max=50)])
    time = StringField('Tempo da Aula', [validators.Length(min=1, max=10)])
    price = StringField('Preço hora', [validators.Length(min=1, max=10)])

# Rota para adicionar nova aula manualmente
@app.route('/add_classe', methods=['GET', 'POST'])
def add_classe():
    form = ClasseForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        teacher = form.teacher.data        
        time = form.time.data
        price = form.price.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO classes(title, description, teacher, time, price) VALUES(%s, %s, %s, %s, %s)",
                    (title, description, teacher, time, price))
        mysql.connection.commit()
        # Fecha conexão com banco de dados
        cur.close()
        flash('Nova aula criada', 'Success')
        return redirect(url_for('dashboard'))
    return render_template('add_classe.html', form=form)

# Editar uma aula cadastrada
@app.route('/edit_classe/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_classe(id):
   # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM classes WHERE id = %s', [id])
    classe = cur.fetchone()
    form = ClasseForm(request.form)
    form.title.data = classe['title']
    form.description.data = classe['description']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        description = request.form['description']
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE classes SET title=%s, description=%s WHERE id=%s", (title, description, id))
        mysql.connection.commit()
        # Fecha conexão com banco de dados
        cur.close()
        flash('Aula atualizada', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_classe.html', form=form)

# Rota para deletar aula cadastrada
@app.route('/delete_classe/<string:id>', methods=['POST'])
@is_logged_in
def delete_classe(id):
   # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM classes WHERE id = %s', [id])
    mysql.connection.commit()
    # Fecha conexão com banco de dados
    cur.close()
    flash('Aula removida', 'success')
    return redirect(url_for('dashboard'))

# Rota para editar cliente
@app.route('/edit_client/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_client(id):
   # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM clients WHERE id = %s', [id])
    client = cur.fetchone()
    form = ClasseForm(request.form)
    form.name.data = classe['name']
    form.email.data = classe['email']
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE clients SET name=%s, email=%s WHERE id=%s", (name, email, id))
        mysql.connection.commit()
        # Fecha conexão com banco de dados
        cur.close()
        flash('Aula atualizada', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_client.html', form=form)

# Rota para remover cliente cadastrado
@app.route('/delete_client/<string:id>', methods=['POST'])
@is_logged_in
def delete_client(id):
   # Cria conexão com Mysql (Banco de Dados)
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clients WHERE id = %s', [id])
    mysql.connection.commit()
    # Fecha conexão com banco de dados
    cur.close()
    flash('Cliente Removido', 'success')
    return redirect(url_for('clients'))

# Inicia Server Python Flask API
if __name__ == '__main__':
    app.secret_key = 'Iclass2021'
    app.run(host='0.0.0.0', port=5000, debug=True)
