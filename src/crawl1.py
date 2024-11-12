import requests
import numpy as np
import pandas as pd
import urllib
import json

def crawl_car_repair_shop():
    hyun_repair_shop_url = 'https://www.car365.go.kr/web/program/ecrepairshopData.do?machineCode=1&menutype=3&entrpsnm=%ED%98%84%EB%8C%80&region=all&sigungu=&repairrange=&searchstr='

    # enterp = urllib.parse.quote('현대')
    # print(enterp)

    #car_enterp_name_list = ['현대', '기아', '르노코리아', '벤츠', '볼보, 폴스타(동일)', '아우디', '포르쉐']
    car_enterp_name_list = ['현대', '볼보, 폴스타(동일)']
    car_enterp_file_name_dic = {'현대': 'hyundai', '볼보, 폴스타(동일)': 'volvo'}

    repair_shop_all_dic = {}
    for x in car_enterp_name_list:
        one_enterp_list = []
        enterp = urllib.parse.quote(x)
        r = requests.get(f'https://www.car365.go.kr/web/program/ecrepairshopData.do?machineCode=1&menutype=3&entrpsnm={enterp}&region=all&sigungu=&repairrange=&searchstr=')
    
        r_json = r.json()
        
        # r_json['RESULT']["LIST"]
        # print(r_json['RESULT']["LIST"])
        repair_shop_df = pd.DataFrame(r_json['RESULT']["LIST"])
        # print(repair_shop_df)
        # one_enterp_list.extend(repair_shop_df.items())
        repair_shop_all_dic[x] = repair_shop_df
        # print(len(repair_shop_df))
        # print(car_enterp_file_name_dic[x])
        # repair_shop_df.to_csv(f'./data/{car_enterp_file_name_dic[x]}.csv')
        repair_shop_refine_df = repair_shop_df.copy()
        # print(repair_shop_refine_df.columns)
        repair_shop_refine_df.drop(columns = ['LIST_SIGUNGU', 'LIST_REPAIR_SHOP', 'LIST_ADDRESS', 'LIST_TEL'], inplace=True)
        # print(repair_shop_refine_df.columns)
        
        
        # aa = repair_shop_refine_df['LIST_REPAIR_RANGE'].str.contains('고전압') == True
        hv = repair_shop_refine_df['LIST_REPAIR_RANGE'].str.contains('고전압')    
        repair_shop_refine_df['high_voltage'] = hv.apply(lambda x : 1 if x else 0)
        repair_shop_refine_df.drop( columns = ['LIST_REPAIR_RANGE'], inplace=True)
        repair_shop_refine_df.to_csv(f'./data/{car_enterp_file_name_dic[x]}_refine.csv', index=False)
        
        print(repair_shop_refine_df.head())


    # for x, v in repair_shop_all_dic.items():
    #     print(v)

