import requests

headers = {
    'authority': 'so.szlcsc.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://so.szlcsc.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://so.szlcsc.com/global.html?k=SMAJ6.0A&hot-key=L7805CV-DG',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
}

page_number = 1
result = []
print("请输入要查询的型号")
product_model = input()
print("正在查询中")



def crawlPrices(product_model, page_number):
    result = []
    price_times = [1, 10, 30, 100, 500, 1000]
    body = {
        'os': '',
        'dp': '',
        'sb': '0',
        'pn': page_number,
        'c': '',
        'k': product_model,
        'tc': '0',
        'pds': '0',
        'pa': '0',
        'pt': '0',
        'gp': '0',
        'queryProductDiscount': '',
        'st': '',
        'sk': product_model,
        'activeStartTime': '-10509438.425',
        'isShowJDECard': 'no',
        'bp': '',
        'ep': '',
        'bpTemp': '',
        'epTemp': ''
    }
    response = requests.post('https://so.szlcsc.com/search', headers=headers, data=body)
    data = response.json()['result']
    try:
        from collections import OrderedDict
        for item in data['productRecordList']:
            prices_result = {}
            tmp = {}
            tmp['型号'] = item['productModel']
            tmp['品牌'] = item['lightBrandName']
            prices = item['numberprices'].split(',')
            if len(prices) > 0:
                price_unit = prices[1]
                prices_tmp = []
                for i in range(7, len(prices), 3):
                    prices_tmp.append(prices[i])
                prices = prices_tmp
                for i in range(len(prices)):
                    prices_result[int(price_unit) * price_times[i]] = prices[i]
                prices_result = OrderedDict(sorted(prices_result.items()))
                tmp['价格'] = prices_result
            else:
                tmp['价格'] = "没有价格"

            if item['hasStockNow'] == 'yes':
                tmp['是否有货'] = '有货'
            else:
                tmp['是否有货'] = '没有'
            result.append(tmp)
    except Exception as e:
        print(str(e))
    return result, data['totalCount']

result_tmp, totalCount = crawlPrices(product_model, page_number)
for item in result_tmp:
    result.append(item)
while len(result_tmp) == 20 and totalCount > 20:
    page_number += 1
    result_tmp, totalCount = crawlPrices(product_model, page_number)
    for item in result_tmp:
        result.append(item)

for item in result:
    for key in item:
        if key == '价格':
            for k, v in item[key].items():
                print(str(k) + '个:', v)
        else:
            print(key + ': ', item[key])
    print()
