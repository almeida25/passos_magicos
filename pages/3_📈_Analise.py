import streamlit as st
import pandas as pd
import plotly.express as px
from auxiliar import apply_custom_style
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def adicionar_colunas_faltantes(df, colunas_unicas):
    for col in colunas_unicas:
        if col not in df.columns:
            df[col] = None  # deixa valores da coluna zerados

    # Função para atualizar 'ANO_INGRESSO' para linhas de 2021 baseado no dicionário
def atualizar_ano_ingresso(row, dict_nome_ano_ingresso):
    if row['ANO_PESQUISA'] == 2021 and row['NOME'] in dict_nome_ano_ingresso:
        return dict_nome_ano_ingresso[row['NOME']]
    else:
        return row['ANO_INGRESSO']


# Função para atualizar 'ANO_PM' para linhas de 2021 baseado no dicionário de 2020 adicionando 1 ano, caso "ANO_INGRESSO" seja igual a 0
def atualizar_anos_pm(row, dict_nome_anos_pm):
    if row['ANO_PESQUISA'] == 2021 and row['ANO_INGRESSO'] == 0 and row['NOME'] in dict_nome_anos_pm:
        return dict_nome_anos_pm[row['NOME']] + 1
    else:
        return row['ANOS_PM']

def get_df_ml():
    df = pd.read_csv("./dados/PEDE_PASSOS_DATASET_FIAP.csv", sep= ";")
    df_2020 = df[[col for col in df.columns if "2020" in col]].copy() #filtra as colunas com "_2020" e adiciona em um novo df
    df_2020.columns = [col.replace("_2020", "") for col in df_2020.columns] # retira caractere numérico da coluna para padronizar
    df_2020["NOME"] = df["NOME"] #adiciona identificador do aluno
    df_2020["ANO_PESQUISA"] = 2020 #adiciona coluna de ano
    cols_nulo_2020 = df_2020.columns.difference(['NOME', 'ANO_PESQUISA']) # excluir
    df_2020 = df_2020.dropna(how='all', subset=cols_nulo_2020).reset_index() # Excluir linhas onde todas as colunas no subset especificado são NaN

    df_2021 = df[[col for col in df.columns if "2021" in col]].copy() #filtra as colunas com "_2021" e adiciona em um novo df
    df_2021.columns = [col.replace("_2021", "") for col in df_2021.columns] # retira caractere numérico da coluna para padronizar
    df_2021["NOME"] = df["NOME"] #adiciona identificador do aluno
    df_2021["ANO_PESQUISA"] = 2021 #adiciona coluna de ano
    cols_nulo_2021 = df_2021.columns.difference(['NOME', 'ANO_PESQUISA']) # excluir
    df_2021 = df_2021.dropna(how='all', subset=cols_nulo_2021).reset_index() # Excluir linhas onde todas as colunas no subset especificado são NaN

    df_2022 = df[[col for col in df.columns if "2022" in col]].copy() #filtra as colunas com "_2022" e adiciona em um novo df
    df_2022.columns = [col.replace("_2022", "") for col in df_2022.columns] # retira caractere numérico da coluna para padronizar
    df_2022["NOME"] = df["NOME"] #adiciona identificador do aluno
    df_2022["ANO_PESQUISA"] = 2022 #adiciona coluna de ano
    cols_nulo_2022 = df_2022.columns.difference(['NOME', 'ANO_PESQUISA']) # excluir
    df_2022 = df_2022.dropna(how='all', subset=cols_nulo_2022).reset_index() # Excluir linhas onde todas as colunas no subset especificado são NaN
    # Separação de dados entre "FASE_TURMA" no df_2020 para ficar similar aos demais
    df_2020[['FASE', 'TURMA']] = df_2020['FASE_TURMA'].str.extract('(\d+)(\D+)')
    df_2020 = df_2020.drop(['FASE_TURMA'], axis=1) #excluindo coluna principal
    col_2020 = df_2020.columns

    col_2020 = list(df_2020.columns)
    col_2021 = list(df_2021.columns)
    col_2022 = list(df_2022.columns)
    colunas_unicas = list(set(col_2020 + col_2021 + col_2022)) # agregar todas colunas dos 3 dataframes em uma única lista, excluindo valores duplicados

    adicionar_colunas_faltantes(df_2020, colunas_unicas)
    adicionar_colunas_faltantes(df_2021, colunas_unicas)
    adicionar_colunas_faltantes(df_2022, colunas_unicas)

    df_final_passos = pd.concat([df_2020, df_2021, df_2022], ignore_index=True)
    colunas = ['IEG', 'IDA', 'IPV', 'IAA', 'IPS', 'IPP', 'IAN', 'IDADE_ALUNO', 'ANOS_PM', 'INDE']
    
    for coluna in colunas:
        df_final_passos[coluna] = pd.to_numeric(df_final_passos[coluna], errors='coerce')
    # organiza dados em colunas
    df_final_passos = df_final_passos[['NOME','ANO_PESQUISA','ANO_INGRESSO','INSTITUICAO_ENSINO_ALUNO','IDADE_ALUNO','ANOS_PM','FASE','TURMA','NIVEL_IDEAL','PONTO_VIRADA','INDICADO_BOLSA','BOLSISTA','INDE','INDE_CONCEITO','PEDRA','DESTAQUE_IEG','DESTAQUE_IDA','DESTAQUE_IPV','IEG','IDA','IPV','IAA','IPS','IPP','IAN','CF','CG','CT','QTD_AVAL','REC_AVA_1','REC_AVA_2','REC_AVA_3','REC_AVA_4','REC_EQUIPE_1','REC_EQUIPE_2','REC_EQUIPE_3','REC_EQUIPE_4','DEFASAGEM','SINALIZADOR_INGRESSANTE','NOTA_PORT','NOTA_MAT','NOTA_ING']]

    df_final_passos = pd.concat([df_2020, df_2021, df_2022], ignore_index=True)
    colunas = ['IEG', 'IDA', 'IPV', 'IAA', 'IPS', 'IPP', 'IAN', 'IDADE_ALUNO', 'ANOS_PM', 'INDE']
    for coluna in colunas:
        df_final_passos[coluna] = pd.to_numeric(df_final_passos[coluna], errors='coerce')
        
    # organiza dados em colunas
    df_final_filtrado  = df_final_passos[['NOME','ANO_PESQUISA','ANO_INGRESSO','INSTITUICAO_ENSINO_ALUNO','IDADE_ALUNO','ANOS_PM','FASE','TURMA','NIVEL_IDEAL','PONTO_VIRADA','INDICADO_BOLSA','BOLSISTA','INDE','INDE_CONCEITO','PEDRA','DESTAQUE_IEG','DESTAQUE_IDA','DESTAQUE_IPV','IEG','IDA','IPV','IAA','IPS','IPP','IAN','CF','CG','CT','QTD_AVAL','REC_AVA_1','REC_AVA_2','REC_AVA_3','REC_AVA_4','REC_EQUIPE_1','REC_EQUIPE_2','REC_EQUIPE_3','REC_EQUIPE_4','DEFASAGEM','SINALIZADOR_INGRESSANTE','NOTA_PORT','NOTA_MAT','NOTA_ING']]
    excluir_outlier = df_final_filtrado[df_final_filtrado['NOME'] == 'ALUNO-1259'].index
    df_final_filtrado = df_final_filtrado.drop(excluir_outlier)

    colunas = ['IEG', 'IDA', 'IPV', 'IAA', 'IPS', 'IPP', 'IAN', 'ANOS_PM', 'INDE']
    for coluna in colunas:
        df_final_filtrado[coluna] = pd.to_numeric(df_final_filtrado[coluna], errors='coerce')

    dict_nivel_ideal = {
    "ALFA  (2o e 3o ano)"       :	0.5, 
    "ALFA  (2º e 3º ano)"       :	0.5,
    "Nível 1 (4o ano)"          :	1,
    "Fase 1 (4º ano)"           :	1,
    "Nível 2 (5o e 6o ano)"     :	2,
    "Fase 2 (5º e 6º ano)"      :	2,
    "Nível 3 (7o e 8o ano)"     :	3,
    "Fase 3 (7º e 8º ano)"      :	3,
    "Fase 4 (9º ano)"           :	4,
    "Nível 4 (9o ano)"          :	4,
    "Fase 5 (1º EM)"            :	5,
    "Nível 5 (1o EM)"           :	5,
    "Fase 6 (2º EM)"            :	6,
    "Nível 6 (2o EM)"           :	6,
    "Fase 7 (3º EM)"            :	7,
    "Nível 7 (3o EM)"           :	7,
    "Nível 8 (Universitários)"  :	8,
    "Fase 8 (Universitários)"   :	8
    }

    df_final_filtrado['NIVEL_IDEAL'] = df_final_filtrado['NIVEL_IDEAL'].map(dict_nivel_ideal).fillna(0).astype(float) # trata valores nulos como 0
    df_final_filtrado['NIVEL_IDEAL'].value_counts()

    condicao_bolsista = df_final_filtrado['BOLSISTA'] == 'Sim'  
    condicao_instituicao = df_final_filtrado['INSTITUICAO_ENSINO_ALUNO'].notna() & (df_final_filtrado['INSTITUICAO_ENSINO_ALUNO'] != 'Escola Pública')

    df_final_filtrado['BOLSISTA_GERAL'] = (condicao_bolsista | condicao_instituicao).astype(int)
    df_final_filtrado = df_final_filtrado.drop(["BOLSISTA"], axis = 1)
    df_final_filtrado["BOLSISTA_GERAL"].value_counts()

    # converter tipo de dado das colunas "ANO_INGRESSO" e "ANOS_PM"  para int (atualmente como float)
    df_final_filtrado['ANO_INGRESSO'] = pd.to_numeric(df_final_filtrado['ANO_INGRESSO'], errors='coerce').fillna(0).astype(int)
    df_final_filtrado['ANOS_PM'] = pd.to_numeric(df_final_filtrado['ANOS_PM'], errors='coerce').fillna(0).astype(int)

    #2021 não tem dados de "ANOS_PM" OU "ANO_INGRESSO", vou criar um dicionário com as informações de 2020 e 2021 por aluno para mapear melhor essa info
    dados_2022 = df_final_filtrado[df_final_filtrado['ANO_PESQUISA'] == 2022]
    dict_nome_ano_ingresso = dados_2022.set_index('NOME')['ANO_INGRESSO'].to_dict()

    dados_2020 = df_final_filtrado[df_final_filtrado['ANO_PESQUISA'] == 2020]
    dict_nome_anos_pm = dados_2020.set_index('NOME')['ANOS_PM'].to_dict()

    df_final_filtrado['ANO_INGRESSO'] = pd.to_numeric(df_final_filtrado['ANO_INGRESSO'], errors='coerce').fillna(0).astype(int)
    df_final_filtrado['ANOS_PM'] = pd.to_numeric(df_final_filtrado['ANOS_PM'], errors='coerce').fillna(0).astype(int)

    #2021 não tem dados de "ANOS_PM" OU "ANO_INGRESSO", vou criar um dicionário com as informações de 2020 e 2021 por aluno para mapear melhor essa info
    dados_2022 = df_final_filtrado[df_final_filtrado['ANO_PESQUISA'] == 2022]
    dict_nome_ano_ingresso = dados_2022.set_index('NOME')['ANO_INGRESSO'].to_dict()

    dados_2020 = df_final_filtrado[df_final_filtrado['ANO_PESQUISA'] == 2020]
    dict_nome_anos_pm = dados_2020.set_index('NOME')['ANOS_PM'].to_dict()

    df_final_filtrado['ANO_INGRESSO'] = df_final_filtrado.apply(lambda row : atualizar_ano_ingresso(row, dict_nome_ano_ingresso), axis=1)
    df_final_filtrado['ANOS_PM'] = df_final_filtrado.apply(lambda row : atualizar_anos_pm (row, dict_nome_anos_pm), axis=1)

    # criar nova coluna mantendo dados de 2020 e fazendo o cálculo entre "ano pesquisa" e "ano_ingresso" para 2021 e 2022
    df_final_filtrado['ANOS_COMO_ALUNO'] = df_final_filtrado.apply(lambda row: row['ANOS_PM'] if row['ANO_INGRESSO'] == 0 else row['ANO_PESQUISA'] - row['ANO_INGRESSO'], axis=1).astype(int)
    df_final_filtrado = df_final_filtrado.drop(["ANO_INGRESSO", "ANOS_PM"], axis = 1)

    df_final_filtrado = df_final_filtrado.loc[df_final_filtrado["PEDRA"] != "#NULO!"]
    df_final_filtrado = df_final_filtrado.loc[df_final_filtrado["PONTO_VIRADA"]!= "#NULO!"]

    dict_pv = { "Não":0, "Sim":1, "#NULO!": None}
    df_final_filtrado['PONTO_VIRADA'] = df_final_filtrado['PONTO_VIRADA'].map(dict_pv).astype(float)

    return df_final_filtrado

def get_df_ml_2022():
    df = pd.read_csv("./dados/PEDE_PASSOS_DATASET_FIAP.csv", sep= ";")
    df_2022 = df[[col for col in df.columns if "2022" in col]].copy() 
    df_2022.columns = [col.replace("_2022", "") for col in df_2022.columns]
    df_2022["NOME"] = df["NOME"]
    df_2022["ANO_PESQUISA"] = 2022
    cols_nulo_2022 = df_2022.columns.difference(['NOME', 'ANO_PESQUISA'])
    df_2022 = df_2022.dropna(how='all', subset=cols_nulo_2022).reset_index(drop=True)

    # df_2022 = df_2022.drop(columns=["REC_EQUIPE_1", "DEFASAGEM", "INDE_CONCEITO", "REC_AVA_4", "REC_AVA_3", "NOTA_ING", "REC_EQUIPE_2", "REC_EQUIPE_4", "ANOS_PM", "IDADE_ALUNO", "INSTITUICAO_ENSINO_ALUNO", "REC_EQUIPE_3", "SINALIZADOR_INGRESSANTE"])
    # df_2022 = df_2022.drop(columns=['index', 'NOME', 'ANO_PESQUISA', 'PEDRA'])
    
    return df_2022

def get_df_final_filtrado():
    df = pd.read_csv("./dados/df_final_filtrado.csv", sep= ",")
    return df

def get_df_final_v2():
    df = pd.read_csv('./dados/df_final_passos-v2.csv')
    df = df.loc[df['ANO_PESQUISA'] == 2022]
    df['categoria_bolsa'] = ''
    for idx, row in df.iterrows():
        if row['BOLSISTA'] == 'Sim':
            df.loc[df.index == idx, 'categoria_bolsa'] = 'Bolsista desde o ano anterior'
            
        elif row['INDICADO_BOLSA'] == 'Sim':
            df.loc[df.index == idx, 'categoria_bolsa'] = 'Indicado a bolsa'

        else:
            df.loc[df.index == idx, 'categoria_bolsa'] = 'Não indicado a bolsa'
    return df 

def read_dataset():
    df = pd.read_csv('./dados/PEDE_PASSOS_DATASET_FIAP.csv', header=0, sep=';')
    return df

def read_final_dataset():
    df = pd.read_csv('./dados/df_final_passos.csv', header=0, sep=',')
    return df

def get_qtd_student_by_year(df:pd.DataFrame, ano:int):
    dic_ano = {
        2020: 'PEDRA_2020',
        2021: 'PEDRA_2021',
        2022: 'PEDRA_2022'
    }
    df_filtered = df[['NOME','PEDRA_2020', 'PEDRA_2021', 'PEDRA_2022']] 
    df_filtered = df_filtered.loc[~df_filtered[dic_ano[ano]].isna()]
    return df_filtered

def get_df_indicators(df:pd.DataFrame, indicators:list, years:list):
    indicators.append('ANO')
    df_filtered = df[indicators]
    if len(years) > 0:

        df_filtered = df_filtered.loc[df_filtered['ANO'].isin(years)]
    return df_filtered

def get_df_final():
    df = pd.read_csv('./dados/df_tratado.csv', sep= ",", index_col = False)
    return df

if __name__ == '__main__':
    apply_custom_style()
    st.title('📈 Análise')

    tab_interacao, tab_insights, tab_modelo = st.tabs(['Interação', 'Insights', 'Modelo de Machine Learning'])

    # st.subheader('Banco de dados')

    with tab_interacao:
        with st.spinner('Aguardando carregamento'):
            st.write('Com os dados disponibilizados é possível realizar um acompanhamento e ')

            # Leitura do dataset
            df_pm = read_dataset()

            st.write(f'A pesquisa conta com {str(df_pm.shape[0])} alunos, sendo eles dividos entre \
                    os periodos de tempo de 2020 a 2022.')
            
            df_filtered = get_qtd_student_by_year(df_pm, 2022)
            qtd_2022_student = df_filtered.shape[0]

            df_filtered = get_qtd_student_by_year(df_pm, 2021)
            qtd_2021_student = df_filtered.shape[0]
            
            df_filtered = get_qtd_student_by_year(df_pm, 2020)
            qtd_2020_student = df_filtered.shape[0]

            df_by_year = {
                'Ano': ['2020', '2021', '2022'],
                'Quantidade Alunos': [qtd_2020_student, qtd_2021_student, qtd_2022_student]
            }

            df_by_year = pd.DataFrame(df_by_year)

            st.markdown('<h4>Quantidade de alunos em cada ano</h4>', unsafe_allow_html=True)
            st.line_chart(df_by_year, x='Ano')

            df_final_pm = read_final_dataset()

            st.divider()
            # Grafico de pie
            st.subheader('Avaliação das Pedras por ano:')
            list_year = st.multiselect('Selecione o ano', [2020,2021,2022], default=[2020])
            if len(list_year) > 0:
                df_grouped_pedra = df_final_pm.loc[df_final_pm['ANO'].isin(list_year)].groupby('PEDRA').count()
                df_grouped_pedra = df_grouped_pedra.loc[['Ametista','Quartzo', 'Topázio', 'Ágata']]
                df_grouped_pedra['Porcentagem'] = df_grouped_pedra['Unnamed: 0']
                fig = px.pie(df_grouped_pedra,values='Porcentagem', names=df_grouped_pedra.index, title='Porcentagem dos alunos')
                st.plotly_chart(fig)

            # df_filtered = get_df_indicators(df_final_pm, select_ind, select_year)

            st.divider()

            st.subheader('Avaliação dos indices')
            list_year = st.multiselect('Selecione o ano', [2020,2021,2022], default=[2020], key='multi_ind_year')
            indicators = ('IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN')
            select_ind = st.multiselect('Indicadores', indicators, default=['IAA'], key='mult_ind')
            if len(list_year) > 0 and len(select_ind) > 0:
                df_avaliacao = df_final_pm.loc[df_final_pm['ANO'].isin(list_year)]
                df_avaliacao = df_avaliacao[select_ind]
                df_avaliacao_sem_nulos = df_avaliacao.dropna()
                try:
                    df_avaliacao_sem_nulos = df_avaliacao_sem_nulos.drop(1258)
                except:
                    pass
                df_avaliacao_sem_nulos[select_ind] = df_avaliacao_sem_nulos[select_ind].astype(float)
                
                df_mean_avaliacao = df_avaliacao_sem_nulos[select_ind].mean()
                fig = px.bar(df_mean_avaliacao,labels={'index': 'Indice', 'value':'Média Notas'},
                            color=df_mean_avaliacao.index, title='Média dos indicadores')
                st.plotly_chart(fig)

            st.divider()

            st.subheader('Número de alunos por Fase')

            df_pm_fase = df_final_pm[['FASE', 'ANO']].dropna()
            df_pm_fase['FASE'] = df_pm_fase['FASE'].astype(int)
            df_pm_fase['ANO'] = df_pm_fase['ANO'].astype(str)

            fases = df_pm_fase['FASE'].unique().tolist()
            input_fases = st.multiselect('Selecione a fase', fases, default=fases)

            if len(input_fases) > 0:
                df_pm_fase = df_pm_fase.loc[df_pm_fase['FASE'].isin(input_fases)]

                df_pm_fase = df_pm_fase.groupby(['ANO', 'FASE']).size().unstack(fill_value=0)
                fig = px.line(df_pm_fase)
                st.plotly_chart(fig)

    with tab_insights:
        with st.spinner('Aguardando carregamento'):
            df = get_df_final_v2()
            df_grouped_by_categoria_bolsa = df[['categoria_bolsa', 'ANO_PESQUISA']].groupby('categoria_bolsa').count().reset_index()

            st.subheader('Análise de indicadores por alunos indicados ou não a bolsa no ano de pesquisa 2022')

            st.write('COMPARAÇÃO DOS INDICADOS E NÃO INDICADOS A BOLSA EM 2022')
            fig = px.pie(df_grouped_by_categoria_bolsa, values='ANO_PESQUISA', names='categoria_bolsa')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )
            st.plotly_chart(fig)

            st.divider()

            st.write('ANÁLISE IDA E IPP – INDICADOS E NÃO INDICADOS A BOLSA EM 2022')
            fig = px.box(data_frame=df[['IDA', 'INDICADO_BOLSA']], x='INDICADO_BOLSA', y='IDA')

            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800,
                height = 550,
            )
            st.plotly_chart(fig)
            
            st.divider()

            st.write('ANÁLISE IDA E IPP DOS INDICADOS A BOLSA POR FASE')
            st.write('Barra e linha -> barra quantidade e média por linha')
            st.write('x -> fase')

            fig = px.bar(df_grouped_by_categoria_bolsa, x='categoria_bolsa', y='ANO_PESQUISA')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )

            st.plotly_chart(fig)

            st.divider()
            st.subheader('Indicado por IPP')

            fig = px.box(data_frame=df[['IPP', 'INDICADO_BOLSA']], x='INDICADO_BOLSA', y='IPP')

            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800,
                height = 550,
            )

            st.plotly_chart(fig)

            st.divider()
            st.subheader('')
            df_per_fase = df.loc[(df['INDICADO_BOLSA'] == 'Sim')]
            df_per_fase['FASE'] = df_per_fase['FASE'].astype(int)
            df_grouped_per_fase = df[['FASE', 'INDICADO_BOLSA']]
            fig = px.bar(data_frame=df_grouped_per_fase, x='FASE', y='FASE')

            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800,
                height = 400,
            )

            st.plotly_chart(fig)

            st.divider()
            st.subheader('Indicado a bolsa por fase')
            fig = px.bar(data_frame=df_grouped_per_fase, x='FASE', y='FASE', color='INDICADO_BOLSA')

            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800,
                height = 400,
            )
            st.plotly_chart(fig)

            st.divider()

            st.subheader('Correção menor')

            df_filtrado = df_final_tratado[['NIVEL_IDEAL', 'PONTO_VIRADA',
                                            'INDE', 'IEG', 'IDA', 'IPV', 'IAA', 
                                            'IPS', 'IPP', 'IAN', 'BOLSISTA_GERAL', 
                                            'ANOS_COMO_ALUNO']]
            correlation_matrix = df_filtrado.corr().round(2)

            fig, ax = plt.subplots(figsize=(15,10))
            sns.heatmap(data=correlation_matrix, annot=True, linewidths=.5, ax=ax)
            st.pyplot(fig)

            st.write('''
                    
                    Adicionar algum texto nessa parte - senão retirar

            ''')

            st.divider()

            # st.subheader('Histograma resumido')

            # fig, ax = plt.subplots(figsize=(15,10))
            # df_filtrado.hist(bins=100, figsize=(12, 12), ax=ax)
            # st.pyplot(fig)

            # st.divider()

            st.header('Análise dos indicadores dos alunos por fase e status de bolsista')
            st.write('''
                    
                    Para aprofundar, analisamos como ocorria a progressão das principais métricas ao longo das fases por\
                    cada perfil de aluno (bolsista ou não).
                    
                    No geral, o aluno bolsista tende a ter uma nota mais alta ao longo das fases do que não bolsistas. \
                    Em alguns casos, a variação entre as médias é expressiva. Outro ponto que chama atenção é que enquanto\
                    as notas dos bolsistas se mantem mais estáveis ao longo das fases, a média de não bolsistas caso \
                    principalmente entre as fases 2 e 6.

                    Esse comportamento acontece principalmente nas métricas INDE, IEG, IDA e em menor proporção em IPV.

            ''')

            st.subheader('Média de INDE por Fase e Status de Bolsista')

            media_anos_por_bolsista = df_filtrado.groupby('BOLSISTA_GERAL')['ANOS_COMO_ALUNO'].mean()
            fig = plt.figure(figsize=(20, 10))
            sns.boxplot(x='FASE', y='INDE', hue='BOLSISTA_GERAL', data=df_final_tratado, palette='Paired')
            # plt.title('Média de INDE por Fase e Status de Bolsista')
            plt.xlabel('Fase')
            plt.ylabel('Média de INDE')
            plt.legend(title='Bolsista', labels=['Não', 'Sim'])
            st.pyplot(fig)

            st.divider()
            st.subheader('Média de IEG por Fase e Status de Bolsista')

            fig = plt.figure(figsize=(20, 10))
            sns.boxplot(x='FASE', y='IEG', hue='BOLSISTA_GERAL', data=df_final_tratado, palette='Paired')
            # plt.title('Média de IEG por Fase e Status de Bolsista')
            plt.xlabel('Fase')
            plt.ylabel('Média de IEG')
            plt.legend(title='Bolsista', labels=['Não', 'Sim'])
            st.pyplot(fig)

            st.divider()
            st.subheader('Média de IPV por Fase e Status de Bolsista')

            fig = plt.figure(figsize=(20, 10))
            sns.boxplot(x='FASE', y='IPV', hue='BOLSISTA_GERAL', data=df_final_tratado, palette='Paired')
            # plt.title('Média de IPV por Fase e Status de Bolsista')
            plt.xlabel('Fase')
            plt.ylabel('Média de IPV')
            plt.legend(title='Bolsista', labels=['Não', 'Sim'])
            st.pyplot(fig)

            st.divider()
            st.subheader('Média de IPS por Fase e Status de Bolsista')

            fig = plt.figure(figsize=(20, 10))
            sns.boxplot(x='FASE', y='IPS', hue='BOLSISTA_GERAL', data=df_final_tratado, palette='Paired')
            # plt.title('Média de IPS por Fase e Status de Bolsista')
            plt.xlabel('Fase')
            plt.ylabel('Média de IPS')
            plt.legend(title='Bolsista', labels=['Não', 'Sim'])
            st.pyplot(fig)

            st.divider()
            st.subheader('Média de IPP por Fase e Status de Bolsista')

            fig = plt.figure(figsize=(20, 10))
            sns.boxplot(x='FASE', y='IPP', hue='BOLSISTA_GERAL', data=df_final_tratado, palette='Paired')
            # plt.title('Média de IPP por Fase e Status de Bolsista')
            plt.xlabel('Fase')
            plt.ylabel('Média de IPP')
            plt.legend(title='Bolsista', labels=['Não', 'Sim'])
            st.pyplot(fig)

            # st.divider()
            # st.subheader('Avaliação Psico Bolsista')
            # avaliacao_psico_bolsista = df_final_tratado[df_final_tratado["BOLSISTA_GERAL"] == 1]
            # avaliacao_psico_bolsista = avaliacao_psico_bolsista[['INDE', 'IEG', 'IDA', 'IPV', 'IAA', 'IPS', 'IPP', 'IAN']]
            # correlation_matrix = avaliacao_psico_bolsista.corr().round(2)

            # fig, ax = plt.subplots(figsize=(25,10))
            # sns.heatmap(data=correlation_matrix, annot=True, linewidths=.5, ax=ax)
            # plt.title('avaliacao_psico_bolsista')
            # st.pyplot(fig)

            # st.divider()
            # st.subheader('Avaliação Psico sem Bolsista')
            # avaliacao_psico_n_bolsista = df_final_tratado[df_final_tratado["BOLSISTA_GERAL"] == 0]
            # avaliacao_psico_n_bolsista = avaliacao_psico_n_bolsista[['INDE', 'IEG', 'IDA', 'IPV', 'IAA', 'IPS', 'IPP', 'IAN']]
            # correlation_matrix = avaliacao_psico_n_bolsista.corr().round(2)

            # fig, ax = plt.subplots(figsize=(25,10))
            # sns.heatmap(data=correlation_matrix, annot=True, linewidths=.5, ax=ax)
            # plt.title('avaliacao_psico_n_bolsista')
            # st.pyplot(fig)

            st.divider()
            # st.subheader('Distribuição da Média de IPV por Tipo de Ponto de Virada')
            # overview = df_filtrado.groupby('PONTO_VIRADA')['IPV'].describe()
            # # sns.set(style="whitegrid")
            # fig = plt.figure(figsize=(12, 8))
            # # sns.set(style="whitegrid")
            # sns.boxplot(x='PONTO_VIRADA', y='IPV', data=df_filtrado)
            # # plt.title('Distribuição da Média de IPV por Tipo de Ponto de Virada')
            # plt.xlabel('Ponto de Virada')
            # plt.ylabel('Média de IPV')
            # st.pyplot(fig)

    with tab_modelo:
        with st.spinner('Aguardando carregamento'):
            st.header('Modelo de Classificação de alunos bolsistas')

            st.write('''
                    
                    Adicionar algum texto nessa parte - senão retirar

            ''')

            df_filtrado_2022  = get_df_ml_2022()

            df_2022_model = df_filtrado_2022.loc[df_filtrado_2022['BOLSISTA'] == 'Não']
            df_2022_model = df_2022_model[['FASE', 'TURMA', 'ANO_INGRESSO', 'BOLSISTA', 'INDE','PEDRA',
            'DESTAQUE_IEG', 'DESTAQUE_IDA', 'DESTAQUE_IPV', 'NOTA_PORT', 'NOTA_MAT', 'QTD_AVAL', 'REC_AVA_1',
            'REC_AVA_2', 'REC_AVA_3', 'REC_AVA_4', 'INDICADO_BOLSA', 'PONTO_VIRADA',
            'NIVEL_IDEAL']]
            dict_pedra = {
                "Quartzo": 1,
                "Ágata": 2,
                "Ametista": 3,
                "Topázio":4
            }
            df_2022_model['PEDRA'] = df_2022_model['PEDRA'].map(dict_pedra)
            dict_destaque_ieg = {
                "Destaque: A sua boa entrega das lições de casa.": 1,
                "Melhorar: Melhorar a sua entrega de lições de casa.": 0
            }

            dict_destaque_ida = {
                "Destaque: As suas boas notas na Passos Mágicos.": 1,
                "Melhorar: Empenhar-se mais nas aulas e avaliações.": 0
            }

            dict_destaque_ipv = {
                "Destaque: A sua boa integração aos Princípios Passos Mágicos.": 1,
                "Melhorar: Integrar-se mais aos Princípios Passos Mágicos.": 0
            }
            df_2022_model['DESTAQUE_IEG'] = df_2022_model['DESTAQUE_IEG'].map(dict_destaque_ieg)
            df_2022_model['DESTAQUE_IDA'] = df_2022_model['DESTAQUE_IDA'].map(dict_destaque_ida)
            df_2022_model['DESTAQUE_IPV'] = df_2022_model['DESTAQUE_IPV'].map(dict_destaque_ipv)

            dict_rec_ava = {
                "Alocado em Fase anterior":-1,
                "Não avaliado": 0,
                "Mantido na Fase atual": 1,
                "Mantido na Fase + Bolsa": 2,
                "Promovido de Fase": 3,
                "Promovido de Fase + Bolsa": 4
            }

            df_2022_model['REC_AVA_1'] = df_2022_model['REC_AVA_1'].fillna('Não avaliado')
            df_2022_model['REC_AVA_2'] = df_2022_model['REC_AVA_2'].fillna('Não avaliado')
            df_2022_model['REC_AVA_3'] = df_2022_model['REC_AVA_3'].fillna('Não avaliado')
            df_2022_model['REC_AVA_4'] = df_2022_model['REC_AVA_4'].fillna('Não avaliado')

            df_2022_model['REC_AVA_1'] = df_2022_model['REC_AVA_1'].map(dict_rec_ava)
            df_2022_model['REC_AVA_2'] = df_2022_model['REC_AVA_2'].map(dict_rec_ava)
            df_2022_model['REC_AVA_3'] = df_2022_model['REC_AVA_3'].map(dict_rec_ava)
            df_2022_model['REC_AVA_4'] = df_2022_model['REC_AVA_4'].map(dict_rec_ava)

            dict_indicado_bolsa = {
                "Sim": 1,
                "Não": 0
            }

            df_2022_model['INDICADO_BOLSA'] = df_2022_model['INDICADO_BOLSA'].map(dict_indicado_bolsa)
            dict_ponto_virada = {
                "Sim": 1,
                "Não": 0
            }
            df_2022_model['PONTO_VIRADA'] = df_2022_model['PONTO_VIRADA'].map(dict_ponto_virada)
            dict_nivel_ideal = {
                "ALFA  (2o e 3o ano)"       :	0.5,
                "ALFA  (2º e 3º ano)"       :	0.5,
                "Nível 1 (4o ano)"          :	1,
                "Fase 1 (4º ano)"           :	1,
                "Nível 2 (5o e 6o ano)"     :	2,
                "Fase 2 (5º e 6º ano)"      :	2,
                "Nível 3 (7o e 8o ano)"     :	3,
                "Fase 3 (7º e 8º ano)"      :	3,
                "Fase 4 (9º ano)"           :	4,
                "Nível 4 (9o ano)"          :	4,
                "Fase 5 (1º EM)"            :	5,
                "Nível 5 (1o EM)"           :	5,
                "Fase 6 (2º EM)"            :	6,
                "Nível 6 (2o EM)"           :	6,
                "Fase 7 (3º EM)"            :	7,
                "Nível 7 (3o EM)"           :	7,
                "Nível 8 (Universitários)"  :	8,
                "Fase 8 (Universitários)"   :	8
            }
            df_2022_model['NIVEL_IDEAL'] = df_2022_model['NIVEL_IDEAL'].map(dict_nivel_ideal).fillna(0).astype(float)
            df_2022_model = df_2022_model.drop(columns=['TURMA', 'BOLSISTA'])
            df_2022_model['NOTA_PORT'] = df_2022_model['NOTA_PORT'].fillna(df_2022_model['NOTA_PORT'].mean())
            df_2022_model['NOTA_MAT'] = df_2022_model['NOTA_MAT'].fillna(df_2022_model['NOTA_MAT'].mean())  

            scaler = StandardScaler()
            X = scaler.fit_transform(df_2022_model)


            km = KMeans(n_clusters=4,init='k-means++', random_state=42)

            labels = km.fit_predict(X)

            df_2022_model['labels'] = labels.astype(str)
            fig = px.scatter(df_2022_model, x='QTD_AVAL', y ='INDICADO_BOLSA', color='labels')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )
            st.plotly_chart(fig)

            X = df_2022_model[['FASE', 'ANO_INGRESSO', 'INDE', 'PEDRA', 'DESTAQUE_IEG', 'DESTAQUE_IDA',
            'DESTAQUE_IPV', 'NOTA_PORT', 'NOTA_MAT', 'QTD_AVAL', 'REC_AVA_1',
            'REC_AVA_2', 'REC_AVA_3', 'REC_AVA_4', 'PONTO_VIRADA',
            'NIVEL_IDEAL']]
            y = df_2022_model['INDICADO_BOLSA']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

            scaler = StandardScaler()
            scaler.fit(X_train)
            scaler.fit(X_test)

            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)

            df_final = get_df_final_filtrado()
            df_2022_model_v2 = df_final[['PEDRA', 'IEG', 'IDA']]
            dict_pedra = {
                "Quartzo": 1,
                "Ágata": 2,
                "Ametista": 3,
                "Topázio":4
            }
            df_2022_model_v2['PEDRA'] = df_2022_model_v2['PEDRA'].map(dict_pedra)
            dict_indicado_bolsa = {
                "Sim": 1,
                "Não": 0
            }
            #df_2022_model_v2['INDICADO_BOLSA'] = df_2022_model['INDICADO_BOLSA'].map(dict_indicado_bolsa)
            # df_2022_model_v2 = df_2022_model_v2.loc[~df_2022_model_v2['INDICADO_BOLSA'].isna()]

            fig, ax = plt.subplots(figsize=(25,10))
            st.dataframe(df_2022_model_v2)
            sns.scatterplot(data=df_2022_model_v2, x='IEG', y='IDA', hue='PEDRA', ax=ax)
            st.pyplot(fig)
            df_2022_model_v2 = df_2022_model_v2.loc[~df_2022_model_v2['PEDRA'].isna()]

            scaler = StandardScaler()
            X = scaler.fit_transform(df_2022_model_v2)
            km = KMeans(n_clusters=2,init='k-means++', random_state=42)

            labels = km.fit_predict(X)
            df_2022_model_v2['labels'] = labels.astype(str)
            fig = px.scatter(df_2022_model_v2, x='IEG', y ='IDA', color='labels')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )

            st.plotly_chart(fig)

            df_2022_model_v2['labels'] = labels.astype(str)
            fig = px.scatter(df_2022_model_v2, x='IEG', y ='IDA', color='PEDRA')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )

            st.plotly_chart(fig)

            st.divider()
            st.header('Classificação V2')

            df_final_filtrado_v2 = get_df_final_filtrado()
            df_final_filtrado_v2 = df_final_filtrado_v2.loc[df_final_filtrado_v2['PEDRA'] != "#NULO!"]
            alunos_bolsistas = df_final_filtrado_v2.loc[df_final_filtrado_v2['BOLSISTA_GERAL'] == 1]['NOME'].to_list()
            df_final_filtrado_v2 = df_final_filtrado_v2.loc[~df_final_filtrado_v2['NOME'].isin(alunos_bolsistas)]
            df_2022_model_v2 = df_final_filtrado_v2[['PEDRA', 'IEG', 'IDA']]

            dict_pedra = {
                "Quartzo": 1,
                "Ágata": 2,
                "Ametista": 3,
                "Topázio":4
            }

            df_2022_model_v2['PEDRA'] = df_2022_model_v2['PEDRA'].map(dict_pedra)
            dict_indicado_bolsa = {
                "Sim": 1,
                "Não": 0
            }
            scaler = StandardScaler()
            X = scaler.fit_transform(df_2022_model_v2)

            km = KMeans(n_clusters=2,init='k-means++', random_state=42)

            labels = km.fit_predict(X)
            df_2022_model_v2['labels'] = labels.astype(str)
            df_grouped = pd.merge(df_final_filtrado_v2, df_2022_model_v2, left_index=True, right_index=True)
            
            st.subheader('Ano de pesquisa')

            fig = px.scatter(df_grouped, x='IEG_y', y ='IDA_y', color='ANO_PESQUISA')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )
            st.plotly_chart(fig)

            st.subheader('PONTO VIRADA')
            fig = px.scatter(df_grouped, x='IEG_y', y ='IDA_y', color='PONTO_VIRADA')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )

            st.plotly_chart(fig)

            st.subheader('Clusterização')
            st.write('Previsto')

            fig = px.scatter(df_grouped, x='IEG_y', y ='IDA_y', color='labels')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )

            st.plotly_chart(fig)
            st.divider()

            st.write('Real')
            fig = px.scatter(df_grouped, x='IEG_y', y ='IDA_y', color='INDICADO_BOLSA')
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="LightSteelBlue",
                width = 800
            )
            st.plotly_chart(fig)

