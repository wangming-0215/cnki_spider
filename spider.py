import re
import random
import requests
import sys
import time
from bs4 import BeautifulSoup
from config import Config
from openpyxl import Workbook

'''
爬虫类

TODO: 添加学术论文下载功能
'''


class Spider:
    def __init__(self):
        self.config = Config()
        self.headers = self.config.get('headers')
        self.session = requests.session()
        self.table_contents = [['题名', '作者', '来源', '数据库', '简介', '发表时间']]
        self.wb = Workbook()
        self.main()

    '''
    爬虫需要的cookie
    requests Session()类可以长期保存session
    '''

    def get_cookies(self, keyword):
        search_url = self.config.get('search_url')
        search_params = self.config.get('search')
        search_params['txt_1_value1'] = keyword
        self.session.get(search_url, params=search_params, headers=self.headers)

    '''
    先爬第一页，获取总页数和第一页的HTML
    '''

    def get_list(self, curr_page=1):
        base_list_url = self.config.get('base_list_url')
        base_list_params = self.config.get('list_page')
        base_list_params['curpage'] = curr_page
        response = self.session.get(base_list_url, params=base_list_params, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find_all('div', {'class': 'GridRightColumn'})
        amount = soup.find('div', {'class': 'pagerTitleCell'}).get_text()
        total_page = int(soup.find('span', {'class': 'countPageMark'}).get_text().split('/')[1])
        return amount, total_page, content_div

    '''
    替换字符串中的空格
    '''

    # noinspection PyMethodMayBeStatic
    def replace_space(self, text):
        regexp = re.compile(r'[\r\n\t\s，$]')
        return regexp.sub('', text)

    '''
    处理每一页的数组，保存到列表，后期输出excel
    '''

    def get_per_list_data(self, page_soup):
        for elements in page_soup:
            # 题名
            title = elements.find('h3', {'class': 'title_c'}).get_text()

            # 作者
            author = elements.find('span', {'class': 'author'}).get_text()

            # 来源
            journal = elements.find('span', {'class': 'journal'}).get_text()
            pubdate = elements.find('span', {'class': 'pubdate'}).get_text()
            source = journal + ' ' + pubdate

            # 数据库
            database = elements.find('span', {'class': 'database'}).get_text()

            # 简介
            abstract = elements.find('p', {'class': 'abstract_c'}).get_text()

            # 发表时间
            publish_date_text = elements.find('div', {'class': 'DetailNum'}).find_all('label')[-1].get_text()
            publish_date = publish_date_text.replace('发表时间：', '')

            row = list(
                map(lambda text: self.replace_space(text), [title, author, source, database, abstract, publish_date])
            )

            self.table_contents.append(row)

    '''
    数据写入Excel
    '''

    def write_to_excel(self, title):
        sheet = self.wb.active
        sheet.title = title
        for i, rows in enumerate(self.table_contents):
            for j, columns in enumerate(rows):
                sheet.cell(row=i + 1, column=j + 1, value=str(columns))
        self.wb.save('./' + title + '.xlsx')

    '''
    主函数
    '''

    def main(self):
        key_word = sys.argv[1]
        self.get_cookies(key_word)
        amount, total_page, page_content = self.get_list()
        print(amount + ', 共' + str(total_page) + '页数据')
        print('正在爬取第1页数据...')
        self.get_per_list_data(page_content)
        current_page = 2

        while current_page <= total_page:
            print('正在爬取第' + str(current_page) + '页数据...')
            try:
                _, _, page_content = self.get_list(current_page)
            except AttributeError:
                # 发生异常了，ip可能被封了， 刷新一下cookie可以解决问题, 但是有几率再次异常
                self.session = requests.session()
                self.get_cookies(key_word)
                _, _, page_content = self.get_list(current_page)

            self.get_per_list_data(page_content)
            current_page = current_page + 1

        self.write_to_excel(key_word)
        print('爬虫结束！！！')


spider = Spider()
