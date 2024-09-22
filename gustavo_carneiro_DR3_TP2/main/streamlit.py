#Crie uma aplicação demo utilizando Streamlit, que incluirá:
#Um título para o projeto.
#Uma descrição do problema de negócio e dos objetivos do projeto.
#Links úteis para as iniciativas e fontes de inspiração do projeto.
#Uma tabela exibindo amostras dos dados que serão utilizados ao longo do projeto.

import streamlit as st
import pandas as pd
import numpy as np
import os

st.title("AI Learn - Trilha de Aprendizagem Personalizada")

st.header("Um dos problemas do sistema de ensino atual é a dificuldade para criar uma trilha personalizada para cada aluno. Minha aplicação irá criar uma trilha individual baseada nas dificuldades dos alunos que servirá como auxílio extra para os estudos visando ajudar individualmente nos pontos fracos de cada um.")


st.markdown("Links úteis para as iniciativas")

st.markdown("https://www.kaggle.com/datasets/lauroliveira/enem-2019-dados-tratados")

# ler csv
df = pd.read_csv("data\enem.csv")
# reduz o arquivo enem.scv para 10000 linhas para consumir menos espaço e eu consiga mandar
df = df.sample(10000)
#deleta o arquivo original para economizar espaço
os.remove("data\enem.csv")
# atualiza o arquivo
df.to_csv("data\enem.csv", index=False)

# mostra a tabela
st.header("Tabela")
st.write(df.head(10))

