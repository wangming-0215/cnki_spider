import time


class Config:
    def __init__(self):
        self.config = {
            'headers': {},
            'search': {},
            'list_page': {},
            'search_url': 'http://kns.cnki.net/kns/request/SearchHandler.ashx?',
            'base_list_url': 'http://kns.cnki.net/kns/brief/brief.aspx'
        }

        # 请求头
        self.config['headers']['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ' \
                                               'like Gecko) Chrome/66.0.3359.117 Safari/537.36 '

        # 搜索参数
        self.config['search']['NaviCode'] = '*'
        self.config['search']['ua'] = '1.11'
        self.config['search']['PageName'] = 'ASP.brief_default_result_aspx'
        self.config['search']['DbPrefix'] = 'SCDB'
        self.config['search']['DbCatalog'] = '中国学术文献网络出版总库'
        self.config['search']['ConfigFile'] = 'SCDBINDEX.xml'
        self.config['search']['db_opt'] = 'CJFQ,CJRF,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'
        self.config['search']['txt_1_sel'] = 'SU$%=|'
        self.config['search']['txt_1_special1'] = '%'
        self.config['search']['his'] = 0
        self.config['search']['parentdb'] = 'SCDB'
        self.config['search']['__'] = time.strftime('%a %m %d %Y %H:%M:%S GMT+0800 (CST)')

        # 第一页参数
        self.config['list_page']['RecordsPerPage'] = '20'
        self.config['list_page']['QueryID'] = '7'
        self.config['list_page']['turnpage'] = '1'
        self.config['list_page']['tpagemode'] = 'L'
        self.config['list_page']['dbPrefix'] = self.config['search']['DbPrefix']
        self.config['list_page']['DisplayMode'] = 'custommode'
        self.config['list_page']['PageName'] = self.config['search']['PageName']

    def get(self, key, parent=None):
        if key and key in self.config.keys():
            return self.config[key]

        if key and parent in self.config.keys():
            return self.config[parent][key]

    def set(self, key, value, parent=None):
        if key and value and key in self.config.keys():
            self.config[key] = value

        if key and value and parent in self.config.keys():
            self.config[parent][key] = value
