import json
from jsonpath import jsonpath


# $  根节点，最外层大括号
# .  子节点
# .. 内部任意节点
#jsonpath 解决多层嵌套问题使用较多


text = {'key1': {'key2': {'key3': {'key4': {'key5': {'key6': {'key7': {'key8': 'python'}}}}}}}}
ret1 = jsonpath(text, '$.key1.key2.key3.key4.key5.key6.key7.key8')[0]
ret2 = jsonpath(text, '$..key8')[0]

print(ret1)
print(ret2)

text2 = '''{"code":200,"message":"获取成功","name":"juejin","title":"稀土掘金","subtitle":"热榜","from":"cache","total":50,"updateTime":"2025-03-02T14:26:49.797Z","data":[{"id":"7476030597166202890","title":"AI 插件第二弹，更强更好用","hot":756,"url":"https://juejin.cn/post/7476030597166202890","mobileUrl":"https://juejin.cn/post/7476030597166202890"},{"id":"7476018550009184275","title":"字节 Trae 支持 Claude 3.7 了，免费用！","hot":585,"url":"https://juejin.cn/post/7476018550009184275","mobileUrl":"https://juejin.cn/post/7476018550009184275"},{"id":"7476389305881346086","title":"深入理解 JavaScript 中的 this 绑定及模拟 call、apply、bind 方法","hot":495,"url":"https://juejin.cn/post/7476389305881346086","mobileUrl":"https://juejin.cn/post/7476389305881346086"},{"id":"7476435531514150963","title":"大厂开源项目，真的太爽啦,字节跳动出品！这个设计系统开源神器，让你的产品颜值与效率齐飞","hot":450,"url":"https://juejin.cn/post/7476435531514150963","mobileUrl":"https://juejin.cn/post/7476435531514150963"},{"id":"7476284371759317019","title":"用Trae智能开发中后台管理系统","hot":405,"url":"https://juejin.cn/post/7476284371759317019","mobileUrl":"https://juejin.cn/post/7476284371759317019"},{"id":"7476053262391869455","title":"Trae 最强 claude 3.7 带你体验面相算命","hot":378,"url":"https://juejin.cn/post/7476053262391869455","mobileUrl":"https://juejin.cn/post/7476053262391869455"}]}
'''

data = json.loads(text2)
ret3 = jsonpath(data,'$..title')
for e in ret3:
    print(e)