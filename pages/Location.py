import streamlit as st
import pandas as pd
import os
import json
import sys

import altair as alt

import pydeck as pdk

# ---------------------

from utils.utils import process_data, color_dict, format_number, alt_make_donut, alt_line_chart, sidebar_filter

pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(
    page_title="Кофе Шоп-н Борлуулалтын Дашбоард",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="collapsed")

alt.themes.enable("dark")

color_names = ['aqua','torq', 'teal','powder_blue','blue1','blue3', 'forest_green','light_orange','light_gray','blood_orange']
color_hex = ["#00C4A6", "#00EACD","#00CFE7","#008696","#006996","#005194","#FFCD00","#FF8000","#B0B0B0"]

# ---------------------

# өгөгдлийг оруулж ирэх ба боловсруулах
@st.cache_data
def load_data(extend_cols):
    df = pd.read_excel(os.path.join("./Data", "Coffee Shop Sales.xlsx"))
    df = process_data(df, extend_cols=extend_cols)

    return df

coffee_df = load_data(extend_cols=True)

product_list = ['All']
product_list.extend(list(coffee_df['product_category'].unique()))
month_list = ["All"]
month_list.extend(list(coffee_df['monthname'].unique()))

branch_list = ['All']
branch_list.extend(list(coffee_df['store_location'].unique()))

# ---------------------

st.header("Кофе Шоп-н Борлуулалтын Дашбоард")

# >>> Sidebar үүсгэх
with st.sidebar:
    st.title("Дашбоардын удирдлага")
    month = st.multiselect(
        "Тайлагнах сар",
        month_list,
        default=month_list[0]
        )

    product_category = st.multiselect(
        "Бүтээгдэхүүний төрөл",
        product_list,
        default=product_list[0]
        )

    branch_radio = st.radio("Байршил",
                            branch_list)
    
    if branch_radio=='All':
        branch_selected = branch_list[1:]
    else:
        branch_selected = [branch_radio]
        
col1, col2, col3 = st.columns((15,20,15))
   
with col1:
    st.markdown("#### Борлуулалт, салбараар")
    st.markdown("Тухайн сар, бүтээгдэхүүний хувьд, '000")
    
    monthly_loc_sales_df = sidebar_filter(coffee_df, month, product_category)\
        .groupby(['store_location','Longitude','Latitude'])\
        .agg({'sales':'sum'}).reset_index()\
        .assign(sales=lambda x: round(x['sales']/1000,2))
        
        
    pie = alt.Chart(monthly_loc_sales_df)\
        .mark_arc(innerRadius=50)\
        .encode(
            theta=alt.Theta('sales:Q').stack(True),
            radius=alt.Radius('sales'),
            color=alt.Color("store_location", legend=None).scale(range=color_hex)
        )
    
    chart = pie\
        +pie.mark_text(radiusOffset=15, 
                        fontSize=12, 
                        color="#FFFFFF"
                        ).encode(text=alt.Text('sales:Q',format="$.0f"))\
        +pie.mark_text(radiusOffset=40, 
                        fontSize=12, 
                        color="#FFFFFF"
                        ).encode(text=alt.Text('store_location:N'))

    st.altair_chart(chart.properties(height=250))
    
    
    st.markdown("#### Борлуулалт")
    st.markdown("Тухайн сар, бүтээгдэхүүний хувьд")
    
    layer = pdk.Layer(
        'ColumnLayer',
        data=monthly_loc_sales_df,
        get_position='[Longitude, Latitude]',
        get_elevation=['sales'],
        elevation_scale=10,
        get_radius=10,
        get_fill_color=[0,156,175],
        auto_highlight=True,
        coverage=0.1,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=40.743521,
        longitude=-73.990896,
        zoom=12,
        pitch=45
    )

    r = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html":"<b>Branch: </b> {store_location} <br> <b> Total sales: </b> ${sales}",
            "style":{"color":"white"}
        }
    )

    st.pydeck_chart(r)
            
with col2:
    st.markdown("#### Борлуулалт, цагаар")
    st.markdown("Тухайн сар, бүтээгдэхүүний хувьд")
    
    product_sales = sidebar_filter(coffee_df, month, product_category)
    product_sales = product_sales[product_sales['store_location'].isin(branch_selected)]\
        .groupby(['product_type','hour']).agg({'sales':'sum'}).reset_index()\
        .assign(sales = lambda x: round(x['sales'],2))\
        .assign(hour = lambda x: round(x['hour']))
        
    chart = alt.Chart(product_sales)\
        .mark_rect()\
        .encode(
            x=alt.X('hour:Q', bin=alt.BinParams(maxbins=24), title="Цаг"),
            y=alt.Y('product_type:N', title="Бүтээгдэхүүн"),
            color=alt.Color('sales:Q', scale=alt.Scale(scheme='greenblue'))
        )\
            .properties(width=500)
    st.altair_chart(chart)
    
    
with col3:
    st.markdown("#### Бүтээгдэхүүний төрөл")
    st.markdown("Хамгийн өндөр борлуулалттай")
    
    product_sales = sidebar_filter(coffee_df, month, product_category)
    product_sales = product_sales[product_sales['store_location'].isin(branch_selected)]\
        .groupby('product_type').agg({'sales':'sum'}).reset_index()

    chart = alt.Chart(product_sales).mark_bar(color="#163356").encode(
        x=alt.X('sales:Q', title="Борлуулалт ($)"),
        y=alt.Y('product_type:N', title="Бүтээгдэхүүний нэр").sort('-x')
    ).properties(
        height=700
    )

    st.altair_chart(chart)