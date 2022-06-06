"""
给予Django框架，写了一个分页的功能，封装成了一个类工具，方便后续直接调用。
"""


# 封裝分頁類
class MyPage(object):

    def __init__(self, current_page, total_count, url_prefix, per_page=3, max_show=11):
        """
        初始化一个我自己定义的分页实例
        :param current_page: 当前页码
        :param total_count: 总的数据量
        :param url_prefix: 分页中a标签的url前缀
        :param per_page: 每一个显示多少条数据
        :param max_show: 页面上最多显示多少个页码
        """
        self.total_count = total_count
        self.per_page = per_page
        self.max_show = max_show
        self.url_prefix = url_prefix

        # 最多顯示頁碼數的一半
        half_show = max_show // 2
        #    因為URL取到的參數是字符串格式，需要轉換成int類型
        try:
            current_page = int(current_page)
        except Exception as e:
            # 如果輸入的頁碼不是正經頁碼，默認展示第一頁
            current_page = 1
        # 求總共需要多少頁顯示
        total_page, more = divmod(total_count, per_page)
        if more:
            total_page += 1
        # 如果輸入的當前頁碼數大於總數據的頁碼數，默認顯示最後一頁
        if current_page > total_page:
            current_page = total_page
        self.current_page = current_page

        # 計算一下顯示頁碼的起點和終點
        show_page_start = current_page - half_show
        show_page_end = current_page + half_show
        # 特殊情況特殊處理
        # 1. 當前頁碼 - half_show <= 0
        if current_page - half_show <= 0:
            show_page_start = 1
            show_page_end = max_show
        # 2. 當前頁碼數 + hale_show >= total_page
        if current_page + half_show >= total_page:
            show_page_end = total_page
            show_page_start = total_page - max_show + 1
        # 3. 總共需要的頁碼數 < max_show
        if total_page < max_show:
            show_page_start = 1
            show_page_end = total_page

        self.show_page_start = show_page_start
        self.show_page_end = show_page_end
        self.total_page = total_page

    # 數據切片的起點
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    # 數據切片的終點
    @property
    def end(self):
        return self.current_page * self.per_page

    # 分頁的html代碼
    def page_html(self):
        tmp = []
        page_html_start = '<nav aria-label="Page navigation" class="text-center"><ul class="pagination">'
        page_html_end = '</ul></nav>'
        tmp.append(page_html_start)
        # 添加一個首頁
        tmp.append('<li><a href="/{}?page=1">首頁</a></li>'.format(self.url_prefix))
        # 添加一個上一頁
        # 當當前頁是第一頁的時候不能再點擊上一頁
        if self.current_page - 1 <= 0:
            tmp.append(
                '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            tmp.append(
                '<li><a href="/{}?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.url_prefix, self.current_page - 1))
        # for循環添加要展示的頁碼
        for i in range(self.show_page_start, self.show_page_end + 1):
            # 如果for循環的頁碼等於當前頁碼，給li標籤加一個active的樣式
            if self.current_page == i:
                tmp.append('<li class="active"><a href="/{1}?page={0}">{0}</a></li>'.format(i, self.url_prefix))
            else:
                tmp.append('<li><a href="/{1}?page={0}">{0}</a></li>'.format(i, self.url_prefix))
        # 添加一個下一頁
        # 當當前頁已經是最後一頁，應該不讓下一頁按鈕能點擊
        if self.current_page + 1 > self.total_page:
            tmp.append(
                '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            tmp.append(
                '<li><a href="/{}?page={}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.url_prefix, self.current_page + 1))
        # 添加一個尾頁
        tmp.append('<li><a href="/{}?page={}">末頁</a></li>'.format(self.url_prefix, self.total_page))
        tmp.append(page_html_end)

        page_html = "".join(tmp)
        return page_html