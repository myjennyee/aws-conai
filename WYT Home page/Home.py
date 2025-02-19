import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="WTY",
    page_icon="🤖"
)

# Page Navigation
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Interior Image Generator", "Data Analysis", "Project Management", "000"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "18px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "font-weight": "normal", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "gray"},
        }
    )

if selected == "Interior Image Generator":
    # Container for the header
    header_container = st.container()
    with header_container:
        st.markdown('<h1 style="font-weight: normal;">WTY</h1>', unsafe_allow_html=True)
        st.markdown("---")
elif selected == "Data Analysis":
    # Container for the header
    header_container = st.container()
    with header_container:
        st.markdown('<h1 style="font-weight: normal;">WTY</h1>', unsafe_allow_html=True)
elif selected == "Project Management":
    # Container for the header
    header_container = st.container()
    with header_container:
        st.markdown('<h1 style="font-weight: normal;">WTY</h1>', unsafe_allow_html=True)
elif selected == "000":
    # Container for the header
    header_container = st.container()
    with header_container:
        st.markdown('<h1 style="font-weight: normal;">WTY</h1>', unsafe_allow_html=True)

