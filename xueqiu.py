import os
import requests
import http.client
import time
import json
import yaml
import pandas as pd

pd.set_option('display.unicode.east_asian_width', True)


def _calc_percent(old_price, new_price):
    return "{:.3f}".format((new_price - old_price) / old_price * 100) + "%"


def _change_code(code):
    return code[2:] + '.' + code[:2]


def _clean_data(data):
    stocks = {}
    for stock in data.get("data").get("list"):
        name = stock.get("name")
        stocks[name] = {
            "代码": stock.get("symbol"),
            "现价": stock.get("current"),
            "涨幅": stock.get("percent"),
            "涨跌": stock.get("chg")
        }
    return stocks


def show_data_table(df):
    print("| 股票名称 |    股票代码 |  买入成本 |   当前价 |   数量 |    盈亏率 |")
    print("| ------- | --------- | -------: | -----: | ----: | -------: |")
    for name in df.index:
        array = list(df.loc[name])
        print("| {} | {:>9s} | {:>8.3f} | {:>7.2f} | {:>5d} | {:>8s} |".format(name, array[0], array[1], array[2], array[3], array[4]))


class Stock:
    def __init__(self):
        localtime = time.localtime(time.time())
        self.datapath = "%d-%02d-%02d.json" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        if os.path.exists(self.datapath):
            f = open(self.datapath, "r", encoding="utf-8")
            self.data = json.load(f)
            f.close()
        else:
            self.download_data()
        self.show_data()

    def download_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/97.0.4692.71 Safari/537.36 "
        }
        url = "https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=9999&order=desc&orderby=percent" \
              "&order_by=percent&market=CN&type=sh_sz "
        r = requests.get(url, headers=headers)
        if r.status_code == http.client.OK:
            print("Connect Success")
            self.data = _clean_data(r.json())
            f = open(self.datapath, "w", encoding="utf-8")
            f.write(json.dumps(self.data, indent=2, ensure_ascii=False))
            f.close()
        else:
            print("Connect Fail")

    def show_data(self):
        f = open("myStock.yml", "r", encoding="utf-8")
        my_stock = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        money, earning = 0, 0
        for stock in my_stock:
            if self.data.get(stock):
                my_stock[stock]["股票代码"] = _change_code(self.data.get(stock).get("代码"))
                my_stock[stock]["当前价"] = self.data.get(stock).get("现价")
                my_stock[stock]["盈亏率"] = _calc_percent(my_stock[stock]["买入成本"], my_stock[stock]["当前价"])
            money += my_stock[stock]["当前价"] * my_stock[stock]["数量"]
            earning += (my_stock[stock]["当前价"] - my_stock[stock]["买入成本"]) * my_stock[stock]["数量"]
        df = pd.DataFrame(my_stock).transpose().sort_values(by="股票代码")
        df = df[["股票代码", "买入成本", "当前价", "数量", "盈亏率"]]
        if 0:
            print(df)
        else:
            show_data_table(df)
        print("总值:", round(money, 2))
        print("浮盈:", round(earning, 2))


s = Stock()
