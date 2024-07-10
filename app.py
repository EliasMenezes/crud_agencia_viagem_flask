# Importando os pacotes
from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

# Criando um objeto para
# herdar os métodos do Flask
app = Flask(__name__)

# Configurando a chave secreta para uso da sessão
app.secret_key = 'progSistSenac20244901'

# Configuração do banco de dados
# Verificando a conexão

try:
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='senha',
    database='nome do banco'   
    )
    if conexao.is_connected():
        print('Conexão realizada com sucesso')
except OSError as error:
    print('Erro ao conectar: ', error)

#variavel de execução do scripts em SQL
cursor = conexao.cursor(dictionary=True)

#obs: dictionarry=true é necessario para leitura do resultado da listagem dos registro das tabelas

# Criando as rotas para o carregamento das páginas e 
# realização das operações CRUD

# Evitando o usuario acesse rotas protegidas sem uso de sessão e evitando que paginas seja abertas pelo cache

@app.after_request
# 'res' refere-se aresposta do servidor
def adicionar_cabecalho(res):
    res.headers['cache-control'] = 'no-store, no-cache, must-revalidate, post-check=0 pre-check=0 max-age=0'
    res.headers['pragma']= 'no-cache'
    res.headers['expires'] = '0'
    return res


# 1) Rota para acesso
# da página principal da aplicação
@app.route('/')
def index():

    if 'id' in session:
        return redirect(url_for('home'))

    # Atribuir um retorno para o
    # carregamento da página principal do servidor
    return render_template('login.html')



# 2) Rota para criação de
# registros no banco
@app.route('/criar', methods = ['GET', 'POST'])
def criar():

    #protegendo a rota 
    if 'id' not in session:
        return render_template('login.html')
    
    # Verificar qual método será
    # usado na operação e atribuir
    # variáveis para receber os valores
    # dos campos de texto(inputs)
    if request.method == 'POST':
        
        # Recebendo os valores dos inputs
        # mudar essas informações de acordo com o banco de dados
        Nome_cliente = request.form['Nome_cliente'] 
        email = request.form['email']
        telefone = request.form['telefone']
        end_cliente = request.form['end_cliente']
        cep = request.form['cep']

        # Comando em SQL para criar
        # o cliente
        # mudar essas informações de acordo com o banco de dados
        comando = 'insert into cliente (Nome_cliente, email, telefone, end_cliente, cep) values (%s,%s,%s,%s,%s)'
    
        # Variável que irá receber todos
        # os valores das variáveis anteriores
        # mudar essas informações de acordo com o banco de dados
        valores = (Nome_cliente, email, telefone, end_cliente, cep)
    
        # Executar o comando em SQL
        cursor.execute(comando, valores)
        
        # Confirmar a execução do
        # comando no banco de dados
        conexao.commit()
                
        # Atribuir um retorno podendo
        # ser o redirecionamento para
        # outra página
        return redirect(url_for('listar'))
        #return 'cliente cadastrado com sucesso'
        # OBS: o parâmetro em 'url_for'
        # é a função criada para
        # carregar a rota desejada
    
    # Atribuir um retorno para o
    # carregamento da página de
    # de criação do cliente
    return render_template('criar.html')


# 3) Rota para seleção de
# registros no banco
@app.route('/listar')
def listar():

    #protegendo a rota 
    if 'id' not in session:
        return render_template('login.html')
    
     #Verificando se a sessão existe
    if 'id' in session:
        # Comando em SQl para selecionar
        # os clientes
        comando = 'select * from cliente'
        
        # Executar o comando em SQL
        cursor.execute(comando)
        # Variável que irá receber
        # o resultado do comando
        clientes = cursor.fetchall()
        
        # retornar o resultado
        # carregando em outra página e usando um apelido depois do nome da pagina a ser carregada
        return render_template('listar.html', clientes = clientes)

        #ESCLARECENDO:('listar.html', clientes = cliente) 
        # a primeira variavel 'clientes' recebe a execução do script em sql
        # 0 segunda variavel 'clientes' sera o apelido dado a pagina 'lista.html'
       
       
    else:
        return render_template('login.html')
    



# 4) Rota para atualização de
# registros no banco
@app.route('/editar/<int:id_cliente>', methods = ['GET', 'POST'])
#declarar a função com "Id" como parametro
def editar(id_cliente):

    #protegendo a rota 
    if 'id' not in session:
        return render_template('login.html')

    # ====== SEGUNDO PASSO ==========
    # Comandos para editar 
    # somente um cliente pelo id

    if request.method == 'POST':
        
        # Recebendo os valores dos inputs
        # mudar essas informações de acordo com o banco de dados
        Nome_cliente = request.form['Nome_cliente']
        email = request.form['email']
        telefone = request.form['telefone']
        end_cliente = request.form['end_cliente']
        cep = request.form['cep']
        
        # Comando em SQl para editar
        # os clientes
        # mudar essas informações de acordo com o banco de dados
        comando = 'update cliente set Nome_cliente= %s, email= %s, telefone= %s, end_cliente= %s, cep= %s where id_cliente= %s '
        
        # Variável que irá receber todos
        # os valores das variáveis anteriores
        # mudar essas informações de acordo com o banco de dados
        valores = (Nome_cliente, email, telefone, end_cliente, cep, id_cliente)
        
        # Executar o comando em SQL
        cursor.execute(comando, valores)
        
        # Confirmar a execução do
        # comando no banco de dados
        conexao.commit()
        # Atribuir um retorno podendo
        # ser o redirecionamento para
        # outra página o parametro de url_for() é o nome da função referente a rota
        return redirect(url_for('listar'))
        
    # ====== PRIMEIRO PASSO ==========
    # Comandos para selecionar
    # somente um cliente pelo id
    
    comando = 'select * from cliente where id_cliente = %s'
    
    # Variável que irá receber 
    # o valor do id do cliente
    valor = (id_cliente, ) 
    
    # Executar o comando em SQL
    cursor.execute(comando, valor)
    #variavel que ira recebe o resultado do comando
    cliente = cursor.fetchone()
    
    # retornar o resultado
    # carregando em outra página
    
    return render_template('editar.html', cliente = cliente)

#ESCLARECENDO:('listar.html', clientes = cliente) 
    # a primeira variavel 'clientes' recebe a execução do script em sql
    # 0 segunda variavel 'clientes' sera o apelido dado a pagina 'editar.html'


# 5) Rota para exclusão de
# registros no banco
@app.route('/excluir/<int:id_cliente>')
#declarar função com id da 
def excluir(id_cliente):

    #protegendo a rota 
    if 'id' not in session:
        return render_template('login.html')
    
    # Comando em SQl para excluir
    # a viagem
    comando = 'delete from cliente where id_cliente= %s'    
    
    # Variável que irá receber 
    # o valor do id 
    valor = (id_cliente, )    
    
    # Executar o comando em SQL
    cursor.execute(comando, valor)
    # Confirmar a execução do
    # comando no banco de dados
    conexao.commit()
    # Atribuir um retorno podendo
    # ser o redirecionamento para
    # outra página
    return redirect(url_for('listar'))

#6)Rota para autenticar o usuario e acessar o sistema
@app.route('/login', methods = ['GET', 'POST'])
# função de execução do escript que ira selecionar o usuario na tabela
def login():
    
    if request.method == 'POST':
# Recebendo o dos valores dos imputs
        email = request.form['email']
        senha = request.form['senha']
        #comando em SQL para selecionar o usuario
    comando = 'select id_usuario, email, senha from usuario where email = %s and senha = %s'

# variavel que ira receber todos os valores das variaveis anteriores
    valores = (email, senha)

# Executar o comando em SQL
    cursor.execute(comando, valores)

# Variavel que ira receber o resultado do comando
    usuario = cursor.fetchone()
    
# Verificando se usuario cadastrado esta no BD

    if usuario:
        # Criando a sessão do usuario apelido atribuido:'id'
        session ['id'] = usuario['id_usuario']
        #direcionar o usuario para pagina index.html se existir usuario
        return redirect(url_for('home'))
    
    else: 
        #criando uma mensagem caso o email ou senha estejam incorretos
        mensagem = "E-mail ou senha incorretos. Tentem novamente!!"
        # renderiza a pagina de login se o usuario nao exitir ou se houver erro com email ou senha incorretos
        return render_template('login.html', mensagem = mensagem) 

    #É preciso dar um retorno para a função nesse caso pose-se usar a pagina de login.html
#return render_template('login.hmtl')

#7) Rota de acesso a pagina index.html e protegendo a rota com sessão
@app.route('/index', )
def home():
    #Verificando se a sessão existe
    if 'id' in session:
        return render_template('index.html')

    else:
        return render_template('login.html')


#8) Rota de loggof do sistema
@app.route('/sair')
def sair():
    # Destruindo a sessão
    session.clear()
    #Nome da função que renderiza a pagina "login.html' no valor 'url_for()'
    return redirect(url_for('index'))


# Criação do método de execução
# do servidor local
if __name__ == '__main__':
    app.run(debug=True)