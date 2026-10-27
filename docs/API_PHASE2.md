# 第二阶段新增与变更API

本文仅说明相对于第一阶段的新增接口及行为变更。原接口定义保存在未经修改的[第一阶段API](API.md)，当前运行以本页列明的变更为准；完整动态结构可在本机`/openapi.json`查看。

## 认证与响应格式的变化

新注册密码由独立RegistrationCredentials限制为8～16个字符，登录Credentials仍支持8～128字符，兼容已有长密码。密码按Unicode码点计数；随机盐、PBKDF2及会话格式不变。注册页面独立，确认密码仅在前端检查，不发送给后端；注册成功回到登录，不自动创建会话。

## 题库、版本、共享与跨问卷接口

所有新接口需要 `Authorization: Bearer <token>`。无登录401；不存在或无权限404；请求模型/题型/跳转非法422；幂等冲突、非草稿或内容摘要不一致409。外层和题目内容模型均禁止额外字段。

| 方法与路径 | 输入/返回 | 权限 |
|---|---|---|
| POST /api/question-banks | {name,description?} → 题库，201 | 登录用户创建 |
| GET /api/question-banks | 自有题库列表 | 仅本人 |
| PUT /api/question-banks/{bid} | {name,description?} → 更新题库 | 题库所有者 |
| GET /api/question-banks/{bid}/questions | 题目族及latest_version | 题库所有者 |
| POST /api/question-banks/{bid}/questions | {content:QuestionInput,request_key} → 题目族及初版，201 | 题库所有者 |
| PUT /api/question-banks/{bid}/questions/{qid} | 将自有题目加入自有题库 | 两者所有者 |
| DELETE /api/question-banks/{bid}/questions/{qid} | 移出，不删除族或版本 | 两者所有者 |
| GET /api/bank-questions | 自有题目族列表（含无题库归属） | 本人 |
| GET /api/shared-questions | 分享给我的题目 | 共享接收人 |
| GET /api/bank-questions/{qid} | 题目族及最新版本 | 所有者或共享接收人 |
| GET /api/bank-questions/{qid}/versions | 按创建顺序的全部版本历史 | 所有者或共享接收人 |
| GET /api/bank-questions/{qid}/versions/{vid} | 指定版本 | 同上 |
| POST /api/bank-questions/{qid}/versions | {content,request_key,parent_version_id} → 新版本，201 | 仅所有者；可指定任意本族父版本形成分支 |
| POST /api/bank-questions/{qid}/versions/{vid}/restore | {request_key,parent_version_id} → 复制vid的新版本，201 | 仅所有者 |
| POST /api/surveys/{sid}/library-questions | {question_id,version_id} → 带新快照的问卷，201 | 草稿所有者且有题库读取权 |
| PUT /api/surveys/{sid}/questions/{instance_id}/version | {question_id,version_id} → 换版后的问卷 | 同上，仅同题目族 |
| POST /api/bank-questions/{qid}/shares | {username} → {ok:true} | 仅所有者 |
| GET /api/bank-questions/{qid}/shares | 已授权用户名列表 | 仅所有者 |
| DELETE /api/bank-questions/{qid}/shares/{username} | 幂等撤销 | 仅所有者 |
| GET /api/bank-questions/{qid}/usages | survey_id/title/status/instances[] | 仅显示本人问卷；持有自己快照时撤销分享后仍可查 |
| GET /api/bank-questions/{qid}/stats?version_id=可选 | 总答卷数、groups[]；每组含版本ID、摘要、问卷数、实例数、答卷数、回答数及题型统计 | 只统计本人问卷；共享不扩大统计权限 |

版本创建、分支、恢复和初次保存需要调用方生成稳定 `request_key`；网络重试必须复用原键和同一请求体。同键不同内容409。初次保存的键作用域为本人+题库；后续版本为题目族。恢复需要显式父版本，以保证重试不因“当前最新”发生变化而改变语义。题库编辑和归属操作不改变内容版本。

旧 `PUT /api/surveys/{sid}/questions/{qid}` 对无source的第一阶段题目保持原行为；对新增题库快照返回409并提示通过版本入口更新，防止内容与来源错配。发布、填写、提交、整卷统计和单题统计接口不变。所有规则和答案仍使用问卷内实例ID。



## 注册约束与降级响应

POST /api/auth/register：重复用户名（含新注册输入大小写变体）和并发重复键均返回409、detail=用户名已存在；无法建立唯一索引时返回503和维护提示，不插入新用户。POST /api/auth/login：若同名历史记录超过1条，返回409并要求管理员处理。GET /api/health：缺少完整username唯一索引时返回503、status=degraded、registration=blocked。其他接口和成功响应不变。


## 问卷题目保存到题库与中文错误响应

- `GET /api/bank-questions?exclude_bank_id={bid}`：可选排除已加入指定题库的题目；必须拥有该题库。仅返回自有、已有有效版本的题目。
- `POST /api/question-banks/{bid}/from-survey`：请求为`{"survey_id":"问卷编号","instance_id":"问卷内题目编号"}`。必须同时拥有问卷和目标题库。返回`question`、`added`和中文`message`。复制题目内容，剔除问卷内标识、来源及跳转规则。
- `PUT /api/question-banks/{bid}/questions/{qid}`：保留原操作，追加`added`和中文`message`。已存在时`added=false`，明确提示无需重复加入。

同一用户反复复制同一问卷题目的相同内容，以确定性题目族标识复用，不反复增加初版；复制到不同题库也只增加归属。原来源确属本人且版本内容相符时直接复用该题目族，不覆盖已有版本。来源属于其他人时，从自己问卷中的快照生成自有题目，不获得修改原题的权限。

请求校验错误仍为422，但detail改为中文提示，不再返回含英文msg/loc的校验数组。答案校验保留内部question_id/message结构供程序使用，前端仅展示message。数据库及未知异常返回中文JSON错误，技术堆栈仅记录于服务端日志。状态码仍遵循HTTP规范，页面不展示状态码或原始异常。

