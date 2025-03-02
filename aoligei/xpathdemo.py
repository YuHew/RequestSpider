import lxml
from lxml import etree

#节点选择
# /, //, ., ..
# text()选中开闭标签中的文本
# @     选中标签具体属性
# /html/head/title
# //title/text()   //link/@href
# 节点修饰语法用[]，里边可以是索引，
#                    可以是last()和加减
#                    可以是position，选中区间
#                    可以是属性值，@具体属性
#                    可以是contains，@具体属性 加具体条件

content = '''
<div>
    <ul>
        <li class="item-1">
            <a href="link1.html">first items</a>
        </li>
        <li class="item-1">
            <a href="link2.html">second items</a>
        </li>
        <li class="item-inactive">
            <a href="link3.html">third items</a>
        </li>
        <li class="item-1">
            <a href="link4.html">fourth items</a>
        </li>
        <li class="item-0">
            <a href="link5.html">fifth items</a>
        </li>
    </ul>
</div>
'''
html = etree.HTML(content)
xpath = html.xpath('//a[@href="link1.html"]/text()')
print(xpath)

xpath_a = html.xpath('//a')
for a in xpath_a:
    print(f'{a.xpath('./@href') + a.xpath('./text()')}')

