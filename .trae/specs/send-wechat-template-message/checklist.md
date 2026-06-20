# Checklist

- [x] `config.example.json` 包含 `app_id`、`app_secret`、`template_id`、`user` 字段
- [x] `config.example.yaml` 包含等价的配置字段
- [x] `send_wechat_template.py` 能够读取并校验 JSON 配置文件
- [x] `send_wechat_template.py` 能够读取并校验 YAML 配置文件
- [x] `send_wechat_template.py` 能够成功获取微信 `access_token`
- [x] `send_wechat_template.py` 能够发送模板消息并处理响应
- [x] 脚本对配置缺失、JSON/YAML 解析错误、网络异常、微信接口错误码都有清晰错误处理
- [x] `requirements.txt` 声明 `requests` 与 `pyyaml` 依赖
- [x] 脚本在 JSON 配置下能成功发送模板消息（或 mock 验证通过）
- [x] 脚本在 YAML 配置下能成功发送模板消息（或 mock 验证通过）
