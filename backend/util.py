from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.toml']
)

class Crawlers:
    def __init__(self):
        # from config import settings
        self.settings = settings.as_dict()
        self.website = {}
        for key in self.settings['WEBSITES'].keys():
            self.website[key] = self.settings['WEBSITES'][key]
        self.modelNumber = ''

    def crawlAllPrices(self, modelNumber):
        from time import time
        result = {}
        self.modelNumber = modelNumber
        for key in self.website.keys():
            if key == 'szlcsc':
                self.website[key]['body']['pn'] = 1
                self.website[key]['body']['k'] = self.modelNumber
                self.website[key]['body']['sk'] = self.modelNumber
        t1 = time()
        try:
            print("szlcsc")
            t1 = time()
            result_tmp, totalCount = self.__crawlSZLCSCPrices()
            result['szlcsc'] = result_tmp
        except Exception as e:
            print(e)
            result['szlcsc'] = []
        t2 = time()
        print(t2-t1)
        try:
            print("ickey")
            result_tmp = self.__crawlICKEYPrices(modelNumber)
            result['ickey'] = result_tmp
        except Exception as e:
            print(e)
            result['ickey'] = []
        t3 = time()
        print(t3-t2)
        try:
            print('ti')
            result_tmp = self.__crawlTIPrices(modelNumber)
            result['ti'] = result_tmp
        except Exception as e:
            print(e)
            result['ti'] = []
        print(time() - t3)
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

    def __crawlICKEYPrices(self, modelNumber):
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        import time
        from bs4 import BeautifulSoup
        result = []
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Remote(self.settings['CHROME']['chrome1_url'], options.to_capabilities())
        part = '{modelNum}&upload=&bom_ab=null'.format(modelNum = modelNumber)
        url = self.settings['WEBSITES']['ickey']['url'] + part
        driver.get(url)
        time.sleep(5)
        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        allData = soup.find('div', id='searchResult')
        data = allData.find_all('div', class_='search-data-item')
        tmp_result = []
        for item in data:
            tmp = item.find_all('div', class_='result-list-content huoqi_1')
            for i in tmp:
                tmp_result.append(i)

        for item in tmp_result:
            tmp = {}
            tmp['型号'] = item.find('div', class_='textSearch search-w-name').text.split('    ')[0]
            tmp['库存'] = item.find('div', class_='tl search-w-store').text.split(' ')[1]
            tmp['价格'] = self.__setICKEYPrice(item.find('div', class_='tl search-w-price').text,
                                             item.find('div', class_='tl search-w-hk').text,
                                             item.find('div', class_='tl search-w-home').text)

            result.append(tmp)
        return result

    def __crawlTIPrices(self, modelNumber):
        from selenium import webdriver
        # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        from time import sleep
        from bs4 import BeautifulSoup

        result = []
        part = '{modelNum}&keyMatch={modelNum}&tisearch=Search-CN-everything'.format(modelNum = modelNumber)
        url = self.settings['WEBSITE']['TI']['url'] + part
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Remote(self.settings['CHROME']['chrome2_url'], options.to_capabilities())
        driver.get(url)
        sleep(5)
        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        tmp = {}
        tmp['库存'] = soup.find_all('span', class_='product-note product-availability')[0].text.strip()
        prices = soup.find_all('div', class_='data-table-wrapper pdp-price-table')[0].text.split('\n')
        prices = [tmp for tmp in prices if tmp != "" and tmp != "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"]
        tmp['价格'] = self.__setTIPrice(prices)
        tmp['型号'] = modelNumber
        result.append(tmp)
        return result

    def __setICKEYPrice(self, priceRank, hkdPrice, cnyPrice):
        priceRank = priceRank.split(' ')
        priceRank = priceRank[1: len(priceRank) - 1]
        hkdPrice = hkdPrice.split(' ')
        hkdPrice = hkdPrice[1: len(hkdPrice) - 1]
        cnyPrice = cnyPrice.split(' ')
        cnyPrice = cnyPrice[1: len(cnyPrice) - 1]

        if len(hkdPrice) == 0:
            hkdPrice = ['无价格' for i in range(len(priceRank))]
        result = []
        tmp = {}
        for i in range(len(priceRank)):
            tmp[priceRank[i]] = 'hkd: ' + hkdPrice[i] + ' cny: ' + cnyPrice[i]
        return tmp

    def __setTIPrice(self, prices):
        result = {}
        result[prices[2]] = prices[3]
        result[prices[4]] = prices[5]
        result[prices[6]] = prices[7]
        result[prices[8]] = prices[9]
        return result


class Auther:
    def __init__(self):
        # from config import settings
        self.password = settings.as_dict()["AUTHENTICATION"]['password']
        self.admin_password = settings.as_dict()["AUTHENTICATION"]['admin_password']

    def authUser(self, password, isAdmin):
        tmp = False
        if isAdmin:
            if password == self.admin_password:
                tmp = True
        else:
            if password == self.password:
                tmp = True
        return tmp

    def resetPsw(self, password):
        try:
            import toml
            data = toml.load(open('settings.toml'))
            data['authentication']['password'] = password
            toml.dump(data, open('settings.toml', 'w'))
            global settings
            settings = Dynaconf(
                settings_files=['settings.toml'])
            return True
        except:
            return False





