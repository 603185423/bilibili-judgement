# bilibili_judgement

风纪委员投票，使用[selenium](https://github.com/seleniumhq/selenium)调用Chrome浏览器，投票结果从众议观点的评论中使用[snowNLP](https://github.com/isnowfy/snownlp)计算情感倾向,如果没有观点，则投默认票<br><br>
**学习项目，请勿滥用！如果有因滥用造成的封号、删除账户等情况或违反相关法律所造成的责任，本人所有的风险都由使用者一律承担，作者一概不负责！**<br>**请仔细阅读脚本源码，保管好自己的cookie、用户名、密码，请勿将带有相关信息的文件交给任何人！**

## 特别声明:
* 本仓库发布的项目中涉及的任何脚本、代码，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.

* 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

* 作者以及其他项目贡献者(如果有)对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

* 间接使用脚本的任何用户在某些行为违反国家/地区法律或相关法规的情况下进行传播, 作者以及其他项目贡献者(如果有)对于由此引起的任何隐私泄漏或其他后果概不负责.

* 请勿将该项目的任何内容用于商业或非法目的，否则后果自负.

* 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，本人将在收到认证文件后删除相关脚本.

* 以任何方式查看此项目的人或直接或间接使用该项目的任何脚本的使用者都应仔细阅读此声明。603185423保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或项目的规则，则视为您已接受此免责声明.

***您使用或者复制了本仓库且本人制作的任何脚本，则视为`已接受`此声明，请仔细阅读*** 


## 使用：
* 使用python3.12或以上版本
* 克隆或下载本项目，使用`pip install selenium`安装依赖
* 自行安装 `Chrome` 与 `Chrome Driver`
* 运行脚本(`judgement-new.py`), 待出现自动生成配置的提示后结束脚本
* 手动结束脚本后修改自动生成的配置文件(`data/config.yaml`)
* 运行脚本(`judgement-new.py`)

## 如何登陆阿b的账号

1. 首次登陆，或者cookie失效后登录（使用账号密码登陆并自动**保存cookie**）：
* 将`data/config.yaml`中的 `login_use_password` 改成 `true` ，并确保 `auto_save_cookies = true`
* 运行脚本，按照提示登陆
2. 使用cookie登陆
* 如已经**保存cookie**，将`data/config.yaml`中的 `login_use_password` 改成 `false` 即可
* 如未保存cookie，则使用1中的方法登陆，或者自行抓取 `SESSDATA`、`bili_jct`、`DedeUserID` 三个值填入 `cookies` 字段 (需要`str(base64.b64encode(json.dumps(browser.get_cookies()).encode('utf-8')), 'utf-8')`)

## 如何自己训练情感分析文件
1. 爬取评论
* 确保该账号下有大量的新版风纪委员众议记录(建议超过400条以上)，并且所有的案件状态为已结束
* 登入账号部分如上
* 运行 `judgement-new-爬虫.py` 文件的前半部分代码(运行至126行`loginUseCookie()`结束)
* 等待界面加载完毕
* 下拉网页，至所有的新版案件记录加载完毕
* 运行剩下代码
* 等待代码运行完毕（由于b站的反爬虫策略，爬取两个案件的评论区间隔时间已设置为10秒）
* 如果因为网络波动等原因造成获取评论失败，该案件将会在队列最后被重试，未设置重试次数上限
* 如果大量连续显示 `get link error,retry at end: http://xxxxxxxxx` 则为触发b站反爬虫策略的表现，不用管，一直挂着就行了，等时间过了就能正常获取评论了
* 代码执行完毕后，会将评论保存在 `./pl/` 中
2. 筛选评论
* 上述代码会根据案件最后的定性，将评论分别保存成三种情感对应的三个文件
* 请自行对评论去重，筛选，将评论正确的分类，并保存为 `neg.txt` 和 `pos.txt` 两个文件（无法判断类型的评论不需要）
3. 训练与替换文件
* 请参考[snowNLP](https://github.com/isnowfy/snownlp)中[README.md](https://github.com/isnowfy/snownlp/blob/master/README.md)文件的[关于训练](https://github.com/isnowfy/snownlp/blob/master/README.md#%E5%85%B3%E4%BA%8E%E8%AE%AD%E7%BB%83)部分内容

## 关于SnowNLP
本代码使用的`SnowNLP`修改了`sentiment`目录下的`训练文件`以及对应的`__init__.py`，如需要更新SnowNLP,请自行修改

## 有其他问题请在issue中提问
我一定~~不~~会回复的

## License

GPL licensed.
