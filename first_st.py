import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta
import time
import os
import xlrd
import numpy as np

#incluir gráfico: selecione o ativo e veja seu desempenho no ranking ao longo do tempo
#incluir customização: adicionar ou não o ranking definido por mim, que vai comparar
#o desemepnho do ativo com o desempenho do ibov naquele ano. começar em 2015 e ir até 2020.
#TROCAR O NOME DO REPO

st.set_page_config(page_title='BDA - Volumes', page_icon="https://static.streamlit.io/examples/cat.jpg", layout='centered', initial_sidebar_state='auto')

st.title("""

BOLSISTAS DATA ANALYSIS

""")

st.write("""
    ## VAMOS ESTUDAR OS VOLUMES: QUANTIDADE, VALOR E NEGÓCIOS
""")

st.write(' ')

with st.beta_expander('MOTIVAÇÃO/INTRODUÇÃO'):

    st.write(
    """
    Este webapp tem como objetivo aglomerar as informações que os volumes dos ativos da B3 nos fornecem.
    Os três tipos de volume analisados são: **Volume de Quantidade** (quantas ações são negociadas),
    **Volume de Negócios** (quantas vezes compradores e vendedores entraram em consenso) e **Volume de Valor** (qual o montante as negociações geraram, em R$).
    Neste webapp, constroi-se um Ranking das principais ações da B3 atribuindo pesos aos diferentes volumes e somando-os.
    """)

    st.write("""
    A análise desses dados se faz necessária uma vez que uma informação complementa a outra. Como por exemplo, podemos citar dois papéis (até então) muito distintos:
    VALE3 e OIBR3. VALE3 tem o preço nominal estabelecido por volta dos R$ 100, enquanto OIBR3 por volta dos R$ 2. Obviamente, o montante que as negociações em VALE3 geram
    (ou seja, o Volume de Valor) será imensamente maior que o de OIBR3, mesmo que negocie muito menos. Do outro lado da moeda, podemos imaginar que
    o Volume de Quantidade em OIBR3 será muito maior que em VALE3, uma vez que 1 ação de uma empresa representa ~50 ações de outra.
    """)

    st.write("""
    Por meio da utilização deste webapp, o usuário conseguirá visualizar os 3 volumes da maneira que quiser. Consequentemente, não será mais tão enganado
    pelos valores dos volumes analisados de forma individual.
    """)


st.write(' ')
st.write(' ')
st.write(' ')


agree = st.checkbox('Estou ciente de que nenhuma informação neste aplicativo é recomendação de compra ou venda de ativos na B3.')

if agree:

    st.write(' ')

    st.write('### 1. Escolha o tipo de análise a ser feita:')

    st.write(' ')

    displaying = st.radio(
        label = "1.1 Como você gostaria de visualizar as informações?",
        options = ('Diário (apenas um dia)', 'Range Diário (vários dias)'),
        index=1
        )

    #displaying um df
    def show_daily():

        global df_show_daily

        armz = {} #armazenar os files encontrados

        for file in os.listdir("planilhas_diarias"):
            if file.endswith(".xlsx"):
                df = pd.read_excel(f'planilhas_diarias/{file}')
                df.drop(df.index[81],inplace=True) #excluindo o IBOV
                df.drop(df.index[22],inplace=True) #excluindo o BOVA11

                df = df[['Asset','Variação','Negócios', 'Quantidade', 'Volume']]

                armz[file[:-5]] = df

        del armz['fonte_DDE']

        st.write(' ')

        lista_de_planilhas = np.sort(list(armz))

        lista_de_datas = [datetime.strptime(a, "%Y-%m-%d").date() for a in lista_de_planilhas]

        lista_de_datas2 = [a.strftime('%d/%m/%Y') for a in lista_de_datas]

        show_df = st.selectbox(
             '1.2 Qual dia você gostaria de visualizar as informações?',
             lista_de_datas2)

        df_show_daily = armz[datetime.strptime(show_df, '%d/%m/%Y').date().strftime("%Y-%m-%d")] #que putaria... kkkkk

        return 'show_daily'


        #st.dataframe(armz[show_df]) #poderia ser st.write(df), mesma coisa. .table mostra ela estática

    def show_range_daily():

        global df_show_range, status, inicio, final, pregoes

        armz = {}

        for file in os.listdir("planilhas_diarias"):
            if file.endswith(".xlsx"):
                df = pd.read_excel(f'planilhas_diarias/{file}')
                df.drop(df.index[80],inplace=True) #excluindo o IBOV
                df.drop(df.index[22],inplace=True) #excluindo o BOVA11

                df = df[['Asset','Variação','Negócios', 'Quantidade', 'Volume']]

                armz[file[:-5]] = df

        del armz['fonte_DDE']

        lista_de_planilhas = np.sort(list(armz))

        lista_de_datas = [datetime.strptime(a, "%Y-%m-%d").date() for a in lista_de_planilhas]

        st.write(' ')

        show_df = st.slider(
        label='1.2 Qual range de data você gostaria de visualizar?',
        min_value=lista_de_datas[0],
        max_value=lista_de_datas[-1],
        value=[lista_de_datas[0],lista_de_datas[-1]],
        format="DD/MM/YYYY")

        qtd_dias = str(show_df[1]-show_df[0] + timedelta(days=1)).split(',')[0]

        if qtd_dias[-4:] == 'days':
            qtd_dias_escrito = qtd_dias[:2] + ' dias corridos'
        else:
            qtd_dias_escrito = qtd_dias[:2] + ' dia corrido'

        st.write(' ')

        pregoes = []

        for file in os.listdir("planilhas_diarias"):
            if file.endswith(".xlsx"):
                if file[0] != 'f':
                    Y_=int(file[:4])
                    M_=int(file[5:7])
                    D_=int(file[8:10])
                    data_=datetime(Y_,M_,D_)
                    if np.logical_and(data_.date()>=show_df[0],data_.date()<=show_df[1]):
                        pregoes.append(file)

        inicio = show_df[0].strftime('%d/%m/%Y')

        final = show_df[1].strftime('%d/%m/%Y')

        st.write(f'*O período selecionado é de {inicio} até {final}. Estamos falando de {qtd_dias_escrito}, quais ocorreram {len(pregoes)} pregões.*')

        with st.beta_expander('MAIORES CUSTOMIZAÇÕES'):

            displaying2 = st.checkbox(
                label = "1.3 Gostaria de visualizar os dados em forma de soma (média por default).")

            displaying3 = st.checkbox(
                label = "1.4 Gostaria de visualizar apenas alguns ativos.")

            if displaying3:
                lista_personal = st.text_input(label='Liste os ativos exatamente como o exemplo demonstra (letra maíuscula e espaço depois de vírgula):', value='VALE3, ABEV3, MRFG3, WEGE3')

                lista_personal = lista_personal.split(', ')

            displaying4 = st.checkbox(
                label = "1.5 Gostaria de alterar os pesos dos valores que constroem o Ranking.")

            if displaying4:

                st.write("O Ranking é construído dando pesos iguais aos 3 tipos de volume (Quantidade, Negócios e Valor).")
                st.write("Em outras palavras, normalizamos todos os valores de acordo com o máximo de cada coluna e então somamos tudo. Quanto mais próximo do valor máximo, maior é o Ranking.")
                st.write("Por padrão, cada tipo de volume recebe o peso de 0,33.")
                st.write("Caso você ache que um valor é mais importante do que outro, altere como preferir nos campos abaixo. **Lembre-se, o valor deve ser próximo de 1!**")
                peso_quantidade = st.number_input(label='Peso para Quantidade', value=0.33)
                peso_negocios = st.number_input(label='Peso para Negócios', value=0.33)
                peso_valor = st.number_input(label='Peso para Valor', value=0.33)


                if (peso_quantidade + peso_negocios + peso_valor < 0.98) | (peso_quantidade + peso_negocios + peso_valor > 1.02):
                    st.error('O valor está divergindo consideravelmente de 1. Algum erro pode acontecer.')

                else:
                    st.success('Tudo certo com o valor dos pesos!')

        dfs = armz[pregoes[0][:10]].copy()

        if len(pregoes)>1:
            for somador in pregoes[1:]:
                dfs += armz[somador[:10]]

        else:
            pass

        status = 'SOMADA'

        if not displaying2:

            status = 'MÉDIA'

            dias = len(pregoes)

            dfs['Variação'] = round(dfs['Variação']/dias,3)
            dfs[['Negócios', 'Quantidade', 'Volume']] = round(dfs[['Negócios', 'Quantidade', 'Volume']]/dias,0)

        dfs['Asset'] = armz[pregoes[0][:10]]['Asset']

        dfs['Negócios_Param'] = dfs['Negócios']/max(dfs['Negócios'])
        dfs['Quantidade_Param'] = dfs['Quantidade']/max(dfs['Quantidade'])
        dfs['Volume_Param'] = dfs['Volume']/max(dfs['Volume'])

        if displaying4:
            dfs['Ranking'] = peso_negocios*dfs['Negócios_Param'] + peso_quantidade*dfs['Quantidade_Param'] + peso_valor*dfs['Volume_Param']

        else:
            dfs['Ranking'] = (1/3)*dfs['Negócios_Param'] + (1/3)*dfs['Quantidade_Param'] + (1/3)*dfs['Volume_Param']

        dfs['Ranking'] = 100*dfs['Ranking']/max(dfs['Ranking'])

        dfs = dfs.sort_values('Ranking', ascending=False)

        dfs['Ranking_Param'] = np.arange(1,len(dfs['Ranking'])+1)

        dfs.set_index('Ranking_Param', inplace=True)

        del dfs['Negócios_Param'], dfs['Quantidade_Param'], dfs['Volume_Param']#, dfs['Ranking']

        if displaying3:
            dfs= dfs[dfs['Asset'].isin(lista_personal)]

        #dfs.columns(['Asset', 'Variação (%)', 'Vol. Negócios (trades)', 'Vol. Quantidade (ações)', 'Vol. Valor (R$)'])

        dfs = dfs.rename({'Variação': 'Variação (%)', 'Negócios': 'Negócios', 'Quantidade':'Quantidade', 'Volume':'Valor (R$)'}, axis='columns')

        df_show_range = dfs

        return 'show_range'

        #st.write(dfs) #poderia ser st.write(df), mesma coisa. .table mostra ela estática

    if displaying == 'Diário (apenas um dia)':
         action = show_daily()

    elif displaying == 'Range Diário (vários dias)':
         action = show_range_daily()

    st.write(' ')
    st.write(' ')
    st.write(' ')

    st.write('### 2. Visualize seus dados e tire suas conclusões clicando no botão!')

    if action == 'show_daily':
        st.write('Clicando no botão, uma tabela será mostrada com todos os ativos mais negociados da B3 no dia selecionado. Você pode alterar a ordem das linhas clicando no nome das colunas.')

    elif action == 'show_range':
        st.write(' ')
        st.write(' ')
        st.write('Clicando no botão, uma tabela será mostrada em ordem do melhor para o pior colodao, de acordo com o Ranking.')
        st.write(' ')

    botao = st.button(label='Mostre-me meus resultados.')

    if botao:
        if action == 'show_range':

            st.write(f"""## TABELA {status} RESUMO: DE {inicio} ATÉ {final} ({len(pregoes)} PREGÕES AO TOTAL)""")

            st.write(df_show_range)

        if action == 'show_daily':
            st.write(df_show_daily)
