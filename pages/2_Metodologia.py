import streamlit as st
import pandas as pd

if __name__ == '__main__':
    st.header('Dimensões educacionais')
    # Adicionando estilos CSS
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

    # Conteúdo do relatório com formatação HTML
    st.write('A fim de avaliar os alunos e identificar o seu desenvolvimento é utilizado o INDE \
             (Indice de desenvolvimento educacional) onde é composto por algumas dimensões')
    st.write('Essas são as 3 dimensões das quais a ONG utiliza:')
    st.write('Cada dimensão é composta por alguns indicadores.')
    st.markdown('<div class="section">1. Dimensão acadêmica</div>', unsafe_allow_html=True)
    
    st.write('- IAN: Indicador de Adequação ao nível')
    st.write('- IDA: Indicador de Desempenho Acadêmico')
    st.write('- IEG: Indicador de Engajamento')

    st.markdown('<div class="section">2. Dimensão psicossocial</div>', unsafe_allow_html=True)
    st.write('- IAA: Indicador de Autoavaliação')
    st.write('- IPS: Indicador de Psicossocial')

    st.markdown('<div class="section">3. Dimensão psicopedagógica</div>', unsafe_allow_html=True)
    st.write('- IAA: Indicador de Psicopedagógico')
    st.write('- IPS: Indicador de Ponto de Virada')

    st.write('---')

    st.markdown('<div class="section">Os Alunos e Suas Fases Educativas:</div>', unsafe_allow_html=True)
    st.write('Na jornada educacional, os alunos atravessam várias fases, \
             cada uma contribuindo para seu desenvolvimento acadêmico e pessoal. \
             Essas fases são organizadas de acordo com o seu ano escolar,\
             representando marcos significativos em sua progressão educacional.')

    st.write('Abaixo a tabela equipara os anos dos alunos com a identificação de\
             fases dada pela Passos Mágicos')
    df_fase = {
        'Ano Escolar': ['1º e 2º ano', '3º e 4º ano', '5º e 6º ano', 
                        '7º e 8º ano', '9º ano', '1º EM', '2º EM', '3º EM', 'Universidade'],
        'Fases Passos Mágicos': ['Alfa', 'Fase 1', 'Fase 2', 'Fase 3', 'Fase 4',
                                    'Fase 5', 'Fase 6', 'Fase 7', 'Fase 8']
    }

    st.dataframe(pd.DataFrame(df_fase))

    st.divider()

    st.markdown('<div class="section">Pedras conceito</div>', unsafe_allow_html=True)
    st.write('''Aplicando os critérios de padronização das notas do INDE, \
              identificamos limites que dividem o desempenho em quatro faixas distintas. \
              Essas faixas resultam nas Pedras-conceito INDE, representando marcos \
              significativos em nossa avaliação educacional. Assim como nas fases do ano \
              escolar e nos Passos Mágicos, essas Pedras-conceito INDE oferecem uma \
              estrutura clara e progressiva para orientar o progresso dos alunos e garantir seu sucesso educacional.''')
    

    df_pedras = {
        'Pedra': ['Quartzo', 'Ágata', 'Ametista', 'Topázio'],
        'Faixa': ['6,0 - 6,6', '6,7 - 7,4', '']
    }
    quartzo_min = 6.047
    quartzo_max = 6.663
    agata_min = 6.663
    agata_max = 7.437
    ametista_min = 7.437
    ametista_max = 8.241
    topazio_min = 8.241
    topazio_max = 9.427

    st.write("Os valores abaixo representam os limites em cada pedra-conceito:")

    # Visualização dos intervalos
    st.write("Quartzo: {} - {}".format(quartzo_min, quartzo_max))
    st.write("Ágata: {} - {}".format(agata_min, agata_max))
    st.write("Ametista: {} - {}".format(ametista_min, ametista_max))
    st.write("Topázio: {} - {}".format(topazio_min, topazio_max))

    # st.write("Os valores abaixo representam a distribuição dos alunos em cada pedra-conceito:")
    # st.write("Quartzo: Entre 6,047 e 6,663")
    # st.write("Ágata: Entre 6,663 e 7,437")
    # st.write("Ametista: Entre 7,437 e 8,241")
    # st.write("Topázio: Entre 8,241 e 9,427")