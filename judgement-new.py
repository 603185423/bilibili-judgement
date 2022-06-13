from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
import json
from snownlp import SnowNLP


COOKIE_PATH = r".\cookies.txt"
AUTO_SAVE_COOKIE = True

USER_NAME = ''
PASSWD = ''

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
browser = Chrome(options=option)
#browser = webdriver.Chrome()

def loginUsePasswd():
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
            f.write(json.dumps(browser.get_cookies()))


def loginUseCookie():
    browser.get("https://www.bilibili.com/judgement/index")
    browser.delete_all_cookies()
    with open(COOKIE_PATH,'r') as f:
        cookies_list = json.load(f)
        for cookie in cookies_list:
            browser.add_cookie(cookie)
    browser.refresh()



loginUseCookie()




while True:
    sleep(0.3)
    try:
        element1 = browser.find_element_by_xpath('//button[@class="btn-action b-btn-blue-old v-btn v-btn--primary v-btn--large"]')#开始众议按钮
    except NoSuchElementException as e:
        print("等待加载")
    else:
        print("任期总结")
        break



def get_comment(browser):
    sleep(0.5)
    js='document.getElementsByClassName("v-dialog__body")[0].scrollBy(0,5000)'
    #向下滚动至加载全部完成
    while True:
        text_nomore=browser.find_elements_by_xpath('//p[@class="b_fade fs_5 text_center mt_xl mb_xl"]')[1].text #没有更多观点了
        if text_nomore == "没有更多观点了":
            break
        browser.execute_script(js)
        sleep(0.2)
    comment_div_list=browser.find_elements_by_xpath('//div[@class="fjw-point-item mb_sm"]/div[@class="item-content"]')#每条评论的div
    comment_list=[]#（评论，赞同，反对）
    for i in comment_div_list:
        comment_list.append((i.find_element_by_xpath('./p[@class="b_text content-message"]').text,int(i.find_element_by_xpath('./p/span[@class="thumb-item mr_lg"]').text),int(i.find_element_by_xpath('./p/span[@class="thumb-item"]').text)))
    return comment_list



def calc_comment_seg(comment_list):
    if comment_list==[]:
        return 0
    num=0
    seg=0
    for i in comment_list:
        weight=(2+1*i[1]-2*i[2])#权重：自身+2，赞同+1，反对-2
        s=SnowNLP(i[0]).sentiments
        seg=seg+s*weight
        #print(s)
        num=num+weight
    seg=seg/num
    print(seg)
    if seg>0.6:
        return 1
    elif seg<0.4:
        return -1
    else:
        return 0


sleep(0.5)
element1.click()
count=0
while True:
    sleep(5)
    try:
        browser.find_element_by_xpath('//button[@class="btn-action v-btn v-btn--info v-btn--large"]')#投票次数已用完
    except NoSuchElementException as e:
        print()
    else:
        print("投票次数已用完")
        break
    try:
        browser.find_elements_by_xpath('//span[@class="b_fade fs_5 point-title-open"]')[0].click()#展开
        sleep(0.5)
        pos=0
        try:
            browser.find_elements_by_xpath('//button[@class="b-btn-fade mt_lg v-btn v-btn--plain v-btn--block v-btn--round v-btn--info v-btn--large"]')[0].click()#查看更多
            sleep(0.5)
            pos=calc_comment_seg(get_comment(browser))
            browser.find_elements_by_xpath('//span[@class="b-icon-close"]')[0].click()#叉叉
            sleep(0.5)
        except:
            try:
                browser.find_elements_by_xpath('//span[@class="b-icon-close"]')[0].click()#叉叉
            except:
                pos=1
            pos=1
        if pos==1:
            browser.find_elements_by_xpath('//button[@class="btn-vote mt_sm v-btn v-btn--plain v-btn--round v-btn--info v-btn--medium"]')[0].click()#好
        elif pos==0:
            browser.find_elements_by_xpath('//button[@class="btn-vote mt_sm v-btn v-btn--plain v-btn--round v-btn--info v-btn--medium"]')[1].click()#一般
        elif pos==-1:
            browser.find_elements_by_xpath('//button[@class="btn-vote mt_sm v-btn v-btn--plain v-btn--round v-btn--info v-btn--medium"]')[2].click()#差
        else:
            browser.find_elements_by_xpath('//button[@class="btn-vote mt_sm v-btn v-btn--plain v-btn--round v-btn--info v-btn--medium"]')[3].click()#无法判断
        #browser.find_elements_by_xpath('//button[@class="btn-vote mt_sm v-btn v-btn--plain v-btn--round v-btn--info v-btn--medium"]')[0].click()#好
        sleep(0.5)
        browser.find_elements_by_xpath('//button[@class="btn-vote mt_sm v-btn v-btn--plain v-btn--round v-btn--info v-btn--small"]')[1].click()#不会观看
        sleep(0.5)
        browser.find_elements_by_xpath('//div[@class="v-check-box__text"]')[0].click()#匿名发布
        sleep(0.5)
        browser.find_elements_by_xpath('//div[@class="vote-submit"]/button')[0].click()#确认提交
        while True:
            sleep(0.5)
            try:
                browser.find_element_by_xpath('//button[@class="b-btn-blue result-btn v-btn v-btn--round v-btn--primary v-btn--large"]').click()#开始下一个
            except NoSuchElementException as e:
                print("等待加载3")
            else:
                count = count+1
                print(str(count)+'/20')
                break
    except NoSuchElementException as e:
        print("等待加载2")



