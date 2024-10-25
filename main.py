from selenium.webdriver.common.by import By
import config, utils

if __name__ == "__main__":
    # ip_list = utils.Get_Api(config.api)
    # print(ip_list)
    ip = 1
    for copies in range(config.copies_num):
        # ip = ip_list[copies]
        driver = utils.Chrome_Get(ip, config.url)
        satisfaction_elements = driver.find_elements(By.XPATH, ".//a[@class='rate-off rate-offlarge']")
        utils.Satisfaction_Chioce(satisfaction_elements, config.satisfaction_answers)
        single_elements = driver.find_elements(By.CLASS_NAME, 'jqradio')
        utils.Chioce_options(single_elements, 'single', config.singe_answers)
        multiple_elements = driver.find_elements(By.CLASS_NAME, 'jqcheck')
        utils.Chioce_options(multiple_elements, 'multiple', config.multiple_answers)
        # print(len(single_elements))
        utils.Sleep(1, 3)
        utils.Completion_into(driver, config.Completion_answers)
        utils.Submit(driver)
        # utils.Verification(driver)
        utils.Sleep(4, 5)
        driver.quit()
        print("已填写{}份".format(copies+1))
