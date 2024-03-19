import streamlit as st
import pandas as pd
import plotly.express as px


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


if __name__ == '__main__':

    st.title('📈 Análise')
    st.divider()

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

