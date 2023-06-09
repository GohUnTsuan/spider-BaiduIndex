"""
百度指数数据获取最佳实践
此脚本完成
1. 清洗关键词
2. 发更少请求获取更多的数据
3. 请求容错
4. 容错后并保留当前已经请求过的数据，并print已请求过的keywords
"""
from queue import Queue
from typing import Dict, List
import traceback
import time

import pandas as pd
from qdata.baidu_index import get_search_index
from qdata.baidu_index.common import check_keywords_exists, split_keywords
from qdata.baidu_index.config import PROVINCE_CODE, CITY_CODE

cookies = """BAIDUID=AF295C0CCE1E89C6B137658BBC9550C5:FG=1; BAIDUID_BFESS=AF295C0CCE1E89C6B137658BBC9550C5:FG=1; BDUSS=Hh2NHd1VS1SUTlndWRnamFyZ2lqbXFLV1hXWS1zR2plTWNONjRYYn5WbG9iS2xrRVFBQUFBJCQAAAAAAAAAAAEAAAD4SVUOst3E4PJ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGjfgWRo34FkM; BDUSS_BFESS=Hh2NHd1VS1SUTlndWRnamFyZ2lqbXFLV1hXWS1zR2plTWNONjRYYn5WbG9iS2xrRVFBQUFBJCQAAAAAAAAAAAEAAAD4SVUOst3E4PJ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGjfgWRo34FkM; BIDUPSID=AF295C0CCE1E89C6B137658BBC9550C5; PSTM=1686232964; bdindexid=9qqq2o44smsjjm74a21b7s1jb4; PTOKEN=8bd32069f82466ab7d9071edacc610b4; PTOKEN_BFESS=8bd32069f82466ab7d9071edacc610b4; STOKEN=565c8f1936af297a4369443fd0846a9642f31b5c857f8868a0425e493080e6c4; STOKEN_BFESS=565c8f1936af297a4369443fd0846a9642f31b5c857f8868a0425e493080e6c4; UBI=fi_PncwhpxZ%7ETaJcxa1KX0RhvsNhdNaMz5W; UBI_BFESS=fi_PncwhpxZ%7ETaJcxa1KX0RhvsNhdNaMz5W; __yjs_st=2_ZDk4ZDRjZDU1YjE4YWE1MjVkYTE1NTJhNmU2NGNmOTlmMmJjNzNjMzRkZTA3OTc2ZDYzYTY4MGU5OTM1YzU0MGRkYTdiNGNmNmJkNTIyM2RhN2I4YzBlMzg1ZTNkYTRjODJmYWY0NGIzZjM3ZjEzZmI2MDYwOWQxMmNjNDAyNjhiNDU2OGRiZWZiNmEwNzg2NjM0MWJkNzdiYTM0ZjU2MDRlYjBmNDM5NDlmYTUyZDI5MTUyMjUxYjg5NGYyMGQwXzdfMmI3MGU4YjE="""


def get_clear_keywords_list(keywords_list: List[List[str]]) -> List[List[str]]:
    q = Queue(-1)

    cur_keywords_list = []
    for keywords in keywords_list:
        cur_keywords_list.extend(keywords)
    
    # 先找到所有未收录的关键词
    for start in range(0, len(cur_keywords_list), 15):
        q.put(cur_keywords_list[start:start+15])
    
    not_exist_keyword_set = set()
    while not q.empty():
        keywords = q.get()
        try:
            check_result = check_keywords_exists(keywords, cookies)
            time.sleep(5)
        except:
            traceback.print_exc()
            q.put(keywords)
            time.sleep(90)

        for keyword in check_result["not_exists_keywords"]:
            not_exist_keyword_set.add(keyword)
    
    # 在原有的keywords_list拎出没有收录的关键词
    new_keywords_list = []
    for keywords in keywords_list:
        not_exists_count = len([None for keyword in keywords if keyword in not_exist_keyword_set])
        if not_exists_count == 0:
            new_keywords_list.append(keywords)

    return new_keywords_list


def save_to_excel(datas: List[Dict]):
    pd.DataFrame(datas).to_excel("index.xlsx")

def save_to_csv(datas: List[Dict]):
    pd.DataFrame(datas).to_csv("index.csv")

def get_search_index_demo(keywords_list: List[List[str]], city_codes: Dict[str, int]):
    """
        1. First clean keywords data, pull out the keywords that are not included
        2. Then split_keywords normal request for keywords
        3. Store the data in excel
    """
    print("Starting keyword cleaning")
    requested_keywords = []
    keywords_list = get_clear_keywords_list(keywords_list)
    q = Queue(-1)

    for splited_keywords_list in split_keywords(keywords_list):
        q.put(splited_keywords_list)

    for city_name, city_code in city_codes.items():
        print(f"Starting Baidu Index request for city: {city_name}")
        datas = []
        while not q.empty():
            cur_keywords_list = q.get()
            try:
                print(f"Start request: {cur_keywords_list}")
                for index in get_search_index(
                    keywords_list=cur_keywords_list,
                    # set start_date and end_date
                    start_date='2018-06-01',
                    end_date='2023-06-01',
                    cookies=cookies,
                    # set the area to the city code
                    area=city_code
                ):
                    index["keyword"] = ",".join(index["keyword"])
                    index["city_code"] = city_code  # store city code
                    index["city_name"] = city_name  # store city name
                    datas.append(index)
                requested_keywords.extend(cur_keywords_list)
                print(f"Request completed: {cur_keywords_list}")
                time.sleep(10)
            except:
                traceback.print_exc()
                print(f"Request error, requested_keywords: {requested_keywords}")
                save_to_excel(datas)
                q.put(cur_keywords_list)
                time.sleep(180)

        save_to_csv(datas)


if __name__ == "__main__":
    # set keywords_list
    keywords_list = [
        ['幽门螺杆菌'], ['黑便'], ['胃镜'], ['消化道出血']
    ]
    # CITY_CODE is a dictionary of city names and their corresponding codes
    get_search_index_demo(keywords_list, CITY_CODE)
