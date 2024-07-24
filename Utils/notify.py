import threading
import time
from abc import ABC, abstractmethod
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from Utils.config import ConfigManager
from Utils.logger import log

config = ConfigManager().data_obj


class NotificationSender:
    def __init__(self):
        self.lock = threading.Lock()
        self.notifications = []
        self.api_url = config.preference.serverchan.serverchan_url
        self.timer = threading.Timer(30, self.send_notifications)
        self.timer.start()

    def send_notification(self, title, desp):
        if not config.preference.serverchan.notify:
            return
        with self.lock:
            self.notifications.append((title, desp))

    def send_notifications(self):
        if not self.api_url:
            return
        with self.lock:
            if self.notifications:
                title = config.preference.serverchan.default_title
                desp = '\n'.join(f"{t}:{d}" for t, d in self.notifications)
                data = {"title": title, "desp": desp}
                session = requests.Session()
                retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
                session.mount('http://', HTTPAdapter(max_retries=retries))
                session.mount('https://', HTTPAdapter(max_retries=retries))
                try:
                    response = session.post(self.api_url, data=data)
                    log.info("通知已发送")
                except Exception as e:
                    log.error("发送通知时出现异常：", str(e))
            self.notifications = []
        # 重置定时器
        self.timer = threading.Timer(30, self.send_notifications)
        self.timer.start()

    def stop(self):
        self.timer.cancel()


# 单例模式实例化
sender_instance = NotificationSender()


class Heartbeat(ABC):
    def __init__(self, interval: int):
        """
        初始化心跳基类。
        :param interval: 发送心跳的时间间隔（秒）
        """
        self.interval: int = interval
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def start(self):
        """
        启动心跳线程。
        """
        if self.interval < 0:
            return
        with self.lock:
            if not self.running:
                self.running = True
                self.thread = threading.Thread(target=self._run)
                self.thread.daemon = True  # Set as a daemon, so it will be killed once the main thread is dead.
                self.thread.start()

    def stop(self):
        """
        停止心跳线程。
        """
        with self.lock:
            self.running = False
            if self.thread:
                self.thread.join()
                self.thread = None

    def _run(self):
        """
        运行一个持续发送心跳的线程。
        """
        while self.running:
            self.beat()
            time.sleep(self.interval)

    @abstractmethod
    def beat(self):
        """
        必须由子类实现的方法，用于发送心跳。
        """
        pass


# 例如，实现一个具体的心跳类
class UptimeKuma(Heartbeat):
    def __init__(self, url: str, token: str, interval: int, status: str = "up", msg: str = "OK"):
        super().__init__(interval)
        self.url = url
        self.token = token
        self.status = status
        self.msg = msg

    def update_status(self, status: str, msg: str):
        """
        更新要发送的心跳状态和消息。
        :param status: 新的心跳状态
        :param msg: 新的心跳消息
        """
        self.status = status
        self.msg = msg

    def beat(self):
        """
        发送心跳到UptimeKuma服务器。
        """
        api_endpoint = f"{self.url}/api/push/{self.token}?status={self.status}&msg={self.msg}"
        try:
            response = requests.get(api_endpoint)
            response.raise_for_status()  # Raise an HTTPError on bad status
            log.info(f"Heartbeat sent successfully! Status code: {response.status_code}")
        except requests.RequestException as e:
            log.error(f"Failed to send heartbeat: {e}")


# 单例模式实例化
beat_instance = UptimeKuma(config.preference.uptime_kuma.url, config.preference.uptime_kuma.token, config.preference.uptime_kuma.interval)


# 使用
def send_notification(title, desp):
    sender_instance.send_notification(title, desp)


def beat_once():
    beat_instance.beat()
