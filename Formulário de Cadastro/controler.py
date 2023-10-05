from PyQt6 import uic, QtWidgets
import pymysql.connections
numero_id=0

banco = pymysql.connections.Connection(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro275"
)

def funcao_principal():
    codigo = produtos.codigo.text()
    descricao = produtos.descricao.text()
    preco = produtos.preco.text()
    print("Identificacao:", codigo)
    print("Nome:", descricao)
    print("Valor:", preco)

    if produtos.limpeza.isChecked():
        print("Categoria Limpeza")
        categoria="Limpeza"
    elif produtos.perecivel.isChecked():
        print("Categoria Perecível")
        categoria="Perecível"
    elif produtos.bebida.isChecked():
        print("Categoria Bebidas")
        categoria="Bebidas"
    
    #Inserindo dados no banco de dados
    cursor = banco.cursor()
    sql = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(codigo),str(descricao), str(preco), categoria)
    cursor.execute(sql, dados)
    banco.commit()


def listar():
    listarProdutos.show()
    
    #Mostrar os dados do banco de dados
    cursor = banco.cursor()
    sql = "SELECT * FROM produtos"
    cursor.execute(sql)
    dados_recebido = cursor.fetchall()
    listarProdutos.tableWidget.setRowCount(len(dados_recebido))
    listarProdutos.tableWidget.setColumnCount(5)

    for linha in range(0,len(dados_recebido)):
        for coluna in range (0,5):
            listarProdutos.tableWidget.setItem(linha,coluna,QtWidgets.QTableWidgetItem(str(dados_recebido[linha][coluna])))

def excluir_dados():
    linha=listarProdutos.tableWidget.currentRow()
    listarProdutos.tableWidget.removeRow(linha)
    cursor = banco.cursor()
    cursor.execute("SELECT id_prod FROM produtos")
    dados_recebidos = cursor.fetchall()
    valor_id=dados_recebidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id_prod="+str
    (valor_id))
    banco.commit()

app = QtWidgets.QApplication([])
produtos = uic.loadUi("cadastro_produtos.ui")
listarProdutos = uic.loadUi("listar_dados.ui")
produtos.cadastrar.clicked.connect(funcao_principal)
produtos.listar.clicked.connect(listar)
listarProdutos.deletar.clicked.connect(excluir_dados)

produtos.show()
app.exec()

