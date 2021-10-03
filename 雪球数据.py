import json
import pandas as pd

# data_url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=9999&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz%27'
# head = {'User-Agent':'Mozilla/5.0',"page":"1","size":"9999","order":"desc","orderby":"percent","order_by":"percent","market":"CN","type":"sh_sz%27"}

pd.set_option('display.unicode.east_asian_width', True)

fp = open('./data.json', 'r', encoding='utf8')
data = json.load(fp).get("data").get("list")
df = pd.read_csv("./my_stocks.csv", encoding='gbk')
names = list(df["股票名称"])

for dic in data:
    name = dic.get("name")
    if name in names:
        code = dic.get("symbol")
        if code[:2] not in ["SH","SZ"]:
            continue
        code = code[2:] + '.' + code[:2]
        price = dic.get("current")
        df.loc[df.loc[:,"股票名称"] == name,"股票代码"] = code
        df.loc[df.loc[:,"股票名称"] == name,"当前价"] = price
df.loc[:,"盈亏率"] = round((df.loc[:,"当前价"] / df.loc[:,"平均成本价"] - 1) * 100, 2).astype("str") + '%'
df.loc[:,"盈亏额"] = (df.loc[:,"当前价"] - df.loc[:,"平均成本价"]) * df.loc[:,"数量"]
print(df)
print('-' * 68)
print("sum:", sum(df.loc[:,"盈亏额"]), 'rmb')
df.loc[:,"盈亏额"] = df.loc[:,"盈亏额"].apply(lambda x: round(x,0))
df.loc[:,"市值"] = df.loc[:,"市值"].apply(lambda x: round(x,0))
df.to_csv("my_stocks.csv", index=False, encoding='gbk')


