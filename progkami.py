from peewee import *
import os

arqui = 'base.db'
db = SqliteDatabase(arqui)

if os.path.exists(arqui):
    os.remove(arqui)

class BaseModel(Model):
    class Meta:
        database = db

class Chef_De_Cozinha(BaseModel):
	nome = CharField()
	expediente = CharField()
	salario = FloatField()
    

class Vendedor(BaseModel):
	nome = CharField()
	expediente = CharField()
	salario = FloatField()

class Endereco(BaseModel):
	bairro = CharField()
	rua = CharField()
	numero = IntegerField()

class Estabelecimento(BaseModel):
    nome = CharField()
    vendedor = ForeignKeyField(Vendedor)
    chef = ForeignKeyField(Chef_De_Cozinha)
    endereco = ForeignKeyField(Endereco)

class Fornecedor(BaseModel):
    nome = CharField()
    vendedor = ForeignKeyField(Vendedor)

class Ingrediente(BaseModel):
    nome = CharField()
    quantidade = CharField()

class Receita(BaseModel):
	nome = CharField()
	ingredientes = ManyToManyField(Ingrediente)

class Doce(BaseModel):
    nome = CharField()
    sabor = CharField()
    peso = CharField()
    valor = FloatField()
    quantidade = IntegerField()

class Pedido(BaseModel):
    doces = ManyToManyField(Doce)
    valor_total = FloatField()
    vendedor = ForeignKeyField(Vendedor)

class Cliente(BaseModel):
	nome = CharField()
	pedidos = ManyToManyField(Pedido)

db.connect()
db.create_tables([
Chef_De_Cozinha, 
Vendedor, 
Endereco, 
Estabelecimento, 
Fornecedor,
Cliente.pedidos.get_through_model(),
Pedido.doces.get_through_model(), 
Receita.ingredientes.get_through_model(), 
Ingrediente, 
Receita, 
Doce, 
Pedido, 
Cliente
]) 

joana = Chef_De_Cozinha.create(nome = "Joana", expediente = "Noturno", salario = "R$1200,00")
karina = Vendedor.create(nome = "Karina", expediente ="Integral", salario = "R$1700,00")
end1 = Endereco.create(bairro = "Itoupavazinha",rua = "Rua Sao Miguel", numero = "90")
fava = Estabelecimento.create(nome = "Pe de Fava", vendedor = karina, chef = joana, endereco = end1)
casas_bahia = Fornecedor.create(nome = "Casas Bahia", vendedor = karina)
batata = Ingrediente.create(nome = "Batata", quantidade = "50 unidades")
batata_frita = Receita.create(nome = "Batatas Fritas")
batata_frita.ingredientes.add(batata)
trufa = Doce.create(nome="Trufas",sabor="Brigadeiro",peso = "50 gramas", valor = "R$2,00", quantidade = "100")
pedido1 = Pedido.create (valor_total="R$200,00", vendedor = karina)
pedido1.doces.add(trufa)
lais = Cliente.create (nome="Lais")
lais.pedidos.add(pedido1)



if __name__=="__main__":
    print ("----------------------------------------")
    print (joana.nome,joana.expediente,joana.salario,"= Chef")
    print ("----------------------------------------")
    print (karina.nome,karina.expediente,karina.salario,"= Vendedor")
    print ("----------------------------------------")
    print (end1.bairro,end1.rua,end1.numero,"= Endereco")
    print ("----------------------------------------")
    print (fava.nome,"= Nome",fava.vendedor.nome,"= Vendedor,",fava.chef.nome,"= Chef,",fava.endereco.rua,"= Rua")
    print ("----------------------------------------")
    print(casas_bahia.nome,"= Nome,",casas_bahia.vendedor.nome,"= Vendedor")
    print ("----------------------------------------")
    print(batata.nome,batata.quantidade)
    print ("----------------------------------------")
    a = Receita.select()
    for rec in a:
        texto = str(rec.nome)
        texto += " = Receita      Ingredientes ="
        for ing in rec.ingredientes:
            texto += (" "+str(ing.nome))
        print (texto)
    print ("----------------------------------------")
    print(trufa.nome,trufa.sabor,trufa.peso,trufa.valor,"Quantidade =",trufa.quantidade)
    print ("----------------------------------------")
    a = Pedido.select()
    for pedido in a:
        texto = pedido.valor_total+" = Valor Total, "+str(pedido.vendedor.nome)+" = Vendedor  \n Alimentos pedidos:"
        for doce in pedido.doces:
            texto += " "+str(doce.nome)
        print(texto)
    print ("----------------------------------------")
    a = Cliente.select()
    for cliente in a:
        texto = cliente.nome+" = Nome do cliente \n"
        cont = 1
        for pedido in cliente.pedidos:
            texto += "Valor do pedido "+str(cont)+" = "+str(pedido.valor_total)
        print(texto)
    print ("----------------------------------------")