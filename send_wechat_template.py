#!/usr/bin/env python3
"""向微信测试号发送模板消息。"""

import argparse
import json
import sys
from pathlib import Path

import requests

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"
REQUIRED_CONFIG_FIELDS = ["app_id", "app_secret", "template_id", "user"]


def load_config(config_path: str) -> dict:
    """加载并校验 JSON 配置文件。"""
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"配置文件不存在: {path.absolute()}")

    try:
        with path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"配置文件 JSON 格式错误: {exc}") from exc

    missing = [field for field in REQUIRED_CONFIG_FIELDS if field not in config]
    if missing:
        raise ValueError(f"配置文件缺少必填字段: {', '.join(missing)}")

    return config


def get_access_token(app_id: str, app_secret: str) -> str:
    """调用微信接口获取 access_token。"""
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret,
    }
    try:
        response = requests.get(TOKEN_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"获取 access_token 网络请求失败: {exc}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"解析 access_token 响应失败: {exc}") from exc

    if "errcode" in data:
        errcode = data.get("errcode")
        errmsg = data.get("errmsg", "未知错误")
        raise RuntimeError(f"微信接口返回错误 (获取 access_token): errcode={errcode}, errmsg={errmsg}")

    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError("微信接口未返回 access_token")

    return access_token


def send_template_message(access_token: str, user: str, template_id: str, data: dict | None = None) -> dict:
    """调用微信接口发送模板消息。"""
    payload = {
        "touser": user,
        "template_id": template_id,
        "data": data if data is not None else {},
    }
    url = f"{SEND_URL}?access_token={access_token}"

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"发送模板消息网络请求失败: {exc}") from exc

    try:
        result = response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"解析发送模板消息响应失败: {exc}") from exc

    if result.get("errcode"):
        errcode = result.get("errcode")
        errmsg = result.get("errmsg", "未知错误")
        raise RuntimeError(f"微信接口返回错误 (发送模板消息): errcode={errcode}, errmsg={errmsg}")

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="向微信测试号发送模板消息")
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="配置文件路径 (默认: config.json)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        print(f"[1/3] 读取配置文件: {args.config}", flush=True)
        config = load_config(args.config)
        print("[1/3] 配置文件加载成功", flush=True)

        print("[2/3] 获取微信 access_token...", flush=True)
        access_token = get_access_token(config["app_id"], config["app_secret"])
        print("[2/3] access_token 获取成功", flush=True)

        print("[3/3] 发送模板消息...", flush=True)
        data = config.get("data", {"result": {"value": "测试消息", "color": "#173177"}})
        result = send_template_message(
            access_token,
            config["user"],
            config["template_id"],
            data,
        )
        print(f"[3/3] 模板消息发送成功: {result}", flush=True)
        return 0

    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
