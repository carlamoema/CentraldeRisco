#pip install babel
# Importando as bibliotecas que serão utilizadas
import streamlit as st
import pandas as pd
import glob as gl
import datetime as dt 
import plotly.express as px
import matplotlib as mat
from PIL import Image


st.set_page_config(page_title='Home', page_icon='📈', layout='wide')

#----------------------------------------------------Funções --------------------------------------------------------------------------#
def read_code(pathfile):
     """Esta função recebe como parâmetro o caminho dos arquivos no formato 'dataset/*.csv' lê todos os arquivos.csv 
        da pasta dataset que contém os dados correspondentes a cada database e concatena em um só dataframe.
        1- Cria uma lista com os nomes dos arquivos do dataset, foram mantidos os arquivos de 2023 (01,02,03,04,05).
        2- Cria uma lista vazia para armazenar os dataframes.
        3- Usa uma estrutura de repetição para ler cada arquivo e armazenar na lista dfs, importando apenas as colunas que serão usadas.
        4- Concatena os dataframes em um só, o comando concat precisa receber com parâmetro a lista de dfs
     """
     arquivos = gl.glob(pathfile, recursive=True)
     dfs=[]
     for arquivo in arquivos:
          df = pd.read_csv(arquivo, sep=';', 
                                    encoding='utf-8', 
                                    thousands='.', 
                                    decimal=',', 
                                    usecols=['data_base', 'uf', 
                                             'carteira_ativa', 'ativo_problematico', 
                                             'carteira_inadimplida_arrastada', 'cliente', 
                                             'modalidade', 'porte', 'ocupacao', 'cnae_secao'])
          dfs.append(df)
     df= pd.concat(dfs, ignore_index=True)
     return df
     
def clean_code(df):    
     """Esta função realiza a limpeza dos dados do dataframe:
     1- Extrai os espaços vazios da coluna 'cliente'
     2- Extrai os espaços vazios da coluna 'uf' 
     """
     df.loc[:, 'cliente']= df.loc[:, 'cliente'].str.strip()
     df.loc[:, 'uf']= df.loc[:, 'uf'].str.strip()
     df.loc[:, 'ocupacao']= df.loc[:, 'ocupacao'].str.strip('PF - ')
     df.loc[:, 'cnae_secao']= df.loc[:, 'cnae_secao'].str.strip('PJ - ')
     df.loc[:, 'porte']= df.loc[:, 'porte'].str.strip('PF - ')
     df.loc[:, 'modalidade']= df.loc[:, 'modalidade'].str.strip('PF - ')
     df.loc[:, 'modalidade']= df.loc[:, 'modalidade'].str.strip('PJ - ')
     return df

def change_code(df):
     """ 
     Esta função ajusta os tipo de dados de acordo com a informação contida nele
     1 - Alterando a coluna data-base para tipo datetime         
     2 - Ajustando as colunas 'ativo_problematico' e 'carteira_inadimplida_arrastada' para tipo float
     3 - Ajustando a Coluna Ocupacao para os cliente PJ (substituindo pelos dados da coluna cnae_secao - Atividade principal)    
     """
     df['data_base'] = pd.to_datetime(df['data_base']) 
     df['carteira_inadimplida_arrastada'].astype(float, copy=False)
     df.loc[df['cliente']=='PJ', 'ocupacao']= df['cnae_secao']
     return df

def inadimp_uf(df2):
     """ 
     Esta função calcula os valores do cartões de Maior e Menor Inadimplência por Estado,
         e Inadimplência média considerando todo o país.
     """
     cols=['data_base', 'uf','carteira_inadimplida_arrastada','carteira_ativa']  
     df3=df2.loc[:,cols].groupby(['data_base','uf']).sum().reset_index()
     df3['Indice_inadimplencia']=(df3['carteira_inadimplida_arrastada']/df3['carteira_ativa'])*100
     df_aux=df3.sort_values('Indice_inadimplencia', ascending=True).head(1)
     menor_ind=df_aux['Indice_inadimplencia'].iloc[0]       
     menor_uf = df_aux['uf'].iloc[0]
     df_aux=df3.sort_values('Indice_inadimplencia', ascending=True).tail(1)
     maior_ind=df_aux['Indice_inadimplencia'].iloc[0]       
     maior_uf = df_aux['uf'].iloc[0]
     media_ind=df3.loc[:,'Indice_inadimplencia'].mean() 
     return (menor_ind, menor_uf, maior_ind, maior_uf, media_ind)

def inadimp_seg(df2, categoria):
     """
     Esta função agrupa as carteiras por categoria (modalidade/ocupação/porte) a depender
     do parâmetro.
     """
     cols=[categoria, 'carteira_ativa','carteira_inadimplida_arrastada', 'ativo_problematico']
     df3=df2.loc[:,cols].groupby(categoria).sum().reset_index()
     return df3

def inadimp_uf_avg(df2):
     """
     Esta função calcula a média da carteiras inadimplida por uf.
     """
     cols=['uf','carteira_inadimplida_arrastada']
     df3= df2.loc[:,cols].groupby('uf').mean().reset_index()
     df3.columns=['uf','Inadimplencia_media']
     return df3

def inadimp_uf_time(df1, ufs):
     """
     Esta função calcula a evolução da carteira de inadimplência durante os meses considerando
     três estados passados como parâmetros.
     """
     cols=['data_base', 'uf','carteira_inadimplida_arrastada','carteira_ativa']   
     df3=df1.query(ufs).loc[:, cols].groupby(['uf', 'data_base']).sum().reset_index()      
     df3['Inadimplência %']= (df3['carteira_inadimplida_arrastada']/df3['carteira_ativa'])*100     
     df3['mes'] = df3['data_base'].dt.month_name() #Criando uma coluna com o nome do mês do campo data_base
     return df3

def inadimp_uf_ocup(df1, uf):
     """
     Esta função calcula a evolução da carteira de inadimplência durante os meses por UF por ocupação.
     """
     df3= df1.query(uf)
     cols=['data_base','carteira_inadimplida_arrastada','carteira_ativa', 'ocupacao']
     df3=df1.loc[:, cols].groupby(['ocupacao', 'data_base']).sum().reset_index()
     df3['Inadimplência %']= (df3['carteira_inadimplida_arrastada']/df3['carteira_ativa'])*100
     df3['mes'] = df3['data_base'].dt.month_name() #Criando uma coluna com o nome do mês do campo data_base
     return df3

def formatar_numero_localizacao(numero, localizacao='pt_BR'):
     """ 
     Esta função formata o número de acordo com a localização, foi usada para melhorar a visualização de números muito grandes (Bilhões)"""
     locale = Locale.parse(localizacao)
     return format_number(numero, locale=locale)
#-------------------------------------------------------------------------------------------------------------#

#-------------------------Lendo o dataset --------------------------------------------------------------------#
pathfile= 'dataset/*.csv'
df = read_code(pathfile)
#------------------------- Limpando os dados -----------------------------------------------------------------#
df= clean_code(df)

#------------------------- Alterando os tipos de dados -------------------------------------------------------#
df= change_code(df)

#df contém o dataset dos meses 01 a 04 do ano 2023

#============================================================================================================#
#                                            Layout no Streamlit                                             #
#============================================================================================================#

st.title(' Informações de Crédito ')


image=Image.open('images/logo_man.jpg')
st.sidebar.image(image, width=180)
st.sidebar.markdown("## Sistema Financeiro Nacional")
st.sidebar.markdown("##### Dados do Banco Central do Brasil")
st.sidebar.markdown("""---""")

#------------------------------------- Seleção do tipo de Pessoa com os botões-------------------------------#

selecao = st.sidebar.radio(
    "Escolha o Tipo:",
    ('Pessoa Jurídica', 'Pessoa Física' ))

if selecao == 'Pessoa Jurídica':
    tipo='PJ'
else:
    tipo = 'PF'

df1 = df.query(f'cliente=="{tipo}"')

meses=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto']
selected_month = st.sidebar.selectbox('Selecione um mês: ', meses)
st.markdown("""---""")

     
match selected_month:
     case 'Janeiro':
          df2=df1.query('data_base=="2023-01-31"')
     case 'Fevereiro':
          df2=df1.query('data_base=="2023-02-28"')
     case 'Março':
          df2=df1.query('data_base=="2023-03-31"')
     case 'Abril':
          df2=df1.query('data_base=="2023-04-30"')
     case 'Maio':
          df2=df1.query('data_base=="2023-05-31"')
     case 'Junho':
          df2=df1.query('data_base=="2023-06-30"')
     case 'Julho':
          df2=df1.query('data_base=="2023-07-31"')
     case 'Agosto':
          df2=df1.query('data_base=="2023-08-31"')     
             
      
#------------------------------------------  Estrutura com Abas -----------------------------------------------#
tab1, tab2= st.tabs(['Goiás', 'Brasil'])

with tab1: # Goiás
     df3= df2.query('uf=="GO"')
     with st.container():
          col1, col2, col3, col4, col5 = st.columns(spec=5, gap='medium')
          with col1:
               cols=['carteira_ativa','carteira_inadimplida_arrastada']
               sum_cart_ativa= df3['carteira_ativa'].sum()
               sum_cart_indimp=df3['carteira_inadimplida_arrastada'].sum()
               Inadimp=(sum_cart_indimp/sum_cart_ativa)*100
               col1.metric(label = "Índice Inadimplência %", value=round(Inadimp,2))
          
          with col2:
               valor_formatado_string = formatar_numero_localizacao(sum_cart_ativa)
               col2.metric(label='Valor da Carteira', value=round(valor_formatado_string,0))
               
#------------------------------------------  Estrutura com Containers -----------------------------------------#
#------------------------------------------  Cartões com Indicadores ------------------------------------------#
     
with tab2: # Brasil
#------------------------------------------  Estrutura com Containers -----------------------------------------#
#------------------------------------------  Cartões com Indicadores ------------------------------------------#
     with st.container(): 
          [menor_ind, menor_uf, maior_ind, maior_uf, media_ind]=inadimp_uf(df2)
          col1, col2, col3 = st.columns(spec=3, gap='medium')
          with col1: ## Cartão com Uf Menor Inadimplência Relativa e valor
               col1.markdown('Menor inadimplência %')
               col1.metric(label = menor_uf, value=round(menor_ind,2))
               
          with col2: ## Cartão com Uf Maior Inadimplência Relativa e valor
               col2.markdown('Maior inadimplência %')
               col2.metric(label = maior_uf, value=round(maior_ind,2))
                                   
          with col3: ## Cartão com Inadimplência Média Relativa por Cliente
               col3.markdown('Inadimplência Média')
               col3.metric(label = "%", value=round(media_ind,2))
     
          st.markdown("""---""")  
          
     #--------------------------------------------------------------------------------------------------------------#       
     #----------------------------------------------  Gráficos -----------------------------------------------------#

     with st.container(): 
          ## Gráfico de Barras Verticais - Y = Inadimplência X = Modalidades
          categoria= 'modalidade'
          df3= inadimp_seg(df2, categoria)
          fig=px.bar(df3, x=categoria, 
                         y=['carteira_ativa','ativo_problematico', 'carteira_inadimplida_arrastada'], 
                         barmode='group',
                         title='Carteira de Crédito segmentada em Modalidades',                      
                         color_discrete_sequence= px.colors.qualitative.G10,
                         height=800
                         )
          st.plotly_chart(fig, use_container_width=True)

     with st.container(): 
          ## Gráfico de Barras Verticais - Y = Inadimplência X = Ocupação
          categoria= 'ocupacao'
          df3 = inadimp_seg(df2, categoria)
          fig=px.bar(df3, x=categoria, 
                         y=['carteira_ativa','ativo_problematico', 'carteira_inadimplida_arrastada'], 
                         barmode='group',
                         title='Carteira de Crédito por Ocupação',                      
                         color_discrete_sequence= px.colors.qualitative.G10,
                         height=800
                         )
          st.plotly_chart(fig, use_container_width=True)
          
     with st.container(): # Gráfico de dispersão - Inadimplência nos Estados
          df3=inadimp_uf_avg(df2)
          fig = px.scatter(df3,
                    x='uf',
                    y='Inadimplencia_media',
                    hover_name='uf',
                    title= 'Carteira Inadimplida média por UF',
                    labels={'Inadimplencia_media': 'Inadimplência Média', 'uf':'UF'}, 
                    color_discrete_sequence= px.colors.qualitative.T10)
          st.plotly_chart(fig, use_container_width=True)
          
               
     with st.container(): # Gráfico de Linhas - Comparando inadimplência em RJ/SP/GO
          ufs="uf==['RJ','SP','GO']"
          df3=inadimp_uf_time(df1, ufs)
          fig =px.line(df3,
                         x='mes',
                         y='Inadimplência %',
                         color='uf', 
                         title='Comparativo da Inadimplência nos Estados',
                         color_discrete_sequence= px.colors.qualitative.T10
                         )
          st.plotly_chart(fig, use_container_width=True)
          
     with st.container(): # Gráfico de Linhas - Evolução da inadimplência por ocupação em GO
          uf="uf=='GO'"
          df3=inadimp_uf_ocup(df1, uf)
          fig=px.line(df3,
               x='mes',
               y='Inadimplência %',
               color='ocupacao', 
               title='Inadimplência por Ocupação no estado de GO'
               )
          st.plotly_chart(fig, use_container_width=True) 
     
     with st.container(): 
          uf="uf=='RJ'"
          df3=inadimp_uf_ocup(df1, uf)
          fig=px.line(df3,
               x='mes',
               y='Inadimplência %',
               color='ocupacao', 
               title='Inadimplência por Ocupação no estado de RJ'
               )
          st.plotly_chart(fig, use_container_width=True) 
          
     with st.container(): 
          uf="uf=='SP'"
          df3=inadimp_uf_ocup(df1, uf)
          fig=px.line(df3,
               x='mes',
               y='Inadimplência %',
               color='ocupacao', 
               title='Inadimplência por Ocupação no estado de SP'
               )
          st.plotly_chart(fig, use_container_width=True) 


