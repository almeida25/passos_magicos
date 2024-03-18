import streamlit as st
import pandas as pd

def read_dataset():
    df = pd.read_csv('PEDE_PASSOS_DATASET_FIAP.csv', header=0, sep=';')
    return df

def read_final_dataset():
    df = pd.read_csv('df_final_passos.csv', header=0, sep=',')
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


if __name__ == '__main__':

    st.subheader('Banco de dados')
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

    st.markdown('<h4>Dashboard</h4>', unsafe_allow_html=True)

    indicators = ('IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN')
    select_ind = st.multiselect('Indicadores', indicators)

    years = (2020, 2021, 2022)
    select_year = st.multiselect('Ano', years)
    
    st.metric('Média', 8)
    st.metric('Aumento %', 12)
    
    st.write('DF FINAL')
    df_final_pm = read_final_dataset()
    st.write(df_final_pm.columns)
    df_filtered = get_df_indicators(df_final_pm, select_ind, select_year)

    st.write(df_filtered)