import streamlit as st
import pandas as pd

PRIMARY_COLOR = "#41c4f0"
SECOND_COLOR = "#41aaf0"

def apply_custom_style():
    st_custom_style = """
                <style>
                summary {
                    display: none;
                }
                h2 {
                    color: {prim-color};
                }
                header[data-testid="stHeader"] {
                    background-image: linear-gradient({prim-color}, {prim-color}, {prim-color});
                }
                div[data-testid="stStatusWidget"] div div div svg{
                    color: white;
                }
                #relat-rio-de-exporta-o-de-vinhos, #tabela-resumida-com-informa-es-de-exporta-es-nos-ltimos-anos{
                    text-align:center;
                }
                div[data-testid="stStatusWidget"] img{
                    opacity: 100%;
                }
                div[data-testid="stStatusWidget"] label{
                    color: white;
                }
                div[data-testid="stStatusWidget"] button{
                    color: white;
                    background: #9e829b;
                    border-radius: 20px;
                }
                #MainMenu{
                    color: white;
                    visibility: hidden;
                }
                * {
                  -webkit-user-drag: none;
                  -khtml-user-drag: none;
                  -moz-user-drag: none;
                  -o-user-drag: none;
                  user-drag: none;
                }
                a[href="#hide"] {
                    visibility: hidden;
                }
                div[data-testid="stDecoration"] {
                    background-image: none;
                    background-color: black;
                }
                section>div.block-container {
                    padding-top: 60px;
                }
                thead tr th:first-child {
                    display:none
                }
                tbody th {
                    display:none
                }
                .stAlert a {
                    display: none;
                }
                button[role="tab"][aria-selected="true"] {
                    background: #9e829b;
                    padding: 4px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    color: white;
                }
                div[data-testid="collapsedControl"] {
                    color: white;
                }
                [tabindex="0"] > * {
                
                    max-width: 86rem !important;
                }
                #grupo {
                    background: #9e829b;
                    padding: 15px;
                    border-radius: 10px;
                }
                </style>
                """.replace('{prim-color}', PRIMARY_COLOR)
    st_custom_style.replace('{second-color}', SECOND_COLOR)

    st.markdown(st_custom_style, unsafe_allow_html=True)

# função para validar quais colunas não estão presentes no dataframe e adiciona
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