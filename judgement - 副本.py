from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions



username=''
passwd=''



option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
browser = Chrome(options=option)
#browser = webdriver.Chrome()
browser.get("https://passport.bilibili.com/login")
browser.find_element_by_xpath('//input[@placeholder="你的手机号/邮箱"]').send_keys(username)
browser.find_element_by_xpath('//input[@placeholder="密码"]').send_keys(passwd)
browser.find_element_by_xpath('//*[contains(text(),"记住我")]').click()
browser.find_element_by_xpath('//a[text()="登录"]').click()

# 从selenium.common.exceptions模块导入NoSuchElementException异常类
from selenium.common.exceptions import NoSuchElementException
flg=True
while flg:
	sleep(0.3)
	try:
		#element1 = browser.find_element_by_xpath('//span[text()="动画"]')
		element1 = browser.find_element_by_xpath('//a[text()="修改密码"]')
	except NoSuchElementException as e:
		# 打印异常信息
		print("dnmd快滑动验证")
		# 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
		flg = True
	else:
		# 没有发生异常，表示在页面中找到了该元素，返回True
		flg = False
		print("ss")
browser.get("https://www.bilibili.com/judgement/index")
flg=True
while flg:
	sleep(0.3)
	try:
		element1 = browser.find_element_by_xpath('//button[text()="开始众裁"]')
	except NoSuchElementException as e:
		print("等待加载")
		flg = True
	else:
		flg = False
		print("任期总结")
#这里↓如果加载慢了会暴毙
sleep(1)
flg=True
try:
	element1 = browser.find_element_by_xpath('//h2[text()="风纪委员任期总结"]')
except NoSuchElementException as e:
	print(e)
	flg = True
else:
	flg = False
	browser.find_element_by_xpath('//*[@class="dialog-close"]').click()
sleep(0.5)
browser.find_element_by_xpath('//button[text()="开始众裁"]').click()

flg=True
while True:
	sleep(0.5)
	try:
		element1 = browser.find_element_by_xpath('//button[text()="返回风纪委员首页"]')
	except NoSuchElementException as e:
		flg = True
	else:
		try:
			element2 = browser.find_element_by_xpath('//h3[text()="真给力 , 移交众裁的举报案件已经被处理完了"]')
		except NoSuchElementException as e:
			flg = True
			browser.find_element_by_xpath('//button[text()="返回风纪委员首页"]').click()
			break
		else:
			browser.find_element_by_xpath('//button[text()="返回风纪委员首页"]').click()
			print('10')
			sleep(2)
			browser.find_element_by_xpath('//button[text()="开始众裁"]').click()
	try:
		element1 = browser.find_element_by_xpath('//*[@class="legal-btn legal-btn-color"]')
	except NoSuchElementException as e:
		flg = True
	else:
		flg = False
		browser.find_element_by_xpath('//*[@class="legal-btn legal-btn-color"]').click()
		browser.find_element_by_xpath('//*[text()="建议删除"]').click()
		try:
			element1 = browser.find_element_by_xpath('//*[@class="checkbox"]')
		except NoSuchElementException as e:
			flg = True
		else:
			flg = False
			browser.find_element_by_xpath('//*[@class="checkbox"]').click()
		browser.find_element_by_xpath('//*[text()="确认投票"]').click()
		sleep(0.3)
		flg=True
		while flg:
			sleep(0.3)
			try:
				element1 = browser.find_element_by_xpath('//*[text()="开始下一个众裁"]')
			except NoSuchElementException as e:
				print(e)
				flg = True
			else:
				flg = False
				print("众裁+1")
				browser.find_element_by_xpath('//*[text()="开始下一个众裁"]').click()
