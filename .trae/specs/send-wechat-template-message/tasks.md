# Tasks

- [x] Task 1: 创建配置文件模板 `config.example.json`
  - [x] 包含 `app_id`、`app_secret`、`template_id`、`user` 四个必填字段
  - [x] 字段说明清晰，便于用户复制为 `config.json` 后填写真实值

- [x] Task 2: 实现 `send_wechat_template.py` 脚本
  - [x] 支持通过命令行参数或默认路径指定配置文件
  - [x] 读取并校验 JSON 配置，缺失字段时报错退出
  - [x] 调用微信 `token` 接口获取 `access_token`，处理网络异常和微信错误码
  - [x] 调用微信模板消息发送接口，处理响应和错误码
  - [x] 所有步骤输出可读日志，错误时返回非零退出码

- [x] Task 3: 添加 `requirements.txt`
  - [x] 声明 `requests` 依赖

- [x] Task 4: 验证脚本
  - [x] 使用无效配置验证错误处理路径
  - [x] 在有效配置下测试发送流程（可用微信测试号真机或本地 mock 服务）
