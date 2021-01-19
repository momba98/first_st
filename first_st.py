import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import time

st.set_page_config(page_title='Nome na aba', page_icon="https://static.streamlit.io/examples/cat.jpg", layout='wide', initial_sidebar_state='auto')

st.title("""

HELLO MYFRIEND

""")

agree = st.checkbox('Estou ciente de que nenhuma informação neste aplicativo é recomendação de compra ou venda de ativos na B3.')

if agree:
    st.write('Great!')

st.write("""

## Esse é o título

""")

#displaying um df

df = pd.read_excel('../../../Desktop/Diario/DDE/2021-01-19.xlsx')

df.drop(df.index[80],inplace=True) #excluindo o IBOV
df.drop(df.columns[0], axis=1, inplace=True) #excluindo aquela primeira coluna podre

st.dataframe(df) #poderia ser st.write(df), mesma coisa. .table mostra ela estática

#st.line_chart(df.Abertura)

#rola fazer OHLC, só não vou focar nisso agora. É com o vega, https://docs.streamlit.io/en/stable/api.html

#st.image(Image.open('vai tourinho.jpg'), caption='VAAAI TOURINHO', use_column_width=True) #USANDO O PIL, ABRIR UMA IMG

genre = st.radio("What's your favorite movie genre", ('Comedy', 'Drama', 'Documentary'))

if genre == 'Comedy':
     st.write('You selected comedy.')
else:
     st.write("You didn't select comedy.")


option = st.selectbox(
     'How would you like to be contacted?',
     ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)

age = st.slider('How old are you?', 0, 130, 27) #para transformar em um range, apenas colocar o 3o argumento como lista
st.write("I'm ", age, 'years old')

start_time = st.slider(
     "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)


#title = st.text_input('Movie title', 'Life of Brian')  #or it could be number_input too
#st.write('The current movie title is', title)

#a sidebar dispõe as opções num menu ao lado pra dar mais foco  à informação.
# a key serve pra referenciar esse cara.

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"), key='sfw121'
)

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

st.balloons()

st.error('This is an error')

st.info('This is a purely informational message')

st.success('This is a success message!')

#Inserts a container into your app that can be used to hold a single element.

with st.empty():
     for seconds in range(12):
         st.write(f"⏳ {seconds} seconds have passed")
         time.sleep(1)
     st.write("✔️ 1 minute over!")
