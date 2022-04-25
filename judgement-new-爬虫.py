from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import re
import time
import json


ROOT_PATH = ".\\pl\\"
EXT='.csv'

COOKIE_PATH=r".\cookies.txt"
AUTO_SAVE_COOKIE=True

USER_NAME = ''
PASSWD = ''


option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
browser = Chrome(options=option)
#browser = webdriver.Chrome()

def loginUseAccount():
    browser.get("https://passport.bilibili.com/login")
    browser.find_element_by_xpath('//input[@placeholder="你的手机号/邮箱"]').send_keys(USER_NAME)
    browser.find_element_by_xpath('//input[@placeholder="密码"]').send_keys(PASSWD)
    browser.find_element_by_xpath('//*[contains(text(),"记住我")]').click()
    sleep(1)
    browser.find_element_by_xpath('//a[text()="登录"]').click()
    count=0;
    while True:
        sleep(1)
        try:
            element1 = browser.find_element_by_xpath('//span[text()="动画"]')
            #element1 = browser.find_element_by_xpath('//a[text()="修改密码"]')
        except NoSuchElementException as e:
            print("dnmd快验证")
        else:
            print("ss")
            break
    browser.get("https://www.bilibili.com/judgement/index")
    if AUTO_SAVE_COOKIE is True:
        with open(COOKIE_PATH,'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(browser.get_cookies()))


def loginUseCookie():
    browser.get("https://www.bilibili.com/judgement/index")
    browser.delete_all_cookies()
    with open(COOKIE_PATH,'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        for cookie in cookies_list:
            browser.add_cookie(cookie)
    browser.refresh()


def get_comments(browser,link):
    browser.get(link)
    sleep(1)
    #判断众议结果倾向
    population_name_list=['positive_num','neutral_num','negative_num','undetermined_num','huikan_num','buhuikan_num']
    population_dic={}
    for i in range(0,6):
        population_dic[population_name_list[i]] = int(re.search("\d+",browser.find_elements_by_xpath('//span[@class="b_fade fs_5"]')[i].text).group())
    max_name=population_name_list[0]
    for i in range(1,4):
        if population_dic[max_name]<population_dic[population_name_list[i]]:
            max_name=population_name_list[i]
    browser.find_element_by_xpath('//button[@class="b-btn-fade mt_lg v-btn v-btn--plain v-btn--block v-btn--round v-btn--info v-btn--large"]').click()#查看更多按钮
    sleep(0.5)
    js='document.getElementsByClassName("v-dialog__body")[0].scrollBy(0,5000)'
    #向下滚动至加载全部完成
    while True:
        text_nomore=browser.find_elements_by_xpath('//p[@class="b_fade fs_5 text_center mt_xl mb_xl"]')[1].text #没有更多观点了
        if not(text_nomore is ""):
            break
        browser.execute_script(js)
        sleep(0.2)
    
    comment_div_list=browser.find_elements_by_xpath('//div[@class="fjw-point-item mb_sm"]/div[@class="item-content"]')#每条评论的div
    comment_list=[]#（评论，赞同，反对）
    for i in comment_div_list:
        comment_list.append((i.find_element_by_xpath('./p[@class="b_text content-message"]').text,int(i.find_element_by_xpath('./p/span[@class="thumb-item mr_lg"]').text),int(i.find_element_by_xpath('./p/span[@class="thumb-item"]').text)))
    return (max_name,comment_list)


def get_all_comment(browser,link_list):
    comment=[]
    k=0
    for i in link_list:
        sleep(10)
        k=k+1
        print(str(k)+"/"+str(len(link_list)))
        try:
            comment.append(get_comments(browser,i))
        except Exception as e:
            print('get link error,retry at end: ' + i)
            link_list.append(i)
    return comment


def save_comment(comments):
    comment_lines={'positive_num':[],'neutral_num':[],'negative_num':[],'undetermined_num':[]}
    weight=(2,1,-2)
    for page in comments:
        max_name=page[0]
        for comment in page[1]:
            comment_lines[max_name].append(comment[0] + ',' + str(weight[0]+comment[1]*weight[1]+comment[2]*weight[2])+'\n')
    for name in comment_lines.keys():
        if comment_lines[name]==[]:
            continue
        f=open(ROOT_PATH+name+EXT,'w',encoding='utf-8')
        f.writelines(comment_lines[name])
        f.close()




loginUseCookie()

element1 = browser.find_elements_by_xpath('//div[@class="fjw-case-item"]/a')
new_case_list=[]
for i in element1:
    new_case_list.append(i.get_attribute("href"))

comments=get_all_comment(browser,new_case_list)
save_comment(comments)


