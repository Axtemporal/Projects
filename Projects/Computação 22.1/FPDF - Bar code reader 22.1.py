# Instalando o pacote FPDF2, ele é o pacote que possiblita a criação e edição do PDF

x = input('Lojista, qual será o produto escolhido?\Temos disponível em nossa loja os seguintes produtos: \n Biscoito maltado da vaquinha, \n biscoito maizena piraquê, \n biscoito de polvilho qualitá, \n batata palha yoki, \n stiksy Elma Chips, \n Torrada Wickbold, \n Vela jardim siciliano phebo, \n livro microeconomia hal varian. \n Insira aqui:   ')


if x == 'biscoito maltado da vaquinha':
  y = '7896024760319'

if x == 'biscoito maizena piraquê':
  y = '7896024722324'

if x == 'biscoito de polvilho':
  y = '7895000318261'

if x == 'batata palha yoki':
  y = '7891095031122'

if x == 'sticksy Elma Chips':
  y = '7892840818029'

if x == 'torrada wickbold':
  y = '7896066304359'

if x == 'vela jardim siciliano phebo':
  y = '7896512953094'

if x == 'livro microeconomia hal varian':
  y = '9788535230185'


pip install fpdf2


#Importando o FPDF


from fpdf import FPDF 

#Definindo a classe

class PDF(FPDF):
     pass

# nada ocorre

#Definindo o formato do pdf, o padrão é A4 mas é importante deixar esse parâmetro claro na hora de fazeer o código para os leitores

pdf = PDF(format='A4')

#Criando a página. A partir dessa linha tudo vaie star dentro dessa folha até que eu insira esse comando novamente, o que gerará mais uma página no arquivo PDF

pdf.add_page()

# Definindo as margens:


pdf.set_margins(0, 0, 0)


# Definindo a fonte e tamanho da letra

pdf.set_font('helvetica', size=30)

# Criando célula de texto

pdf.cell(200, 10, txt = "Nota Fiscal do Mercadinho do Walter", align='C')

#Fonte e tamanho para a próxima celula de texto

pdf.set_font('helvetica', size=15)

#Criando outra célula:

pdf.cell(200, 10, txt = "Aqui trabalhamos com só um produto por compra!", align='C')

#Testando a Utilização de uma fonte externa ao FPDF


pip install python-barcode 
pip install pillow

from barcode import EAN13 
from barcode.writer import ImageWriter 
number = y
  
my_code = EAN13(number, writer=ImageWriter()) 
my_code.save("new_code1")


#Adicionando o código de barras do produto selecionado:

pdf.image('/content/new_code1.png', x = 85, y = 32.5, w = 40, h = 0, type = '', link = '')


#Output termina o documento 

pdf.output('testando.pdf','F')










