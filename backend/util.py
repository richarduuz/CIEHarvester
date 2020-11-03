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
    'referer': 'https://so.szlcsc.com/global.html?k=SMAJ6.0A&hot-key=OP07CDR',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'cookie': 'noLoginCustomerFlag=5d12a40bd3601adb4f99; noLoginCustomerFlag2=dabbe3cc9401c32cf0fc; Hm_lvt_e2986f4b6753d376004696a1628713d2=1604029128; guidePage=true; AGL_USER_ID=a4bd3bfd-7262-4573-a672-5e0aeb261a21; isShowRightUtils=no; mediav=%7B%22eid%22%3A%22586266%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A1%2C%22_refnf%22%3A0%7D; searchHistoryRecord=SMAJ6.0A%EF%BC%9A2SC4617TLR%EF%BC%9A2SC4617TSR%EF%BC%9A; acw_tc=2ff62a9a16043799442851365edea0f41e5286612cd4bf544fc33c696c; Qs_lvt_290854=1604029114%2C1604379955; Qs_pv_290854=4105050826023623700%2C3166205219329458700%2C2534289223983876600%2C1667744776741844500%2C3713273474357107000; Hm_lpvt_e2986f4b6753d376004696a1628713d2=1604379968',
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
    if response.status_code == 200:
        data = []
        try:
            data = response.json()['result']
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
            return result, data['totalCount']
        except Exception as e:
            print(str(e))
            return None, 0
    else:
        return None, 0

result_tmp, totalCount = crawlPrices(product_model, page_number)
if result_tmp != None:
    for item in result_tmp:
        result.append(item)
    while len(result_tmp) == 20 and totalCount > 20:
        page_number += 1
        result_tmp, totalCount = crawlPrices(product_model, page_number)
        for item in result_tmp:
            result.append(item)

    print("搜索完毕, 一共找到{num}条记录".format(num = len(result)))
    print()
    counter = 1
    for item in result:
        print("第{_}条".format(_ = counter))
        for key in item:
            if key == '价格':
                for k, v in item[key].items():
                    print(str(k) + '个:', v)
            else:
                print(key + ': ', item[key])
        print()
        counter += 1
else:
    print("搜索失败")
