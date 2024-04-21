import streamlit as st
import pandas as pd

pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(
    page_title="Кофе Шоп-н Борлуулалтын Дашбоард",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

st.header("Кофе Шоп-н Борлуулалтын Дашбоард")

# -------------------

st.subheader("Кофе шопны тухай")

col1, col2 = st.columns((10,20))

with col1:
    st.image("./assets/image.jpg")
with col2:
    st.markdown("Welcome to our humble corner of the internet, where stories brew, dreams take flight, and the aroma of freshly brewed coffee fills the air.\
                It all began with Sarah's unwavering passion for coffee and her deep-rooted desire to create a space where people could come together, connect, and find solace in the simple pleasures of life. With boundless enthusiasm and a sprinkle of magic, Sarah opened the doors to her first coffee shop—a cozy haven adorned with twinkling fairy lights and adorned with rustic charm.\
                From the moment Sarah poured her first cup of coffee, she poured her heart and soul into every aspect of her business. Each bean was carefully selected, each brew meticulously crafted, and every interaction infused with warmth and hospitality. Word of Sarah's delightful concoctions and genuine kindness spread like wildfire, drawing in locals and travelers alike.\
                As the days turned into weeks and months, Sarah's coffee shop became more than just a place to grab a caffeine fix—it became a beloved gathering spot where friendships blossomed, stories were shared, and memories were made.")

col1, col2 = st.columns((15,15))
with col1:
    st.markdown("With meticulous planning and unwavering determination, Sarah opened two more branches in neighboring communities, each one infused with the same warmth, charm, and sense of belonging that had made her original coffee shop so beloved.\
                From hosting charity events to supporting local artists and musicians, Sarah's coffee shops became more than just places to grab a cup of coffee—they became pillars of support, kindness, and connection in the communities they served.\
                So come, join us at our table, and be part of our story—a story of love, laughter, and the boundless possibilities that unfold when we dare to chase our dreams. Welcome to our coffee family—where every cup tells a story, and every sip brings us closer together.")
with col2:
    st.image("./assets/coffee_shop.jpeg")
    
# -------------------

st.subheader("Кофе-ий урлагт суралцацгаая!")

with st.expander("Coffee-ий төрлүүдийн тухай дэлгэрэнгүй харах"):

    col1, col2, col3 = st.columns((10,10,10))
    with col1:
        with st.container(height=200, border=False):
            st.write("Espresso")

        with st.container(height=200, border=False):
            st.write("Americano")
    
    with col2:
        with st.container(height=200, border=False):
            st.write("Espresso image")
        
        with st.container(height=200, border=False):
            st.write("Espresso image")
    
    with col3:
        with st.container(height=200, border=False):
            st.write("Espresso explanation")
        
        with st.container(height=200, border=False):
            st.write("Espresso explanation")

# -------------------