import scrapy
import os
from datetime import date

basedir = os.path.dirname(os.path.realpath('__file__'))


# Xử lý tên sản phẩm

# Hàm xử lý tên sản phẩm
def name_processing(name):
    f = open("blacklist.txt", "r", encoding='utf-8')
    lines = f.read().splitlines()

    if name == None:
        return ''
    for character in lines:
        if character in name or character.lower() in name or character.title() in name or character.upper():
            name = name.replace(character,'')
            name = name.replace(character.lower(),'')
            name = name.replace(character.title(),'')
            name = name.replace(character.upper(),'')

    black_list1 = ['Chính', 'hãng', 'I', 'VN/A', 'chính', '|', '-', 'Hãng', 'Cũ', 'Nobox',
                   '1', '1|', 'Chip', 'Snapdragon', '865', '865+', 'Hongkong', 'Fan', 'Edition',
                   'Hộp', 'Trải', 'Nghiệm', 'Đã', 'Kích', 'Phép', 'Hoạt', 'Ng', 'Pin', 'Siêu',
                   'Dùng', 'Siêu', 'Chụp', 'Ảnh', 'Nguyên', 'Nhập', 'Khẩu', 'Màn', 'Hình', '2K',
                   'Nhám', 'Cấu', 'Hiệu', 'Năng', 'Đầy', 'Giá', 'Tiên', 'Máy', 'Thiết', 'Kế',
                   'Tử', 'HàN', 'QuốC', 'Như', 'Vna', 'Điện', 'Thoại', 'Ng', 'Racing', 'Youth',
                   'Zoom', '64', '128', 'Tay', 'Phân', 'Quốc', 'Chống', ]

    unprocess_name = name.split()
    processed_name = []
    for i in unprocess_name:
        if i not in black_list1:
            processed_name.append(i)
    return ' '.join(processed_name).title()


# Xử lý price
def format_price(price):
    _list = ['đ', '₫', '.', ',', 'VNĐ', 'VND', '\r', '\n', '\t', ' ', ' ']
    if not price:
        return None
    else:
        for i in _list:
            price = price.replace(i, '')
    return price


# Xử lý bộ nhớ
def format_bonho(name):
    attr_bonho = 'None'
    list_attr_bonho = ['512GB', '256GB', '128GB', '64GB', '16GB', '32GB', '512Gb', '256Gb', '128Gb', '64Gb', '16Gb',
                       '32Gb']

    for i in list_attr_bonho:
        if i in name:
            attr_bonho = i
    return attr_bonho

# Lớp crawl dữ liệu minhducvn
class minhducvn(scrapy.Spider):
    name = 'minhducvn'
    start_urls = ['https://www.minhducvn.com/danh-muc/dien-thoai/', ]

    def parse(self, response):
        self.log('Visited ' + response.url)

        products = response.css('div.products > div.product-small')

        self.log('products ' + str(len(products)))
        for product in products:
            title = name_processing(product.css('div.box-text > div.title-wrapper > p > a::text').get()).title()
            item_link = product.css('div.box-text > div.title-wrapper > p.name > a::attr(href)').get()
            thuong_hieu = item_link.split('/')[3].split('-')[0]
            image1 = ''

            item = {
                'ten': title,
                'url': item_link,
                'image': image1,
                'ngay': date.today().strftime("%Y-%m-%d"),
                'loaisanpham': 'dienthoai',
                'thuonghieu': thuong_hieu
            }
            yield scrapy.Request(url=item_link, meta={'item': item}, callback=self.get_detail)

        next_page_url = response.css('ul.page-numbers > li:nth-child(5) > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def get_detail(self, response):
        self.log('Visited ' + response.url)
        item = response.meta['item']

        option_old_price = format_price(response.css('div.price-wrapper > p.price > del > span > bdi::text').get())
        option_rom = format_bonho(response.css('div.product-info > h1.product-title::text').get())

        option_color = None
        option_new_price = format_price(response.css('div.price-wrapper > p.price > ins > span > bdi::text').get())
        active = True

        image2 = response.css('div.woocommerce-product-gallery__image > a > img::attr(src)').get()

        attributes = []
        attributes.append({
            'bonho': option_rom,
            'mausac': option_color,
            'giagoc': option_old_price,
            'giamoi': option_new_price,
            'active': active
        })

        item['thuoctinh'] = attributes
        item['image'] = image2
        item['tskt'] = response.css('#ago_tsky_widget-3').get()
        item['mota'] = ''
        return item