# 微信测试号模板消息发送脚本 Spec

## Why
为了自动化每周 trae 任务的状态通知，需要一个独立的 Python 脚本，能够读取微信测试号配置并调用微信模板消息接口发送通知。

## What Changes
- 新增 `send_wechat_template.py` 脚本，负责读取配置、获取 access_token、发送模板消息。
- 新增 `config.example.json` 配置文件模板，包含 `app_id`、`app_secret`、`template_id`、`user` 字段。
- 新增 `config.example.yaml` 配置文件模板，作为 YAML 格式示例。
- 修改 `send_wechat_template.py`，使其同时支持 JSON 与 YAML 配置文件，并根据文件扩展名自动选择解析器。
- 更新 `requirements.txt`，新增 `pyyaml` 依赖。

## Impact
- 仅新增独立脚本和配置文件，不影响现有代码。
- 未来可由 TRAE 的自动化任务（work 端）调用该脚本完成每周通知。

## ADDED Requirements

### Requirement: 读取配置
脚本 SHALL 从指定的 JSON 或 YAML 配置文件中读取 `app_id`、`app_secret`、`template_id`、`user`。根据文件扩展名 `.json`、`.yaml`、`.yml` 自动选择解析器。

#### Scenario: 正常读取
- **WHEN** 配置文件存在且包含所有必填字段
- **THEN** 脚本成功加载配置并继续执行

#### Scenario: 配置缺失
- **WHEN** 配置文件不存在或必填字段缺失
- **THEN** 脚本打印清晰的错误信息并以非零状态码退出

#### Scenario: 格式错误
- **WHEN** JSON 或 YAML 配置文件格式非法
- **THEN** 脚本打印解析错误信息并以非零状态码退出

### Requirement: 获取微信 access_token
脚本 SHALL 使用 `app_id` 和 `app_secret` 调用微信接口获取 `access_token`。

#### Scenario: 获取成功
- **WHEN** 凭据有效
- **THEN** 成功获取 `access_token` 并进入发送流程

#### Scenario: 凭据无效或请求失败
- **WHEN** 微信接口返回错误码或网络异常
- **THEN** 脚本打印错误详情并以非零状态码退出

### Requirement: 发送模板消息
脚本 SHALL 使用 `access_token`、`template_id`、`user` 向指定用户发送模板消息。

#### Scenario: 发送成功
- **WHEN** 所有参数有效
- **THEN** 微信接口返回成功，脚本打印成功信息并以零状态码退出

#### Scenario: 发送失败
- **WHEN** 模板 ID 无效、用户未关注或其他接口错误
- **THEN** 脚本打印微信返回的错误码和错误信息并以非零状态码退出

### Requirement: 错误处理与日志
脚本 SHALL 对配置读取、网络请求、JSON 解析、微信接口返回错误等情况进行捕获并输出可读的日志。

## MODIFIED Requirements
无

## REMOVED Requirements
无
