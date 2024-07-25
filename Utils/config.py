import os
from json import JSONDecodeError
from pathlib import Path
from typing import List, Union, Dict

import yaml
from pydantic import BaseModel, ValidationError, validator

from Utils.data_model import *
from Utils.logger import log

ROOT_PATH = Path(__name__).parent.absolute()

DATA_PATH = ROOT_PATH / "data"
'''数据保存目录'''

CONFIG_PATH = DATA_PATH / "config.yaml"  # if os.getenv("_CONFIG_PATH") is None else Path(
# os.getenv("_CONFIG_PATH"))
"""数据文件默认路径"""


class ServerChan(BaseModel):
    default_title: str = ""
    notify: bool = True
    serverchan_url: str = ""
    merge_message: bool = False


class UptimeKuma(BaseModel):
    url: str = "http://000.000.000.000:0000"
    token: str = "xXxXxXxXx"
    interval: int = -1


class Account(BaseModel):
    username: str = ""
    passwd: str = ""
    cookies: str = ""


class Preference(BaseModel):
    auto_save_cookies: bool = True
    login_use_password: bool = False
    notify: bool = True
    serverchan: ServerChan = ServerChan()
    uptime_kuma: UptimeKuma = UptimeKuma()


class Config(BaseModel):
    preference: Preference = Preference()
    """偏好设置"""
    account: List[Account] = [Account()]
    """账号设置"""


def write_plugin_data(data: Config = None):
    """
    写入插件数据文件

    :param data: 配置对象
    """
    try:
        if data is None:
            data = ConfigManager.data_obj
        try:
            # str_data = orjson.dumps(data.dict(), option=orjson.OPT_PASSTHROUGH_DATETIME |
            # orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2)
            str_data = yaml.dump(data.model_dump(), indent=4, allow_unicode=True, sort_keys=False)
        except (AttributeError, TypeError, ValueError):
            log.exception("数据对象序列化失败，可能是数据类型错误")
            return False
        with open(CONFIG_PATH, "w") as f:
            f.write(str_data)
        return True
    except OSError:
        return False


class ConfigManager:
    data_obj = Config()
    """加载出的插件数据对象"""
    platform = "pc"
    """运行环境"""

    @classmethod
    def load_config(cls):
        """
        加载插件数据文件
        """
        if os.path.exists(DATA_PATH) and os.path.isfile(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as file:
                    data = yaml.safe_load(file)
                new_model = Config.model_validate(data)
                for attr in new_model.model_fields:
                    ConfigManager.data_obj.__setattr__(attr, new_model.__getattribute__(attr))
                write_plugin_data(ConfigManager.data_obj)  # 同步配置
            except (ValidationError, JSONDecodeError):
                log.exception(f"读取数据文件失败，请检查数据文件 {CONFIG_PATH} 格式是否正确")
                raise
            except Exception:
                log.exception(
                    f"读取数据文件失败，请检查数据文件 {CONFIG_PATH} 是否存在且有权限读取和写入")
                raise
        else:
            try:
                if not os.path.exists(DATA_PATH):
                    os.mkdir(DATA_PATH)
                write_plugin_data()
            except (AttributeError, TypeError, ValueError, PermissionError):
                log.exception(f"创建数据文件失败，请检查是否有权限读取和写入 {CONFIG_PATH}")
                raise
            log.info(f"数据文件 {CONFIG_PATH} 不存在，已创建默认数据文件。")


ConfigManager.load_config()
