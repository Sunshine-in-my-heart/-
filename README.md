![read](https://github.com/user-attachments/assets/fe4a27a8-7acf-477a-9051-c6129ad17139)
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

**列表长度对应几个选项，重点检查**

概率可以是1:1:1，也可以是10:10:10，也可以是10:20:30

```
# 单选题
singe_answers = [
    {
        'question': 1,
        'type': '单选题',
        'options': [(0, 200), (1, 10)]
    },
    {
        'question': 2,
        'type': '单选题',
        'options': [(0, 94), (1, 106)]
    },
    {
        'question': 3,
        'type': '单选题',
        'options': [(0, 10), (1, 20), (2, 30), (3, 40)]
    },.......
]

multiple_answers = [
    {
        'question': 15,
        'type': '多选题',
        'options': [(0, 25), (1, 25), (2, 15), (3, 15), (4, 20)]
    },
    {
        'question': 19,
        'type': '多选题',
        'options': [(0, 30), (1, 20), (2, 10), (3, 15), (4, 25)]
    }
]

# 满意度题型
satisfaction_answers = [
    {
        'question': 19,
        'type': 'satisfaction',
        'options': [
            [(0, 1), (1, 1), (2, 2), (3, 4), (4, 2)],
            [(0, 1), (1, 2), (2, 3), (3, 2), (4, 2)],
            [(0, 1), (1, 2), (2, 2), (3, 3), (4, 2)],
            [(0, 1), (1, 1), (2, 2), (3, 4), (4, 2)],
            [(0, 2), (1, 3), (2, 2), (3, 2), (4, 1)],
            [(0, 3), (1, 2), (2, 2), (3, 2), (4, 1)],
            [(0, 2), (1, 3), (2, 2), (3, 2), (4, 1)],
            [(0, 1), (1, 1), (2, 2), (3, 2), (4, 4)],
            [(0, 1), (1, 1), (2, 1), (3, 3), (4, 4)],
            [(0, 1), (1, 1), (2, 2), (3, 2), (4, 4)],
            [(0, 2), (1, 3), (2, 2), (3, 2), (4, 1)],
            [(0, 1), (1, 1), (2, 2), (3, 4), (4, 2)],
            [(0, 1), (1, 1), (2, 1), (3, 3), (4, 4)],
            [(0, 1), (1, 1), (2, 2), (3, 4), (4, 2)],
            [(0, 2), (1, 1), (2, 4), (3, 2), (4, 1)],
            [(0, 1), (1, 1), (2, 2), (3, 2), (4, 4)],
            [(0, 1), (1, 1), (2, 1), (3, 4), (4, 3)],
            [(0, 4), (1, 2), (2, 2), (3, 1), (4, 1)],
            [(0, 1), (1, 2), (2, 4), (3, 2), (4, 1)],
            [(0, 1), (1, 1), (2, 1), (3, 4), (4, 3)]
        ]
    }
]
```

## 填空题概率

填空题

'probability': [2, 2, 2, 2, 202]每个答案对应概率

```python
Completion_answers = [
    {
        'question': 20,
        'content': ["基础设施不齐全", "服务不好", "加快旅游温泉基础设施改造", "提升旅游服务质量", ""],
        'probability': [2, 2, 2, 2, 202]
    }
]
```

# 智能验证

如果出现滑块认证，则打开，这个项目在测试过程中未出现

```python
# utils.Verification(driver)
```

```python
# 智能验证
def Verification(driver):
    # 请点击智能验证码进行验证！
    try:
        comfirm = driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a')
        comfirm.click()
        time.sleep(1)
    except Exception as e:
        print(e)

    # 点击按钮开始智能验证
    try:
        button = driver.find_element(By.XPATH, '//*[@id="SM_BTN_WRAPPER_1"]')
        button.click()
        time.sleep(0.5)
    except Exception as e:
        print(e)

    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        time.sleep(0.3)
        if str(slider.text).startswith("请按住滑块，拖动到最右边"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
            time.sleep(1)
    except Exception as e:
        print(e)
```
