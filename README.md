# 须知

本项目只有单选、多选、打分题，其余的需要自己设计，支持按照比例完成问卷

## 主要实现逻辑

通过selenium实现答题，将不同选项按照概率生成答案，再将答案转化为0和1的列表，遍历每个选项实现点击动作，完成答题

------



# 先检查浏览器版本

检查chrome浏览器版本不是114.0.5735.xx，版本对则跳过

![image-20240406154253679](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406154253679.png)

如果不是先卸载chrome，然后打开资源文件夹解压，安装114版本

![image-20240406154631288](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406154631288.png)

![image-20240406154802980](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406154802980.png)

当然，你也可以自行选择版本安装，chrome浏览器版本要与chromedriver基本对上，下面是chromedriver驱动网址

https://registry.npmmirror.com/binary.html?path=chromedriver/

将下载的驱动复制到项目文件夹下

![image-20240406165126800](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406165126800.png)

# 参数配置

## 代理ip

项目里面已经设置一些反检测手段，我没有用代理ip也没有关系，试过几百份问卷，可以根据自己实际情况是否需要配置，api自己修改，需要一定编程基础，新手勿试

下面的自己改

```python
# 代理ip的api接口
api = "https://ip.ihuan.me/today/2024/03/31/01.html"
```

```python
# 获取代理ip池
def Get_Api(api):
    headers = {
        "User-Agent": str(UserAgent.random),
    }
    ip_text = requests.get(api, headers=headers).text
    # 编译正则表达式
    proxy_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})\b')

    # 查找所有代理IP
    proxies = proxy_pattern.findall(ip_text)
    return proxies
```

```python
if __name__ == "__main__":
    ip_list = utils.Get_Api(config.api)
    for copies in range(config.copies_num):
        ip = ip_list[copies]
        driver = utils.Chrome_Get(ip, config.url)
```

```python
# 配置代理ip,避免触发反爬（有代理ip可以打开）
chrome_options.add_argument('--proxy-server={}'.format(ip))
```

## 选项及其概率

![image-20240406162204144](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406162204144.png)

![image-20240406162237647](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406162237647.png)

![image-20240406162321959](C:\Users\Sunshine\AppData\Roaming\Typora\typora-user-images\image-20240406162321959.png)

 [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)] 

 [(第一个选项, 概率), (第二个选项, 概率), ...........]
