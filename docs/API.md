# API 说明

基础地址 `http://127.0.0.1:8000/api`。请求与响应均为 JSON。除健康检查、注册、登录外，所有业务接口均要求 `Authorization: Bearer <access_token>`。完整字段约束见 `/openapi.json`，本机 `/docs` 提供无需外网的接口浏览页。

| 方法 | 路径（省略 /api） | 行为 |
| --- | --- | --- |
| GET | /health | MongoDB 连通性；可用 200，不可用 503 |
| POST | /auth/register | username、password；成功 201，重复 409 |
| POST | /auth/login | 同上；返回 access_token，错误 401 |
| GET | /auth/me | 当前用户 id、username |
| POST | /auth/logout | 删除当前会话 |
| POST | /surveys | 创建草稿，成功 201 |
| GET | /surveys | 当前用户自己的问卷列表 |
| GET | /surveys/{sid} | 创建者问卷详情 |
| PUT | /surveys/{sid} | 替换草稿设置 |
| POST | /surveys/{sid}/publish | 验证结构后发布 |
| POST | /surveys/{sid}/close | 关闭已发布问卷 |
| POST | /surveys/{sid}/questions | 添加题目，成功 201，返回更新后的问卷 |
| PUT | /surveys/{sid}/questions/{qid} | 替换草稿题目，保留 ID 与规则，并重新检查规则 |
| PUT | /surveys/{sid}/questions/{qid}/rules | 替换规则列表，返回更新后的问卷 |
| GET | /fill/{sid} | 填写用公开内容，仍需登录 |
| POST | /fill/{sid}/next | 校验已有路径答案，返回 next_question_id |
| POST | /fill/{sid}/submit | 重新完整校验并保存，成功 201 |
| GET | /surveys/{sid}/responses | 创建者查看答卷；匿名隐藏身份 |
| GET | /surveys/{sid}/stats | 整卷统计 |
| GET | /surveys/{sid}/stats/{qid} | 单题统计 |

未授权 401；他人问卷按 404 处理；过期填写 410；重复提交、不可编辑状态或并发草稿更新冲突 409；不合法字段、规则或答案 422。不存在、未发布、已关闭问卷的填写接口返回 404。

## 账号

用户名为 3～40 位字母、数字、下划线，存储时转小写；密码 8～128 字符。密码使用每人随机盐与 PBKDF2-HMAC-SHA256，600000 次迭代。令牌有效期 12 小时，退出立即失效。

## 创建与编辑问卷

```json
{"title":"课堂调查","description":"说明","anonymous":true,"allow_multiple":false,"deadline":"2026-12-31T23:59:00+08:00"}
```

deadline 可为 null。时间必须包含时区。PUT 是全量设置替换，未传的可选字段恢复默认值；题目不在此接口替换。返回 id、share_url、status、questions 等。分享路径为 `/survey/{sid}`。

## 添加题目

```json
{"title":"喜欢哪些水果","type":"multiple","required":true,
 "options":[{"id":"apple","label":"苹果"},{"id":"pear","label":"梨"}],
 "min_choices":1,"max_choices":2}
```

支持 single、multiple、text、number。通用字段 title、type、required；文本 min_length / max_length；数字 min_value / max_value / integer。精确选择 N 项设置 min_choices=max_choices=N。填空题 options 必须为空。题目 ID 由服务端生成。

## 配置规则

```json
{"rules":[{"op":"contains_any","value":["apple"],"target":"后面题目的UUID"}]}
```

单选使用 eq+选项ID；多选使用 contains_any 或 contains_all+选项ID数组；数字使用 eq、gt、gte、lt、lte+数字。target 为后续题目 ID 或字符串 END。空 rules 数组清空规则。规则按数组顺序，首个匹配生效。

## 填写与提交

```json
{"answers":{"题目UUID1":"apple","题目UUID2":["apple","pear"],"题目UUID3":"反馈","题目UUID4":18}}
```

next 与 submit 使用相同数据格式。next 接受已经回答的路径前缀，返回 path、answers（规范化非空答案）、next_question_id。END 表示可提交。选答留空时应显式传 null，表示已访问并跳过此题；否则 next 会停在尚未回答的题目。submit 验证完整路径，拒绝跳过题目或未知题目的额外答案。不能依赖前端返回的 path 绕过校验。

## 统计字段

整卷返回 survey_id、total_responses、questions。单题包含 question_id、title、type、answer_count；选择题 options 含 id、label、count；填空题 values 为答案列表；数字另含 average，无答案时为 null。单题接口附加 total_responses。

统计以答卷为单位，不按用户去重：若允许同一用户多次提交，单选选项人数代表该选项对应的有效答卷数。未回答或被跳过不计入 answer_count；多选每份答卷同一选项最多计一次。
