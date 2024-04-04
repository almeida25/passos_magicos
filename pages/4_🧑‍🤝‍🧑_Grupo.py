import streamlit as st

from auxiliar import apply_custom_style 

if __name__ == '__main__':
        apply_custom_style()
        st.title('Sobre')
        st.subheader('Projeto desenvolvido por Estudantes da FIAP - Pós Tech em Data Analytics.')

        st.subheader('Github')
        st.write('https://github.com/almeida25/passos_magicos')

        st.subheader('Membros')
        st.markdown("<li>Barbara Campos</li> \
                <li>Brendon Calazans</li>\
                <li>Carlos Eduardo</li> \
                <li>Gabriel Rosa</li>", unsafe_allow_html=True)
