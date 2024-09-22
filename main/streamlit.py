import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import requests
import cachetools as ct

cacheIntro = ct.TTLCache(maxsize=float('inf'), ttl=86400)  
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
        links = {
            "Kaggle": "https://www.kaggle.com/datasets/lauroliveira/enem-2019-dados-tratados"
        }
        st.markdown("Links úteis para as iniciativas")
        for nome, link in links.items():
            st.markdown(f"[{nome}]({link})")

        # Tabela
        st.header("Tabela")
        df = pd.read_csv("data/enem.csv")
        df = df.sample(10000)
        os.remove("data/enem.csv")
        df.to_csv("data/enem.csv", index=False)
        # adiciona uma coluna com a média das notas notas_ct, nota_ch, nota_lc, nota_mt, nota_redacao

        df['media_das_notas'] = df[['nota_ct', 'nota_ch', 'nota_lc', 'nota_mt', 'nota_redacao']].mean(axis=1)

        st.write("Aqui está uma amostra dos dados que serão utilizados:")
        st.dataframe(df.head(10))

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

        st.header("Download")

        st.download_button(
            label="Download",
            data=df.to_csv(),
            file_name="enem.csv",
            mime="text/csv",
        )

        # - Reset

        st.header("Reset")

        if st.button('Reset'):
            df = pd.read_csv("data/enem.csv")
            st.write('Dados resetados com sucesso!')
            # limpa o selectbox

            colunas = df.columns
            colunas = colunas.drop('inscricao')


        # - Upload

        st.header("Upload")

        uploaded_file = st.file_uploader("Selecione um arquivo CSV", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)
        
        # - Salvar
        cacheIntro['dados'] = df

# -----

def formulario():
    cacheForm = ct.TTLCache(maxsize=float('inf'), ttl=86400)  
    if 'dados' in cacheForm:
        st.write(cacheForm['dados'])
        nome, idade, df = cacheForm['dados']
        st.write("Formulario")
        st.write(f'Nome: {nome}')
        st.write(f'Idade: {idade}')
        st.write("Grafico de exemplo")
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        st.pyplot(fig)
    else:
        st.write("Formulario")
        nome = st.text_input('Digite seu nome')

        idade = st.slider('Selecione sua idade', 0, 100, 25)

        st.write(f'Nome: {nome}')
        st.write(f'Idade: {idade}')

        st.write("Grafico de exemplo como placeholder")
        df = pd.DataFrame({'Coluna 1': [1, 2, 3], 'Coluna 2': [4, 5, 6]})
        st.write(df)

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        st.pyplot(fig)

    if st.button('Enviar para o cache'):
        cacheForm['dados'] = nome, idade, df
        st.write('Dados enviados com sucesso!')

    if st.button('Reset'):
        df = pd.DataFrame({'Coluna 1': [1, 2, 3], 'Coluna 2': [4, 5, 6]})
        st.write('Dados resetados com sucesso!')


cache = ct.TTLCache(maxsize=float('inf'), ttl=86400)    
def analise_web(): 
    # Verifica se os dados estão no cache
    if 'text' in cache:
        st.write(cache['text'])
    else:
        # Requisição da página
        url = 'https://www.romanews.com.br/cidades/hoje-e-dia-do-cliente-confira-lojas-com-programacao-especial-e-descontos-em-belem-0924'

        # Requisição da página
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            soup = bs(response.content, 'html.parser')
            text = soup.get_text()
            # Armazena os dados no cache
            cache['text'] = text
            st.write(text)
        else:
            print("Requisição não foi bem-sucedida")
            print(f"Status code: {response.status_code}")

# Usa um sidebar para fazer a paginação
page = st.sidebar.selectbox('Selecione uma opção', ['Introdução', 'Formulário', 'Analise Web'])

if page == 'Introdução':
    introducao()
elif page == 'Formulário':
    formulario()
elif page == 'Analise Web':
    analise_web()



