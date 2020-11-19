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
        result = {}
        self.modelNumber = modelNumber
        for key in self.website.keys():
            if key == 'szlcsc':
                self.website[key]['body']['pn'] = 1
                self.website[key]['body']['k'] = self.modelNumber
                self.website[key]['body']['sk'] = self.modelNumber

        try:
            print("szlcsc")
            result_tmp, totalCount = self.__crawlSZLCSCPrices()
            result['szlcsc'] = result_tmp
        except Exception as e:
            print(e)
            result['szlcsc'] = []
        try:
            print("ickey")
            result_tmp = self.__crawlICKEYPrices(modelNumber)
            result['ickey'] = result_tmp
        except Exception as e:
            print(e)
            result['ickey'] = []
        try:
            print('ti')
            result_tmp = self.__crawlTIPrices(modelNumber)
            result['ti'] = result_tmp
        except Exception as e:
            print(e)
            result['ti'] = []
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
        driver = webdriver.Remote(self.settings['CHROME']['chrome1_url'], DesiredCapabilities.CHROME)
        url = self.settings['WEBSITES']['ickey']['url'] + modelNumber
        driver.get(url)
        time.sleep(5)
        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        data = soup.find_all('div', class_='search-data-item')
        for item in data:
            tmp = {}
            value = item.find('div', class_="result-list clearfix")
            tmp['型号'] = value.find('div', class_='search-w-sup').text
            tmp['品牌'] = value.find('div', class_='search-w-maf').text
            tmp['库存'] = value.find('div', class_='search-result-bor store-num fw-b').text
            tmp['价格'] = self.__setICKEYPrice(value.find('div', class_='tl search-w-price').text,
                                    value.find('div', class_='tl search-w-hk').text,
                                    value.find('div', class_='tl search-w-home').text)
            result.append(tmp)
        return result

    def __crawlTIPrices(self, modelNumber):
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        from time import sleep
        result = []
        part = '{modelNum}#q={modelNum}&t=everything&linkId=1'.format(modelNum = modelNumber)
        url = self.settings['WEBSITE']['TI']['url'] + part
        driver = webdriver.Remote(self.settings['CHROME']['chrome2_url'], DesiredCapabilities.CHROME)
        driver.get(url)
        sleep(5)
        shadow_section = driver.execute_script('''return document.querySelector("ti-opn-snapshot").shadowRoot''')
        root = shadow_section.find_elements_by_css_selector('ti-card')
        for root1 in root:
            tmp = {}
            data = root1.find_element_by_class_name('ti-opn-snapshot-details-row')
            tmp['型号'] = data.find_element_by_class_name('ti-opn-snapshot-table-part-number').text
            tmp['库存'] = data.find_elements_by_tag_name('td')[4].text
            tmp['价格'] = self.__setTIPrice(data.find_elements_by_tag_name('td')[5].text)
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
        tmp = prices.split('\n')
        tmp = tmp[1:]
        for item in tmp:
            unit = item.split(' ')[0]
            value = item.split(' ')[1]
            result[unit] = value
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





