import streamlit as st

st.set_page_config(
    page_title="Tornado Project", 
    page_icon="🌪️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

left_col, right_col = st.columns(2)

left_col.markdown("# Tornado Project")
left_col.markdown("### Visualize Tornado data")

right_col.markdown("![Tornado image](https://media.tenor.com/DObIxX3C-qkAAAAM/tornado-animaniacs.gif)")

st.write('''## 🤔 How to use?''')

st.write('''- On the side bar choose the "Explore" page.''')
st.write('''- After which you will view visualizations for States.''')
st.write('''- Explore different filters by choosing them.''')
st.write('''- Fiddle around with the remaining filters to view the respective visualizations!''')

st.write('''## ℹ️  Extra Information?''')

st.write('''This page contains details about the origin of the data we use, what cleaning we have performed in the data, the methodologies we used to visualize the data.''')

footer="""
            <style>
                a:link , a:visited{
                color: white;
                background-color: transparent;
                }

                a:hover,  a:active {
                color: red;
                background-color: transparent;
                text-decoration: underline;
                }

                .footer {
                position: fixed;
                left: 1;
                bottom: 0;
                width: 100%;
                background-color: transparent;
                color: white;
                text-align: left;
                }
            </style>
            <div class="footer">
                <p>Developed with ❤️ by <a href="https://www.linkedin.com/in/sai-pranam-reddy-chillakuru/" target="_blank">Pranam</a>, <a href="https://www.linkedin.com/in/thomas-reedy-151363190/" target="_blank">Thomas</a>, <a href="https://www.linkedin.com/in/vigneshwarravirao/" target="_blank">Viki</a>, & <a href="https://www.linkedin.com/in/yashpatel2952/" target="_blank">Yash</a></p>
            </div>
        """
st.markdown(footer,unsafe_allow_html=True)