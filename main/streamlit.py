import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import requests
import cachetools as ct

from scrapping import *

cacheIntro = ct.TTLCache(maxsize=float('inf'), ttl=86400)  
cache = ct.TTLCache(maxsize=float('inf'), ttl=86400)
def introducao():
    if 'dados' in cacheIntro:
        st.write(cacheIntro['dados'])
    else:
        st.write("Introdução")

        st.title("AI Learn - Trilha de Aprendizagem Personalizada")

        # Problema
        st.header("Um dos problemas do sistema de ensino atual é a dificuldade para criar uma trilha personalizada para cada aluno.")
        st.write("Minha aplicação irá criar uma trilha individual baseada nas dificuldades dos alunos que servirá como auxílio extra para os estudos visando ajudar individualmente nos pontos fracos de cada um.")

        # Links
        st.markdown("Link dos dados usados:")
        links = {
            "Kaggle": "https://www.kaggle.com/datasets/lauroliveira/enem-2019-dados-tratados"
        }
        
        for nome, link in links.items():
            st.markdown(f"[{nome}]({link})")


        # Tabela
        st.header("Tabela")
        df = pd.read_csv("./data/enem copy.csv")
        df = df.sample(10000)

        st.write("Aqui está uma amostra dos dados que serão utilizados:")
        st.dataframe(df.head(10))

        # - Download
        st.download_button(
            label="Download",
            data=df.to_csv(),
            file_name="enem.csv",
            mime="text/csv",
        )

        # - Salvar
        cacheIntro['dados'] = df

# -----

def analise_dinamica():
    st.header("Analise dinâmica")

    # Tabela
    st.header("Tabela")
    df = pd.read_csv("./data/enem.csv")
    df = df.sample(10000)
    os.remove("./data/enem.csv")
    df.to_csv("./data/enem.csv", index=False)
    # adiciona uma coluna com a média das notas notas_ct, nota_ch, nota_lc, nota_mt, nota_redacao

    df['media_das_notas'] = df[['nota_ct', 'nota_ch', 'nota_lc', 'nota_mt', 'nota_redacao']].mean(axis=1)

    # - Select box das colunas do df acima
    colunas = df.columns
    colunas = colunas.drop('inscricao')

    st.header("Selecione uma coluna")
    coluna = st.selectbox('Selecione uma coluna', colunas)

    # - Select box das opções
    opcoes = df[coluna].unique()
    opcoes = np.sort(opcoes)
    st.header("Selecione uma opção")
    opcao = st.multiselect('Selecione uma opção', opcoes, default=opcoes)

    # - Tabela filtrada
    st.header("Tabela filtrada")
    df = df[df[coluna].isin(opcao)]
    st.dataframe(df)



    # - Grafico da médias das notas por coluna filtrada

    st.header("Grafico")

    fig, ax = plt.subplots()
    ax.bar(df[coluna], df['media_das_notas'])
    ax.set_xlabel(coluna)
    ax.set_ylabel('Media das notas')
    st.pyplot(fig)

    # - Download
    st.download_button(
        label="Download",
        data=df.to_csv(),
        file_name="enem.csv",
        mime="text/csv",
    )



def upload():
    st.header("Upload para analise individual")
    uploaded_file = st.file_uploader("Selecione um arquivo CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
    
    st.write('Dados carregados com sucesso!')

    st.subheader('Trilha personalizada via machine learning')
    st.write('Em desenvolvimento...')


def scrapping(): 
    st.header("Scrapping")

    st.write("Selecione o cargo e a região:")

    # digite o cargo e a região
    cargo = st.text_input('Cargo')

    regiao = st.text_input('Região')

    num_pags = st.text_input('Quantidade de paginas')

    # button para executar o scraping
    if st.button('Executar o scraping'):
        if cargo == '':
            cargo = 'Analista de Dados'
        if regiao == '':
            regiao = 'São Paulo'
        if num_pags == '':
            num_pags = 2
        executar_scrapping(cargo, regiao, num_pags)

    df = pd.read_json('./arquivosGerados/8_vagasIndeed.json')
    st.dataframe(df)

# Usa um sidebar para fazer a paginação
page = st.sidebar.selectbox('Selecione uma opção', ['Introdução', 'Analise dinâmica', 'Upload para análise individual', 'Scrapping'])

if page == 'Introdução':
    introducao()
elif page == 'Analise dinâmica':
    analise_dinamica()
elif page == 'Upload para análise individual':
    upload()
elif page == 'Scrapping':
    scrapping()



