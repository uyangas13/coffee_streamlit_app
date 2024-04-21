import pandas as pd
import numpy as np
import json
import os
import streamlit as st

import altair as alt


color_dict = {'sky_blue':'rgb(52,144,218)','sky_blue2':'rgb(130,230,240)','light_teal':'rgb(79,195,222)',
               'blue':'rgb(0,61,135)','blue1':'rgb(52,144,218)', 'blue2':'rgb(2,61,114)','blue3':'rgb(0,61,135)',
              'powder_blue':'rgb(150,222,228)',
               'teal':'rgb(0,150,150)','teal2':'rgb(0,140,160)','teal3':'rgb(0,141,154)','dark_teal':'rgb(0,103,120)',
               'dark_green':'rgb(52,144,128)','forest_green':'rgb(0,130,60)',
               'aqua':'rgb(0,214,219)','torq':'rgb(0,189,202)', 'torq2':'rgb(0,191,195)','light_torq':'rgb(93,222,215)',
               'light_orange':'rgb(255,197,0)','orange':'rgb(255,181,0)','orange2':'rgb(255,166,0)','blood_orange':'rgb(255,119,0)','dark_orange':'rgb(198,112,1)','brown':'rgb(105,49,0)',
               'gray':'rgb(130,130,130)', 'light_gray':'rgb(160,160,160)','light_gray2':'rgb(180,180,180)','light_gray3':'rgb(210,210,210)',
               'empty':'rgba(0,0,0,0)','background':'rgba(239,239,239,239)', 'white':'rgb(255,255,255)',
              'light_red':'rgb(255,134,134)','red_orange':'rgb(233,74,0)'
              }


with open(os.path.join("./Data", "location.json"), 'r') as f:
    branch_location = json.load(f)


def process_data(df, extend_cols=None):
    # convert date to YYYY-MM-DD format
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], format="YYYY-MM-DD")

    if extend_cols:
        df['sales'] = df['unit_price']*df['transaction_qty']
        # extract date time variables
        df['year'] = df['transaction_date'].dt.year
        df['month'] = df['transaction_date'].dt.month
        df['day'] = df['transaction_date'].dt.day
        df['dayofweek'] = df['transaction_date'].dt.day_name()
        df['dayofweek_numbered'] = df['dayofweek'].replace({'Monday':'01_Mon','Tuesday':'02_Tue','Wednesday':'03_Wed',
                                                    'Thursday':'04_Thu','Friday':'05_Fri','Saturday':'06_Sat','Sunday':'07_Sun'})
        df['monthname'] = df['transaction_date'].dt.month_name()
        df['monthname_numbered'] = df['monthname'].replace({'January':'01_Jan','February':'02_Feb','March':'03_Mar',
                                                   'April':'04_Apr', 'May':'05_May','June':'06_June',
                                                   'July':'07_Jul','August':'08_Aug','September':'09_Sep',
                                                   'October':'10_Oct','November':'11_Nov','December':'12_Dec'})

        # convert the transaction time to H-M-S format
        df['transaction_time'] = pd.to_datetime(df['transaction_time'], format="%H:%M:%S")

        # extract hour, minute
        df['hour'] = df['transaction_time'].dt.hour
        df['minute'] = df['transaction_time'].dt.minute
        df['hour'] = df['hour'].astype('int')
        df['minute'] = df['minute'].astype('int')

        # create timeofday variable
        df['timeofday'] = ""
        df['timeofday'][(df['hour']>=5)&(df['hour']<=11)] = "morning"
        df['timeofday'][(df['hour']>11)&(df['hour']<=13)] = "lunch"
        df['timeofday'][(df['hour']>13)&(df['hour']<=18)] = "afternoon"
        df['timeofday'][(df['hour']>18)&(df['hour']<=20)] = "dinner"
        df['timeofday'][(df['hour']>20)&(df['hour']<=24)] = "evening"
        df['timeofday'][(df['hour']>0)&(df['hour']<5)] = "night"

        # add branch locations
        df['Latitude'] = [branch_location[loc][0] for loc in df['store_location']]
        df['Longitude'] = [branch_location[loc][1] for loc in df['store_location']]
        df['Latitude'] = df['Latitude'].astype('float')
        df['Longitude'] = df['Longitude'].astype('float')
        
    else:
        # convert the transaction time to H-M-S format
        df['transaction_time'] = pd.to_datetime(df['transaction_time'], format="%H:%M:%S").dt.time

    return df


def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'$ {num // 1000000} M'
        return f'$ {round(num / 1000000, 1)} M'
    return f'$ {num // 1000} K'


def sidebar_filter(df, month, product_category):

    product_category_list = ['All']
    product_category_list.extend(list(df['product_category'].unique()))
    month_list = ["All"]
    month_list.extend(list(df['monthname'].unique()))
    
    if ((len(month)==1) & (month[0]=='All')) & ((len(product_category)==1)&(product_category[0]=='All')):
        monthly_value = df
    elif ((len(month)==1) & (month[0]=='All')) & ('All' not in product_category):
        monthly_value = df[df['product_category'].isin(product_category)]
    elif ('All' not in month) & ((len(product_category)==1)&(product_category[0]=='All')):
        monthly_value = df[(df['monthname'].isin(month))]
    elif ('All' not in month) & ('All' not in product_category):
        monthly_value = df[(df['monthname'].isin(month))&(df['product_category'].isin(product_category))]

    return monthly_value


def alt_make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#4D9CFF', '#004EAF']
  if input_color == 'green':
      chart_color = ['#5CE2F2', '#009CAF']
    
  source = pd.DataFrame({
      "Үзүүлэлт": ['', input_text],
      "Хувь": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Үзүүлэлт": ['', input_text],
      "Хувь": [100, 0]
  })
    
  chart = alt.Chart(source).mark_arc(innerRadius=42, 
                                    cornerRadius=25).encode(
      theta="Хувь",
      color= alt.Color("Үзүүлэлт:N",
                       scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=150, height=150)
      
  text = chart.mark_text(align='center',
                        color="#29b5e8",
                        fontSize=25,
                        fontWeight=300,
                        ).encode(text=alt.value(f'{input_response} %'))
  
  chart_bg = alt.Chart(source_bg).mark_arc(innerRadius=42, 
                                          cornerRadius=20).encode(
      theta="Хувь",
      color= alt.Color("Үзүүлэлт:N",
                      scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=150, height=150)

  return chart_bg + chart + text



def alt_line_chart(df, 
                   x_axis=None,
                   agg_col=None,
                   x_title=None,
                   y_title=None,
                   color='blue',
                   lollipop=False):

    if not lollipop:
        chart = alt.Chart(df[[x_axis,agg_col]],
                        height=300,
                        width=600)\
        .mark_line(point=True, 
                strokeWidth=3,
                color=color)\
        .encode(
            x=alt.X(f'{x_axis}:N',
                    axis=alt.Axis(title=x_title)),
            y=alt.Y('sum_qty:Q',
                    axis=alt.Axis(title=y_title)),
            tooltip=alt.Tooltip('sum_qty:Q', format=",.2f")
        ).transform_aggregate(
            sum_qty=f'sum({agg_col})',
            groupby=['monthname_numbered']
        ).configure_point(
            size=150,
            color=color
        )

        return chart

    else:
        bar_chart = alt.Chart(df[[x_axis,agg_col]],
                        height=300,
                        width=600).mark_bar(size=5, color=color).encode(
                            x=alt.X(f'{x_axis}:N', axis=alt.Axis(title=x_title)),
                            y=alt.Y('sum_qty:Q',
                                    axis=alt.Axis(title=y_title)),
                                    tooltip=alt.Tooltip('sum_qty:Q', format=",.2f")
                                    ).transform_aggregate(
                                        sum_qty=f'sum({agg_col})',
                                        groupby=['monthname_numbered']
                                    )
        
        circle_chart = alt.Chart(df[[x_axis,agg_col]],
                        height=300,
                        width=600).mark_point(filled=True, size=150, color=color).encode(
                            x=alt.X(f'{x_axis}:N', axis=alt.Axis(title=x_title)),
                            y=alt.Y('sum_qty:Q',
                                    axis=alt.Axis(title=y_title),
                                    impute=alt.ImputeParams(value=None)),
                                    tooltip=alt.Tooltip('sum_qty:Q', format=",.2f")
                                    ).transform_aggregate(
                                        sum_qty=f'sum({agg_col})',
                                        groupby=['monthname_numbered']
                                    )
        
        return bar_chart+circle_chart