"""
 copyrigth: ICOVETOUS
 time: 2024-01-16 10:27:14
 version: 2.0.0
 language: python3.9
 system: windows10
 editor: PyCharm
 --- description ---
 此程序用于「教学管理服务平台」的自动评教
 --- warning ---
 此程序需要安装 selenium 包
"""

import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

'''登录信息'''
# 用户名(学号)
username = ''
# 密码
password = ''

'''「教学管理服务平台」登录入口'''
# 登录页
login_url = 'https://jw.qlu.edu.cn/jwglxt/xtgl/login_slogin.html'

''' 操作间隔 '''
interval = 0.3


class Connection:
    # 初始化加载
    def __init__(self):
        # 当前浏览器驱动对象
        self.driver = webdriver.Chrome()

    ''' 登录「教学管理服务平台」 '''
    def login(self):
        self.driver.get(login_url)
        print(' 开始登录 QLU一号通系统(教学管理信息服务平台)...')
        while True:
            try:
                # 输入账号
                xpath_u = '/html/body/div[2]/div/div/div[2]/div/div/form/div[2]/div/input'
                self.driver.find_element(By.XPATH, xpath_u).clear()
                self.driver.find_element(By.XPATH, xpath_u).send_keys(username)
                sleep(interval)

                # 输入密码
                xpath_p = '/html/body/div[2]/div/div/div[2]/div/div/form/div[3]/div/input[2]'
                self.driver.find_element(By.XPATH, xpath_p).clear()
                self.driver.find_element(By.XPATH, xpath_p).send_keys(password)
                sleep(interval)

                # 点击登录
                xpath_b = '/html/body/div[2]/div/div/div[2]/div/div/form/div[5]/button'
                self.driver.find_element(By.XPATH, xpath_b).click()
                sleep(interval)

                # 判断是否登录成功
                if 'login' not in self.driver.current_url:
                    print('「教学管理服务平台」登录成功！')
                    print("当前界面为:", self.driver.current_url)
                    break
                else:
                    print('「教学管理服务平台」登录失败，正在重试...')
                    sleep(interval * 3)

            except Exception as exception:
                print("Error:", exception, "「教学管理服务平台」登录失败，当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 进入「教学评价」->「学生评价」页面 '''
    def enter_evaluation_page(self):
        print(' 进入「教学评价」->「学生评价」页面...')
        while True:
            try:
                # 首页
                index_url = self.driver.current_url

                # 进入「教学评价」页面
                xpath_teaching_evaluation = '/html/body/div[3]/div/nav/ul/li[5]/a'
                self.driver.find_element(By.XPATH, xpath_teaching_evaluation).click()
                sleep(interval)

                # 进入「学生评价」页面
                xpath_student_evaluation = '/html/body/div[3]/div/nav/ul/li[5]/ul/li[1]/a'
                self.driver.find_element(By.XPATH, xpath_student_evaluation).click()
                sleep(interval)

                # 切换窗口到「学生评价」页面
                self.driver.switch_to.window(self.driver.window_handles[-1])

                if self.driver.current_url != index_url:
                    print(' 进入「教学评价」->「学生评价」页面成功！')
                    print("当前界面为:", self.driver.current_url)
                    break
                else:
                    print('「教学评价」->「学生评价」页面进入失败，正在重试...')
                    sleep(interval * 3)

            except Exception as exception:
                print("Error:", exception, "「教学评价」->「学生评价」页面进入失败，当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 开始「学生评价」 '''
    def evaluation(self):
        print(' 正在「学生评价」...')
        while True:
            try:
                # 将分页设置为最大
                xpath_max_page_select = '/html/body/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[' \
                                 '5]/div/table/tbody/tr/td[2]/table/tbody/tr/td[8]/select'
                self.driver.find_element(By.XPATH, xpath_max_page_select).click()

                xpath_max_page_option = f"{xpath_max_page_select}/option[last()]"
                self.driver.find_element(By.XPATH, xpath_max_page_option).click()
                sleep(interval)

                # 教师 table
                xpath_table = "/html/body/div[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[3]/div[3]/div/table"
                table = self.driver.find_element(By.XPATH, xpath_table)
                trs = table.find_elements(By.TAG_NAME, 'tr')
                table_length = len(trs)

                # 遍历教师 table 点击每行评价每人
                for i in range(1, table_length):
                    # 点击每一行
                    xpath_tr = f"{xpath_table}/tbody/tr[{i + 1}]"  # 替换成你的选择器
                    script = f"document.evaluate('{xpath_tr}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, " \
                             f"null).singleNodeValue.click();"
                    self.driver.execute_script(script)
                    sleep(interval)

                    # 读取出所有需评价的 table
                    xpath_div = '/html/body/div[2]/div/div/div[3]/div[2]/div'
                    div = self.driver.find_element(By.XPATH, xpath_div)
                    tables = div.find_elements(By.TAG_NAME, 'table')

                    # 确定并错开前两个选项 使所选选项不会出现完全相同的情况
                    flag = 1

                    # 遍历每个 table
                    for table in tables:
                        trs = table.find_elements(By.TAG_NAME, 'tr')
                        # tr 遍历
                        for tr in trs:
                            tds = tr.find_elements(By.TAG_NAME, 'td')
                            # 选择项
                            select_num = -1
                            # td 遍历
                            for td in tds:
                                # 如果文字中包含「停课次数」或「作业次数」
                                if '停课次数' in td.get_attribute('innerHTML'):
                                    # 选择 第4项
                                    select_num = 3
                                if '作业次数' in td.get_attribute('innerHTML'):
                                    # 选择 第1项
                                    select_num = 0

                                if 'radio' in td.get_attribute('innerHTML'):
                                    # 选择input中的 随机 第1项或第2项
                                    if select_num == -1:
                                        select_num = random.choice([0, 1])

                                    if flag >= 0:
                                        select_num = flag
                                        flag -= 1

                                    td.find_elements(By.TAG_NAME, 'input')[select_num].click()

                    # 点击 保存 按钮
                    xpath_save = '/html/body/div[2]/div/div/div[3]/div[2]/div/div[3]/form/div[2]/div[' \
                                 '2]/div/div/div/button[1]'
                    self.driver.find_element(By.XPATH, xpath_save).click()
                    sleep(interval)

                    # 点击 确定 按钮
                    xpath_confirm = '/html/body/div[5]/div/div/div[3]/button'
                    self.driver.find_element(By.XPATH, xpath_confirm).click()
                    sleep(interval * 5)

                    print(' 第「', i, '」个教师评价成功！')

                print(' 「学生评价」完成！')
                break
            except Exception as exception:
                print("Error:", exception, "「学生评价」错误，当前界面为:", self.driver.current_url)
                sleep(interval * 3)
                continue

    ''' 退出 '''
    def finish(self):
        # self.driver.quit()
        pass


if __name__ == '__main__':
    print('--> START...')

    con = Connection()
    try:
        # 登录
        con.login()
        # 进入评教页面
        con.enter_evaluation_page()
        # 开始评教
        con.evaluation()
    except Exception as e:
        print(e)
    finally:
        con.finish()

    print('...END <--')
