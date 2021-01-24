import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta
import time
import os
import xlrd

#falta construir o ranking e tentar otimizar essa exibição dos floats. no futuro, automatizar push pro github junto com o DDE pra não precisar ficar fazendo isso

st.set_page_config(page_title='Nome na aba', page_icon="https://static.streamlit.io/examples/cat.jpg", layout='centered', initial_sidebar_state='auto')

st.title("""

BOLSISTAS DATA ANALYSIS

""")

agree = st.checkbox('Estou ciente de que nenhuma informação neste aplicativo é recomendação de compra ou venda de ativos na B3.')

if agree:
    st.write('Great!')

st.write("""

    ## VAMOS ESTUDAR OS VOLUMES:
    ### QUANTIDADE, VALOR E NEGÓCIOS


""")

displaying = st.radio(
    label = "Como você gostaria de visualizar as informações?",
    options = ('Diário', 'Range Diário'),
    index=1
    )

#displaying um df
def show_daily():

    armz = {}

    for file in os.listdir("planilhas_diarias"):
        if file.endswith(".xlsx"):
            df = pd.read_excel(f'planilhas_diarias/{file}')
            df.drop(df.index[80],inplace=True) #excluindo o IBOV

            df = df[['Asset','Nome do Ativo','Variação','Negócios', 'Quantidade', 'Volume']]

            armz[file[:-5]] = df

    del armz['fonte_DDE']

    show_df = st.selectbox(
         'Qual dia você gostaria de visualizar as informações?',
         list(armz))

    st.dataframe(armz[show_df]) #poderia ser st.write(df), mesma coisa. .table mostra ela estática

def show_range_daily():

    displaying2 = st.radio(
        label = "Como você gostaria de analisar as informações?",
        options = ('Em soma', 'Em média'),
        index=0
        )

    armz = {}

    for file in os.listdir("planilhas_diarias"):
        if file.endswith(".xlsx"):
            df = pd.read_excel(f'planilhas_diarias/{file}')
            df.drop(df.index[80],inplace=True) #excluindo o IBOV
            df.drop(df.index[22],inplace=True) #excluindo o BOVA11

            df = df[['Asset','Variação','Negócios', 'Quantidade', 'Volume']]

            armz[file[:-5]] = df

    del armz['fonte_DDE']

    Y_i=int(list(armz)[0][:4])
    M_i=int(list(armz)[0][5:7])
    D_i=int(list(armz)[0][8:10])

    data_i=datetime(Y_i,M_i,D_i)

    Y_f=int(list(armz)[-1][:4])
    M_f=int(list(armz)[-1][5:7])
    D_f=int(list(armz)[-1][8:10])

    data_f=datetime(Y_f,M_f,D_f)

    show_df = st.slider(
        label='Qual range você gostaria de visualizar?',
        min_value=data_i,
        max_value=data_f,
        value=[data_i,data_f])
        #format="YY-MM-DD")

    qtd_dias = str(show_df[1]-show_df[0] + timedelta(days=1)).split(',')[0]

    st.write('We are talking about', qtd_dias)

    day_low = str((show_df)[0])[:-9]
    day_high = str((show_df)[1])[:-9]

    lista_inicio_fim_iteracao=[]

    for chave,valor in enumerate(armz.keys()):
        if valor == day_low:
            lista_inicio_fim_iteracao.append(chave)

        if valor == day_high:
            lista_inicio_fim_iteracao.append(chave)

            #duplo é necessário pra lista ter sempre o mesmo tamanho

    dfs = armz[day_low].copy()

    for somador in range(lista_inicio_fim_iteracao[0]+1,lista_inicio_fim_iteracao[1]+1):
        dfs += armz[list(armz)[somador]]

    if displaying2 == 'Em média':

        if qtd_dias[-1] == 's':
            dias = int(qtd_dias[:-5])
        else:
            dias = 1

        dfs[['Variação','Negócios', 'Quantidade', 'Volume']] = round(dfs[['Variação','Negócios', 'Quantidade', 'Volume']]/dias,2) #retirando o ' days'

        #dfs[['Volume']] = dfs[['Volume']].astype(float)
        dfs[['Negócios', 'Quantidade']] = dfs[['Negócios', 'Quantidade']].astype(int)

    dfs[['Asset']] = armz[day_low][['Asset']]

    st.write(dfs) #poderia ser st.write(df), mesma coisa. .table mostra ela estática



if displaying == 'Diário':
     show_daily()
elif displaying == 'Range Diário':
     show_range_daily()

#st.line_chart(df.Abertura)

#rola fazer OHLC, só não vou focar nisso agora. É com o vega, https://docs.streamlit.io/en/stable/api.html

st.image(Image.open('vaito.jpg'), caption='VAAAI TOURINHO', use_column_width=True) #USANDO O PIL, ABRIR UMA IMG

age = st.slider('How old are you?', 0, 130, 27) #para transformar em um range, apenas colocar o 3o argumento como lista
st.write("I'm ", age, 'years old')


#title = st.text_input('Movie title', 'Life of Brian')  #or it could be number_input too
#st.write('The current movie title is', title)

#a sidebar dispõe as opções num menu ao lado pra dar mais foco  à informação.
# a key serve pra referenciar esse cara.

#add_selectbox = st.sidebar.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone"), key='sfw121'
#)


#beta_columns organiza o app em forma de colunas.
# se for passado só um int, é o número de colunas que vai ter, todas iguais.
# se for passado uma lista, o numero de colunas é o len e a width é proporcional ao int da posição.

col1, col2, col3 = st.beta_columns([5,2,1])

#pode ser com o nome da coluna.a função
#ou pode ser com o with.

col1.header("A cat")
col1.image("https://static.streamlit.io/examples/cat.jpg", use_column_width=True)

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", use_column_width=True)

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", use_column_width=True)


#uma forma de esconder as informações

st.line_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.beta_expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
     st.image("https://static.streamlit.io/examples/dice.jpg")

#st.balloons()

#st.error('This is an error')

#st.info('This is a purely informational message')

#st.success('This is a success message!')

#Inserts a container into your app that can be used to hold a single element.

with st.empty():
     for seconds in range(12):
         st.write(f"⏳ {seconds} seconds have passed")
         time.sleep(1)
     st.write("✔️ 1 minute over!")
