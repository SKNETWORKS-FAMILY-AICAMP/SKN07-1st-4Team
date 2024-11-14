import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import requests
import urllib
from urllib import parse
import pymysql
import plotly.express as px

import platform
from matplotlib import font_manager, rc


@st.cache_data
def load_data():
    con = pymysql.connect(host='192.168.0.95', user='team4', passwd='Encore_team4@', port=3306, database='team4')
    cursor = con.cursor()
    
    sql1 = "select * from nation_elec_car_charger"
    cursor.execute(sql1)
    elec_car_charger_data = cursor.fetchall()  
    elec_car_charger_df = pd.DataFrame(elec_car_charger_data)
    elec_car_charger_df.drop(columns = [0], inplace=True)
    print(elec_car_charger_df.head())

    sql2 = "select * from nation_elec_car"
    cursor.execute(sql2)
    elec_car_reg_data = cursor.fetchall()  
    elec_car_reg_df = pd.DataFrame(elec_car_reg_data)
    elec_car_reg_df.drop(columns = [0], inplace=True)
    print(elec_car_reg_df.head())

    sql3 = "select * from car_repair_shop"
    cursor.execute(sql3)
    elec_car_repair_data = cursor.fetchall()  
    elec_car_repair_df = pd.DataFrame(elec_car_repair_data)
    elec_car_repair_df.drop(columns = [0], inplace=True)
    print(elec_car_repair_df.head())

    return elec_car_charger_df, elec_car_reg_df, elec_car_repair_df

def main():

    plt.rcParams['axes.unicode_minus'] = False
    if platform.system() == 'Linux':
        rc('font', family='NanumGothic')

    elec_car_charger_df, elec_car_reg_df, elec_car_repair_df = load_data()

    question = ['지역별 충전소', '지역별 전기차 등록대수','지역별 통합','brand 별 전기차 정비소 수','전기차 등록대수', '충전기당 전기차수']

    my_choice = st.selectbox('질문을 선택하시오', question)

    st.text( '{}대한 정보입니다.'.format(my_choice) )

    if my_choice == question[0] :
        st.text('지역별 충전소 개수')

        # 서울, 인천, 경기, 강원, 제주, 충청, 전라, 경상

        elec_car_charger_df.sort_values([1], inplace=True)

        fig1 = px.bar( elec_car_charger_df, x=1, y=2)    #plotly bar차트
        fig1.update_xaxes(title_text='지역')
        fig1.update_yaxes(title_text='count')
        st.plotly_chart(fig1)
        
    elif my_choice == question[1]:

        st.text('지역별 전기차 등록대수')
        elec_region_df = elec_car_reg_df.copy()

        elec_region_df[3] = elec_region_df[1]
        elec_region_df.head(20)

        # 서울, 인천, 경기, 강원, 제주, 충청, 전라, 경상

        ex_region_maping={
        '세종':'충청',
        '울산':'경상',
        '광주':'전라',
        '대전':'충청',
        '대구':'경상',
        '부산':'경상',
        '충북':'충청',
        '충남':'충청',
        '전북':'전라',
        '전남':'전라',
        '경북':'경상',
        '경남':'경상'
        }

        elec_region_df[3] = elec_region_df[3].replace('세종', '충청')
        elec_region_df[3] = elec_region_df[3].replace('울산', '경상')
        elec_region_df[3] = elec_region_df[3].replace('광주', '전라')
        elec_region_df[3] = elec_region_df[3].replace('대전', '충청')
        elec_region_df[3] = elec_region_df[3].replace('대구', '경상')
        elec_region_df[3] = elec_region_df[3].replace('부산', '경상')

        elec_region_df[3] = elec_region_df[3].replace('충북', '충청')
        elec_region_df[3] = elec_region_df[3].replace('충남', '충청')

        elec_region_df[3] = elec_region_df[3].replace('전북', '전라')
        elec_region_df[3] = elec_region_df[3].replace('전남', '전라')


        elec_region_df[3] = elec_region_df[3].replace('경북', '경상')
        elec_region_df[3] = elec_region_df[3].replace('경남', '경상')

        elec_region_df.head(20)


        elec_car_reg_region_df= elec_region_df.groupby(3, as_index=False)[[2]].sum()
        
        print(elec_car_reg_region_df)
        fig5, ax = plt.subplots()
        
        plt.xticks(rotation=90)  
        plt.bar(elec_car_reg_region_df[3], elec_car_reg_region_df[2])        
        st.pyplot(fig5)

    elif my_choice == question[2]:
        st.text('brand 별 전기차 정비소 수')
        print(elec_car_repair_df.head())
        y_series = elec_car_repair_df.groupby(1).size()
        y_series.sort_values(inplace=True)
        print(y_series.head())

        print(y_series.info())

        # fig3 = px.bar( y_series, x=0, y=1)    #plotly bar차트
        # fig3.update_xaxes(title_text='brand')
        # fig3.update_yaxes(title_text='count')
        # st.plotly_chart(fig3)
        # fig3 = plt.plot()
        # plt.bar(y_series.index, y_series.values)
        # st.pyplot(fig3)

        fig3, ax = plt.subplots()
        # plt.figure(figsize=(6,8))
        plt.xticks(rotation=90)  
        plt.bar(y_series.index, y_series.values)        
        st.pyplot(fig3)

    elif my_choice == question[3]:
        repair_df = elec_car_repair_df.groupby(1, as_index=False)[[3]].count()
        repair_df.sort_values([3], inplace=True)
        fig4, ax = plt.subplots()
        
        plt.xticks(rotation=90)  
        plt.bar(repair_df[1], repair_df[3])        
        st.pyplot(fig4)
    elif my_choice == question[4]:
        st.text('전기차 등록대수')
        elec_car_reg_df.sort_values([2], inplace=True)
        fig2 = px.bar( elec_car_reg_df, x=1, y=2)    #plotly bar차트
        fig2.update_xaxes(title_text='지역')
        fig2.update_yaxes(title_text='count')
        st.plotly_chart(fig2)

    elif my_choice == question[5]:
        pass






if __name__ == '__main__':
    main()
