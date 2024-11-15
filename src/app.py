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
import pickle

@st.cache_data
def load_pickle():
    with open("./data/charge_car_ratio.pkl" , "rb") as f:
        charge_car_ratio  = pickle.load(f)

    with open("./data/car_region.pkl" , "rb") as f:
        car_region  = pickle.load(f)

    with open("./data/car_charge.pkl" , "rb") as f:
        car_charge  = pickle.load(f)

    with open("./data/car_repairshop.pkl" , "rb") as f:
        car_repairshop  = pickle.load(f)

    with open("./data/result_car_charge.pkl" , "rb") as f:
        result_car_charge  = pickle.load(f)

    return charge_car_ratio, car_region, car_charge, car_repairshop, result_car_charge


@st.cache_data
def load_data():
    con = pymysql.connect(host='192.168.0.95', user='team4', passwd='', port=3306, database='team4')
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

    charge_car_ratio, car_region, car_charge, car_repairshop, result_car_charge = load_pickle()

    print(charge_car_ratio.head(10))

    question = ['지역별 충전소', '지역별 전기차 등록대수','지역별 차충기', '지역별 정비소','brand 별 전기차 정비소 수']

    my_choice = st.selectbox('차트를 선택하시오', question)

    st.text( '{} 대한 정보입니다.'.format(my_choice) )

    if my_choice == question[0] :
        # st.text('지역별 충전소 개수')

        # 서울, 인천, 경기, 강원, 제주, 충청, 전라, 경상

        elec_car_charger_df.sort_values([1], inplace=True)

        fig1 = px.bar( elec_car_charger_df, x=1, y=2)    #plotly bar차트
        fig1.update_xaxes(title_text='지역')
        fig1.update_yaxes(title_text='count')
        st.plotly_chart(fig1)
        
    elif my_choice == question[1]:

        # st.text('지역별 전기차 등록대수')
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
        
        # plt.xticks(rotation=90)  
        plt.bar( elec_car_reg_region_df[3], elec_car_reg_region_df[2], color='green')        
        st.pyplot(fig5)

    
    elif my_choice == question[2]:
        fig5, ax = plt.subplots()

        print(charge_car_ratio.sort_values(['region'], inplace=True))

        plt.title('지역별 차충기')
        xs=charge_car_ratio['region'].to_list()
        ys=charge_car_ratio['ratio'].to_list()

        plt.xlabel('Region')
        plt.ylabel('Count')
        
        plt.bar(xs, ys, width=0.6, color='#ffc000')
        st.pyplot(fig5)

        st.text('충전기 1대당 전기차 대수를 의미하는 것을 [차충비] 라고 한다.')

    elif my_choice == question[3]:
        # st.text('brand 별 전기차 정비소 수')

        print(car_repairshop.head())
        fig6, ax = plt.subplots()
        
        # plt.xticks(rotation=90)  
        plt.bar(car_repairshop['지역'], car_repairshop['정비소'], color='cyan')        
        st.pyplot(fig6)

    elif my_choice == question[4]:
        # st.text('brand 별 전기차 정비소 수')

        repair_df = elec_car_repair_df.groupby(1, as_index=False)[[3]].count()
        repair_df.sort_values([3], inplace=True)
        fig4, ax = plt.subplots()
        
        plt.xticks(rotation=90)  
        plt.bar(repair_df[1], repair_df[3])        
        st.pyplot(fig4)
    # elif my_choice == question[4]:
    #     st.text('전기차 등록대수')
    #     elec_car_reg_df.sort_values([2], inplace=True)
    #     fig2 = px.bar( elec_car_reg_df, x=1, y=2)    #plotly bar차트
    #     fig2.update_xaxes(title_text='지역')
    #     fig2.update_yaxes(title_text='count')
    #     st.plotly_chart(fig2)




if __name__ == '__main__':
    main()
