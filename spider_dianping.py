from time import sleep
from urllib import request
import re

urls_dianping = {
    "华中科技大学集贤楼湘菜馆": "http://www.dianping.com/shop/2336701/review_more?pageno=",
    "华中科技大学东一学生食堂": "http://www.dianping.com/shop/21618772/review_more?pageno=",
    "华中科技大学学生二食堂": "http://www.dianping.com/shop/21618797/review_more?pageno=",
    "华中科技大学 西一食堂": "http://www.dianping.com/shop/50939069/review_more?pageno=",
    "华中科技大学东教工食堂": "http://www.dianping.com/shop/21618943/review_more?pageno=",
    "华中科技大学 东园食堂一楼": "http://www.dianping.com/shop/22729452/review_more?pageno=",
    "华中科技大学百景园(一楼食堂)": "http://www.dianping.com/shop/21180749/review_more?pageno=",
    "华中科技大学东三食堂": "http://www.dianping.com/shop/17686588/review_more?pageno=",
    "华中科技大学西二食堂": "http://www.dianping.com/shop/58001459/review_more?pageno=",
    "韵苑学生食堂": "http://www.dianping.com/shop/58597139/review_more?pageno=",
    "西华园文化餐吧": "http://www.dianping.com/shop/74577699/review_more?pageno=",
    "清真食堂": "http://www.dianping.com/shop/18395592/review_more?pageno="
}# 共 12 个食堂


# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


# 爬取大众点评网上的华科食堂点评
class Hust_canteen:
    def __init__(self, base_url):
        # 大众上华科食堂的页面url无规律，每个baseUrl都是不同食堂页面
        self.baseUrl = base_url
        self.pageIndex = 1
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1)'}
        self.comments = {}
        self.canteen_name = ''
        self.pageCode = ''

    # 访问指定的pageIndex页，并返回页面脚本
    def getPage(self, page_index):
        sleep(3)
        try:
            url = self.baseUrl + str(page_index)
            # 构建请求的request
            req = request.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = request.urlopen(req)
            # 将页面转化为UTF-8编码
            page_code = response.read().decode('utf-8')
            self.pageCode = page_code
            return page_code

        except(request.URLError) as e:
            if hasattr(e, "reason"):
                print(u"连接失败,错误原因", e.reason)
                return None

    # 抓取食堂名称
    def get_canteen(self):
        if not self.pageCode:
            print("页面加载失败....")
            return None
        pattern = re.compile(
            r'<meta http-equiv="X-UA-Compatible" content="IE=edge"/>.*?<title>(.*?)的全部评价-武汉-大众点评网</title>',
            re.S)
        items = re.findall(pattern, self.pageCode)
        self.canteen_name = items[0]
        return items[0]

    # 抓取食堂名称
    def get_comments(self):
        if not self.pageCode:
            print("页面加载失败....")
            return None
        pattern = re.compile(
            r'<p class="name">(.*?)</p>.*?<span class="user-rank-rst.*?<div class="user-info">.*?class="item-rank-rst irr-star(.*?)"></span>.*?class="comm-per">',
            re.S)
        items = re.findall(pattern, self.pageCode)
        if items == None:
            return None
        for item in items:
            tool = Tool()
            user_name = tool.replace(item[0])
            print("用户", user_name)
            print("评分", float(item[1][0]))
            self.comments.setdefault(user_name, float(item[1][0]))
        return self.comments

    def get_all_comments(self):
        self.getPage(1)
        self.get_canteen()
        for page_num in range(1, 3):
            self.getPage(page_num)
            page_content = self.get_comments()
            if page_content == None:
                print(self.canteen_name, "评论结束。评论有", str(page_num - 1), "页")
                break


if __name__ == "__main__":

    #  "清真食堂": "http://www.dianping.com/shop/18395592/review_more?pageno="
    # "西华园文化餐吧": "http://www.dianping.com/shop/74577699/review_more?pageno="
    # "韵苑学生食堂": "http://www.dianping.com/shop/58597139/review_more?pageno="
    # "华中科技大学西二食堂": "http://www.dianping.com/shop/58001459/review_more?pageno="
    # "华中科技大学东三食堂": "http://www.dianping.com/shop/17686588/review_more?pageno="
    # "华中科技大学百景园(一楼食堂)": "http://www.dianping.com/shop/21180749/review_more?pageno=",
    # "华中科技大学 东园食堂一楼": "http://www.dianping.com/shop/22729452/review_more?pageno=",
    # "华中科技大学东教工食堂": "http://www.dianping.com/shop/21618943/review_more?pageno="

    #  "华中科技大学学生二食堂": "http://www.dianping.com/shop/21618797/review_more?pageno=",

    hust_canteen_comments = {}
    c1=Hust_canteen("http://www.dianping.com/shop/21618797/review_more?pageno=")
    c1.get_all_comments()
    hust_canteen_comments[c1.canteen_name]=c1.comments
    print(hust_canteen_comments)

    # for name, url in urls_dianping.items():
    #     spider = Hust_canteen(url)
    #     spider.get_all_comments()
    #     hust_canteen_comments[spider.canteen_name] = spider.comments
    # print(hust_canteen_comments)
