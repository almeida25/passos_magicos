import streamlit as st
import pandas as pd
from auxiliar import apply_custom_style

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
    st.set_page_config(page_title='Passos Magicos - Dashboard',
                       layout='wide')
    
    st.image('./assets/Passos-magicos-icon-cor.png')
    apply_custom_style()
    
    st.markdown("""
        <style>
            .section {
                font-family: 'Sans-serif';
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            .indicator {
                margin-left: 20px;
                font-size: 16px;
                font-weight: normal;
            }
        </style>
    """, unsafe_allow_html=True)
    # st.header('Passos Mágicos - Avaliação')

    # st.subheader('A ONG Passos Magicos busca ajudar jovens vulneraiveis \
    #              a terem acesso a educação. ')
    
    st.title('🌍 Quem Somos')
    st.divider()

    st.subheader('Nossa história')
    st.write('''
            A Associação Passos Mágicos tem uma trajetória de 30 anos de atuação, \
            trabalhando na transformação da vida de crianças e jovens de baixa renda os levando a \
            melhores oportunidades de vida.

            A transformação, idealizada por Michelle Flues e Dimetri Ivanoff, começou em 1992,\
            atuando dentro de orfanatos, no município de Embu-Guaçu.

            Em 2016, depois de anos de atuação, decidem ampliar o programa para que mais jovens \
            tivessem acesso a essa fórmula mágica para transformação que inclui: educação de qualidade, \
            auxílio psicológico/psicopedagógico, ampliação de sua visão de mundo e protagonismo.\
            Passaram então a atuar como um projeto social e educacional, criando assim a Associação Passos Mágicos.
    ''')
    
    st.write('---')

    st.subheader('O que fazemos?')
    st.write('Oferecemos um programa de educação de qualidade para crianças e jovens do município de Embu-Guaçu.')

    st.markdown('<div class="section">Aceleração de conehecimento</div>', unsafe_allow_html=True)
    st.write('Educação de qualidade, programas educacionais, \
             assistência psicológica e ampliação da visão de mundo. ')
    
    st.markdown('<div class="section">Programas Especiais</div>', unsafe_allow_html=True)
    st.write('Projeto de apadrinhamento e de intercâmbio, visando uma maior integração dos\
              alunos com diferentes ambientes e culturas. ')
    
    st.markdown('<div class="section">Eventos e Ações Sociais</div>', unsafe_allow_html=True)
    st.write('Anualmente, em prol dos alunos, são promovidas campanhas de arrecadação para presentear \
             as centenas de crianças e adolescentes Passos Mágicos.')
    
    st.divider()

    st.subheader('Missão e Valores')
    st.write('''
        Nossa missão é transformar a vida de jovens e crianças, oferecendo ferramentas para levá-los \
        a melhores oportunidades de vida.

        Nossa visão é viver em um Brasil no qual todas as crianças e jovens têm iguais oportunidades \
        para realizarem seus sonhos e são agentes transformadores de suas próprias vidas.
    ''')


    