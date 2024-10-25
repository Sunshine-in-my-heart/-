import random, time, requests, re
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # 导入Chrome选项类
from selenium import webdriver
from selenium.webdriver import ActionChains


#打开浏览器访问网站
def Chrome_Get(ip, url):
    # 创建一个Chrome选项对象
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized')

    # 配置代理ip,避免触发反爬（有代理ip可以打开）
    # chrome_options.add_argument('--proxy-server={}'.format(ip))

    # 配置随机请求头
    user_agent = UserAgent().random
    chrome_options.add_argument(f'user-agent={user_agent}')

    # 初始化Chrome浏览器
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    # 打开网页
    driver.get(url)
    # 手机端首页有填写问卷的打开
    # User_Agent(user_agent, driver)
    return driver

# 模仿人随机等待
def Sleep(start, end):
    time.sleep(random.uniform(start, end))

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

# 手机端单独处理首页按钮
def User_Agent(user_agent, driver):
    if "Android" not in user_agent and "iPhone" not in user_agent:
        pass
    else:
        element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'slideChunkWord'))
            )
        element.click()

# 选择选项
def Chioce_options(elements, type, questions_answers):
    Sleep(0.3, 0.7)
    i = 0
    chioces = []
    print(len(elements))
    if type == 'single':
        chioces = Single_Chioce(questions_answers)
    if type == 'multiple':
        chioces = Multipler_Chioce(questions_answers)
    # if type == 'satisfaction':
    #     chioces = Satisfaction_Chioce(questions_answers)
    for element in elements:
        if chioces[i] == 1:
            element.click()
        i += 1
        # print(i)
        Sleep(0, 0.5)


def Single_Chioce(single_answers):
    exam_answers = {}
    single_numlist = []  # 记录各题选项数
    for question in single_answers:
        single_numlist.append(len(question['options']))
        # 对于单选题，选择一个答案作为正确答案
        total_probability = sum(prob for _, prob in question['options'])
        normalized_options = [(option, prob / total_probability) for option, prob in question['options']]
        correct_answer = random.choices([option for option, _ in normalized_options],
                                        weights=[prob for _, prob in normalized_options],
                                        k=1)[0]
        exam_answers[question['question']] = correct_answer
    print("单选题答案：{}".format(exam_answers))
    return Answer_list(exam_answers, single_numlist)

# 按照概率生成试卷答案
def Multipler_Chioce(multiple_answers):
    multiple_numlist = []  # 记录各题选项数
    exam_answers = {}  # 用于存储问题和答案的字典
    for question in multiple_answers:
        multiple_numlist.append(len(question['options']))
        # 对于多选题，选择至少min_correct个，至多max_correct个答案作为正确答案
        correct_answers = []
        options_with_probabilities = question['options']
        # 确保至少选择一个答案
        correct_answers.append(random.choice([option for option, prob in options_with_probabilities if prob > 0]))
        options_left = [(option, prob) for option, prob in options_with_probabilities if
                        option != correct_answers[-1]]

        # 继续选择答案，直到达到min_correct到max_correct之间的数量
        while len(correct_answers) < len(question['options']):
            if len(correct_answers) >= 2 and random.random() < 0.5:
                # 达到最小正确答案数量后，以50%的概率停止选择更多答案
                break

                # 从剩余选项中随机选择一个作为正确答案
            total_probability = sum(prob for _, prob in options_left)
            normalized_options_left = [(option, prob / total_probability) for option, prob in options_left]
            new_correct_answer = random.choices([option for option, _ in normalized_options_left],
                                                weights=[prob for _, prob in normalized_options_left],
                                                k=1)[0]

            # 确保不重复选择同一个答案
            if new_correct_answer not in correct_answers:
                correct_answers.append(new_correct_answer)
                options_left = [(option, prob) for option, prob in options_left if option != new_correct_answer]
                correct_answers.sort()
                    # 将问题和答案存储在字典中，对于多选题，答案是一个列表
        exam_answers[question['question']] = correct_answers
    print("多选题答案：{}".format(exam_answers))
    return Answer_list(exam_answers, multiple_numlist)

# 满意题
def Satisfaction_Chioce(elements, satisfaction_answers):
    satisfaction_numlist = []  # 记录各题选项数
    exam_answers = {}
    question_num = 1
    i = 0
    for question in satisfaction_answers:
        for minor_question in question['options']:
            satisfaction_numlist.append(len(minor_question))
            total_probability = sum(prob for _, prob in minor_question)
            normalized_options = [(option, prob / total_probability) for option, prob in minor_question]
            correct_answer = random.choices([option for option, _ in normalized_options],
                                            weights=[prob for _, prob in normalized_options],
                                            k=1)[0]
            exam_answers[question_num] = correct_answer
            question_num += 1
    print("满意题答案：{}".format(exam_answers))
    answer_list = Answer_list(exam_answers, satisfaction_numlist)
    for element in elements:
        if answer_list[i] == 1:
            element.click()
        i += 1
        Sleep(0, 0.5)

# 将每个选项转化为0和1的列表方便处理点击动作
def Answer_list(exam_answers, numlist):
    answers_list = [0] * sum(numlist)
    # 选项总数
    num = 0
    i = 0
    # 0为不选，1为选择
    for question, answer in exam_answers.items():
        if isinstance(answer, list):
            for choice in answer:
                answers_list[choice + num] = 1
            num += numlist[i] #加上选项数的索引
        else:
            answers_list[answer+num] = 1
            num += numlist[i] #加上选项数的索引
        i += 1
    # print(answers_list)
    return answers_list

# 填空题按概率填入
def Completion_into(driver, completion_answers):
    for completion in completion_answers:
        question_number = completion['question']  # 获取问题编号
        contents = completion['content']  # 获取内容列表
        probabilitys = completion['probability']
        content = random.choices(contents, weights=probabilitys, k=1)[0]
        element = driver.find_element(By.ID, "q{}".format(question_number))
        element.send_keys(content)
        Sleep(2, 3)

# 点击提交
def Submit(driver):
    submit = driver.find_element(By.ID, 'ctlNext')
    submit.click()

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