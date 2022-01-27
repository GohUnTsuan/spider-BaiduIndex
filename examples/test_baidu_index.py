from qdata.baidu_index import (
    get_feed_index,
    get_news_index,
    get_search_index,
    get_live_search_index
)

import json
import pandas as pd



keywords_list = [['幽门螺杆菌'], ['黑便'], ['胃镜']]
cookies = """IDUPSID=75603EF66BD5F2EB3345D7ECB5CEDB51; PSTM=1639396369; BAIDUID=75603EF66BD5F2EBAB523EA5ECE1C68E:FG=1; BD_UPN=123253; __yjs_duid=1_b424383f0107aaa1e3063988d59316701639471235756; BDUSS=VxWUZMSFpaQUxYZm5kUTRRfnR6WU50ejVVNTA0akZNenRaRDRMcGs3VDA4UWhpRUFBQUFBJCQAAAAAAAAAAAEAAAD4SVUOst3E4PJ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRk4WH0ZOFhTW; BDUSS_BFESS=VxWUZMSFpaQUxYZm5kUTRRfnR6WU50ejVVNTA0akZNenRaRDRMcGs3VDA4UWhpRUFBQUFBJCQAAAAAAAAAAAEAAAD4SVUOst3E4PJ5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRk4WH0ZOFhTW; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_CK_SAM=1; PSINO=6; BAIDUID_BFESS=75603EF66BD5F2EBAB523EA5ECE1C68E:FG=1; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; shifen[1122063_91638]=1643187706; BCLID=7075927688245732522; BDSFRCVID=WykOJexroG0RHxRHPDEd-h6l5eKK0gOTDYLEOwXPsp3LGJLVgN5xEG0PtEey1c4-oxFfogKK3mOTH4-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbAjVCtatII3fP36q45HMt00qxby26nM5ec9aJ5nQI5nhKbuX5J1DqIzhJ_fQjcEQGOnQPnlQUbmjRO206oay6O3LlO83h5MaR7-Kl0MLPbtehTq0RoD044hbUnMBMPjamOnaPLE3fAKftnOM46JehL3346-35543bRTLnLy5KJYMDFljTu2j63beU5eetjK2CntsJOOaCvmDpbOy4oWK441DaOm-jb75Nbq2I_XLPbAV56tDnbj3M04K4o9-hvT-54e2p3FBUQJSfOPQft20b0ZhUj95h8La5bgBn7jWhk2Dq72y5jvQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCDt5FjJJPOVbobHJoHjJbGq4bohjPO2aO9BtQO-DOxoIbnbD31eMPl36KB0b0l02cGJbJ2QgnkQq5vbMnmqPtRXMJkXhKs3Jba0x-jLTnpWbQvKMtVDPnbM-nJyUnQhtnnBT5i3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFhJKIKMDKReP55q4D_MfOtetJyaR3UXRvvWJ5WqR7jDh512hDn0-O4KIr3JDtt0lvctn3cShbXXMoc5pkrKp0eWUbZBNcM2D5y3l02V-bHbJua-T3Dhp7lKtRMW20eWl7mWI-VsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKjaLtJjQP; BCLID_BFESS=7075927688245732522; BDSFRCVID_BFESS=WykOJexroG0RHxRHPDEd-h6l5eKK0gOTDYLEOwXPsp3LGJLVgN5xEG0PtEey1c4-oxFfogKK3mOTH4-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbAjVCtatII3fP36q45HMt00qxby26nM5ec9aJ5nQI5nhKbuX5J1DqIzhJ_fQjcEQGOnQPnlQUbmjRO206oay6O3LlO83h5MaR7-Kl0MLPbtehTq0RoD044hbUnMBMPjamOnaPLE3fAKftnOM46JehL3346-35543bRTLnLy5KJYMDFljTu2j63beU5eetjK2CntsJOOaCvmDpbOy4oWK441DaOm-jb75Nbq2I_XLPbAV56tDnbj3M04K4o9-hvT-54e2p3FBUQJSfOPQft20b0ZhUj95h8La5bgBn7jWhk2Dq72y5jvQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCDt5FjJJPOVbobHJoHjJbGq4bohjPO2aO9BtQO-DOxoIbnbD31eMPl36KB0b0l02cGJbJ2QgnkQq5vbMnmqPtRXMJkXhKs3Jba0x-jLTnpWbQvKMtVDPnbM-nJyUnQhtnnBT5i3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CFhJKIKMDKReP55q4D_MfOtetJyaR3UXRvvWJ5WqR7jDh512hDn0-O4KIr3JDtt0lvctn3cShbXXMoc5pkrKp0eWUbZBNcM2D5y3l02V-bHbJua-T3Dhp7lKtRMW20eWl7mWI-VsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKjaLtJjQP; bdindexid=ngacflggvu4ejfuvakjpgn7s44; H_PS_PSSID=35410_34429_35104_31660_34584_35491_35245_35317_26350_22157; H_PS_645EC=19025%2B1SSiDwOSkha63Bu7N0caBUCf%2B6KGscYzoNuQS2rxQ5omiqPQyVTAOjEYzzSGKe; baikeVisitId=07f50185-ad8a-47c4-802e-4144caf22f0b; delPer=1; __yjs_st=2_OTc3Mjc2ZWFkOWFjNzVjOGVjM2RiMGIzOTZjNTA1NjY5ZDUzNTVkNzQ5YTAwMmU2NTY0ZDMwMzQyMjM5N2ViOWNiZDc0ZWQxMDUyNzQxN2NiNDkwNDBmOTJkYzcyYWRmY2VkZDU3NDgzMGY3Y2NhNTNiNTcxMmU4NmUyMDU5YmZlYzUxNjFiOGMxZDNhNTcxNGI4NGI5YTA0ZjgzMWQ1OTEwMTc4M2RhZjMzNmNkMzZjNGQyYWE4ZjBjMjc4NzgxXzdfNzMwNmE3MGY=; ab_sr=1.0.1_NTM5MjhkZWQ3MjY2ZGM4OGI4YTIwZDE1M2YzNjY3Y2M5NGRjZWNmOTEyN2FjMmUyMmU5YjQ4YTEzYjcyNTgyYzYyZjBmZDdlYWI3OTVlN2U2OGU3YTk0ZWQ2NjNmNmI1; COOKIE_SESSION=5581_0_5_6_11_5_1_0_5_4_1_1_121_0_0_0_1643191478_0_1643197762%7C9%230_3_1637738010%7C1; RT="z=1&dm=baidu.com&si=o9uahh0o5v&ss=kyvhit3k&sl=2&tt=i6&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1bd"; sug=3; sugstore=0; ORIGIN=2; bdime=21110; BA_HECTOR=8lag2405agah8ha0l91gv2dad0r"""


def test_get_feed_index():
    """获取资讯指数"""
    for index in get_feed_index(
        keywords_list=keywords_list,
        start_date='2021-01-01',
        end_date='2021-12-30',
        cookies=cookies
    ):
        print(index)



def test_get_news_index():
    """获取媒体指数"""
    for index in get_news_index(
        keywords_list=keywords_list,
        start_date='2021-01-01',
        end_date='2021-12-30',
        cookies=cookies
    ):
        print(index)
    print(index)

def test_get_search_index():
    """获取搜索指数"""
    df_all = pd.DataFrame()
    for index in get_search_index(
        keywords_list=keywords_list,
        start_date='2021-12-01',
        end_date='2021-12-30',
        cookies=cookies,
        area=909
    ):
        print(index)
        df = pd.DataFrame.from_dict(index)
        df_all = pd.concat([df_all, df])
        df_all.to_csv("search_index.csv")


def test_get_search_index_area():
    """获取分地区搜索指数"""
    df_all = pd.DataFrame()
    areas = [50, 51, 52, 53, 54, 55, 56, 87, 253]
    for area in areas:
        print(area)
        for index in get_search_index(
            keywords_list=keywords_list,
            start_date='2017-01-01',
            end_date='2021-12-30',
            cookies=cookies,
            area=area
        ):
            print(index)
            df = pd.DataFrame.from_dict(index)
            df.loc[:, 'area'] = area
            df_all = pd.concat([df_all, df])
    df_all.to_csv("search_index_area.csv")

def test_get_live_search_index():
    """获取搜索指数实时数据"""
    for index in get_live_search_index(
        keywords_list=keywords_list,
        cookies=cookies,
        area=0
    ):
        print(index)

    for index in get_live_search_index(
        keywords_list=keywords_list,
        cookies=cookies,
        area=911
    ):
        print(index)


if __name__ == "__main__":
    # test_get_feed_index()
    # test_get_news_index()
    test_get_search_index()
    # test_get_search_index_area()
    # test_get_live_search_index()
