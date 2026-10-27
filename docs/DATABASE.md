# MongoDB 集合设计

数据库默认 `survey_system`，由环境变量 `MONGODB_DATABASE` 配置。连接由 `MONGODB_URI` 配置。使用 PyMongo 同步驱动，FastAPI 同步路由在线程池中执行。没有关系数据库或内存数据库替代实现。

## 集合与索引

| 集合 | 主要字段 | 索引与用途 |
| --- | --- | --- |
| users | _id（UUID字符串）、username、salt、password_hash、created_at | _id 默认唯一；username 唯一，阻止并发重复注册 |
| surveys | _id、owner_id、title、description、anonymous、allow_multiple、deadline、status、questions、revision、schema_version、created_at | owner_id，用于查询自己的问卷 |
| responses | _id、survey_id、respondent_id、answers、path、created_at、schema_version、once_key（按配置存在） | survey_id 用于统计；once_key 部分唯一索引，仅约束字符串字段，保证每人一次 |
| sessions | _id（令牌 SHA-256）、user_id、expires_at | expires_at TTL 索引，自动清除过期会话；认证同时主动校验时间 |

所有业务记录均写入 MongoDB。会话令牌原文只返回浏览器，浏览器 sessionStorage 保存会话凭据，不保存业务数据库。所有时间使用 UTC，界面按浏览器本地时区显示。

## 问卷文档示例

```json
{
  "_id": "survey-uuid",
  "owner_id": "owner-uuid",
  "title": "课堂调查",
  "description": "演示数据驱动跳转",
  "anonymous": true,
  "allow_multiple": false,
  "deadline": null,
  "status": "draft",
  "revision": 2,
  "schema_version": 1,
  "questions": [{
    "id": "question-uuid",
    "title": "年龄",
    "type": "number",
    "required": true,
    "options": [],
    "min_choices": 0,
    "max_choices": null,
    "min_length": 0,
    "max_length": 1000,
    "min_value": 0,
    "max_value": 120,
    "integer": true,
    "rules": [{"op":"lt", "value":18, "target":"END"}]
  }]
}
```

`created_at`、`deadline` 在 MongoDB 中是 BSON Date，示例省略创建时间。问卷和题目由后端生成 UUID，编辑不改变 ID；选项 ID 由编辑者指定并校验唯一，最多 64 个字母、数字、下划线或短横线。单问卷最多 100 题，每题最多 100 个选项、50 条跳转规则。

## 答卷文档示例

```json
{
  "_id":"response-uuid",
  "survey_id":"survey-uuid",
  "respondent_id":"user-uuid",
  "answers":{"question-uuid":16},
  "path":["question-uuid"],
  "once_key":"survey-uuid:user-uuid",
  "schema_version":1
}
```

答案按题目 ID 存储，不依赖题目位置。单选为选项 ID 字符串，多选为不重复 ID 数组，文本为字符串，数字为 JSON 数字。选答空值不会进入 answers；path 记录访问过的题目。允许多次填写时不写 once_key，每次提交生成新答卷 ID。

## 设计理由与扩展

题目、校验条件和规则嵌入问卷：填写时一次读取完整结构，修改题目可以进行单文档原子更新。用户、答卷独立成集合，避免问卷文档随答卷数量无限膨胀。题目使用稳定 ID，题目顺序只负责默认路由，不承担关联键用途。

这里没有照搬关系数据库的题目表、选项表、规则表和多层关联表；不同题型有不同结构，MongoDB 的嵌入文档与数组直接表达这一结构。引用用户和问卷 ID 提供必要关联，避免在每份答卷中重复存储整份问卷。发布后冻结结构，保证历史答案含义不变。

第一阶段用 Pydantic 与业务函数校验写入结构，未设置 MongoDB `$jsonSchema`；直接用数据库管理工具写入错误数据不在 API 保障范围内。第二阶段保留 schema_version，新增结构应编写迁移脚本、保留稳定 ID、先备份并验证旧数据兼容性。

## 匿名边界

匿名问卷仍必须登录。数据库内部保留 respondent_id，以支持同一用户一次填写限制。创建者的答卷详情通过显式字段白名单输出，不返回 respondent_id、once_key 或用户名；统计查询只读取 answers。这里的匿名是对问卷创建者隐藏身份，不是对数据库管理员不可追溯。用户自己在文本答案中填写姓名等信息，系统不会自动识别或删除。
