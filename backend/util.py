class Crawlers:
    def __init__(self):
        from config import settings
        self.settings = settings.as_dict()
        self.website = {}
        for key in self.settings['WEBSITES'].keys():
            self.website[key] = self.settings['WEBSITES'][key]
        self.modelNumber = ''

    def crawlAllPrices(self, modelNumber):
        result = {}
        self.modelNumber = modelNumber
        for key in self.website.keys():
            if key == 'szlcsc':
                self.website[key]['body']['pn'] = 1
                self.website[key]['body']['k'] = self.modelNumber
                self.website[key]['body']['sk'] = self.modelNumber
        result_tmp, totalCount = self.__crawlSZLCSCPrices()
        result['szlcsc'] = result_tmp
        return result

    #########Internal methods#########
    def __crawlSZLCSCPrices(self):
        import requests
        result = []
        price_times = [1, 10, 30, 100, 500, 1000]

        response = requests.post('https://so.szlcsc.com/search', headers=self.website['szlcsc']['headers'], data=self.website['szlcsc']['body'])
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

class Auther:
    def __init__(self):
        from config import settings
        self.password = settings.as_dict()["AUTHENTICATION"]['password']
        self.admin_password = settings.as_dict()["AUTHENTICATION"]['admin_password']

    def authUser(self, password):
        if password == self.password:
            return True
        else:
            return False



