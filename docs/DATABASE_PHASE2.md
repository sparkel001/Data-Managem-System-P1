# 第二阶段新增数据结构与兼容性

本文仅记录相对于[第一阶段数据库说明](DATABASE.md)的新增或变更内容。users、sessions、surveys、responses及原问卷题目结构保留；旧文稿原样保存，不回写新增说明。

## 题库扩展集合

题库扩展保留基础四集合，另使用以下三个集合，不使用旁路集合。

| 集合 | 核心字段 | 说明与索引 |
|---|---|---|
| question_banks | _id、owner_id、name、description、created_at | 题库元信息；owner_id索引；仅所有者管理 |
| bank_questions | _id、owner_id、bank_ids[]、shared_with[]、created_at | _id是题目族ID；bank_ids支持多题库归属；shared_with保存被授权用户ID；三个查询字段各有索引 |
| question_versions | _id、question_id、version_no、parent_version_id、restored_from_version_id、content、content_hash、request_key、request_hash、created_at | _id是不可变版本ID；question_id指题目族；(question_id,version_no)和(question_id,request_key)唯一索引 |

三个新集合使用MongoDB `$jsonSchema`检查必需字段及主要类型；完整题型约束复用应用层 `QuestionInput`。应用仅插入版本，不提供覆盖或删除版本的接口；数据库管理员直接修改不属于不可变API的保障范围。

`content`严格等于 `QuestionInput.model_dump()`，不含问卷内ID、规则或source。`content_hash`为规范JSON（键排序、紧凑分隔、UTF-8）的SHA-256。父版本支持分支；恢复记录被恢复版本并创建新的版本ID与序号。最新版本通过最大序号读取，不设置跨文档可变指针，避免版本已提交而指针未更新的问题。版本号表示创建顺序，不代表问卷自动采用。

问卷内保存完整扁平快照，保留 `id`、题型/约束、`rules`，新增可选字段：

```json
{"source":{"question_id":"题目族UUID","version_id":"不可变版本UUID","content_hash":"SHA256"}}
```

问卷内`id`是每次复用生成的新UUID。答案键、path、跳转目标继续使用这个实例ID。草稿换版保持实例ID，先验证整卷规则再以revision条件原子写入；已发布和已关闭问卷不可换版。旧问卷无source，照常读取和填写，迁移不补写来源。

跨问卷查询先按当前用户owner_id过滤问卷，再按source关联；同版本多实例增加回答次数，答卷总数按响应ID去重。按version_id分组，即使hash一致也不合并恢复版本。数值统计返回原答案、平均值和精确值频数分布。统计验证快照摘要，发现不一致返回409。

## 本阶段的MongoDB设计理由

题目族、版本和问卷内实例分开管理，因为三者生命周期不同：题目族负责归属与共享，版本文档保存历史内容，问卷则嵌入完整快照并用source记录版本来源。填写时直接读取问卷快照，无需逐题查询版本集合；版本更新也不会自动改变既有问卷和答卷。

MongoDB嵌入文档适合保存问卷题目、约束和跳转规则，独立的答卷及版本集合避免历史记录不断扩大同一个问卷文档。版本与快照通过稳定ID关联，由应用层维护一致性，不依赖数据库外键。版本不可变由应用的只插入接口及校验逻辑保障，不能由数据库结构单独推导；跨问卷统计按version_id分组，避免不同语义版本直接混算。

## 结构验证与初始化

题库三个集合由app/migrations.py设置MongoDB的$jsonSchema基础类型校验，完整题型复用QuestionInput。原四集合维持原字段和应用层校验。初始化只新增集合和索引，不补写旧问卷source；幂等与失败处理见[MIGRATION_PHASE2.md](MIGRATION_PHASE2.md)。

## 用户名唯一性维护

注册将用户名转为小写，服务端预查询用于明确提示；启动和新增注册前确认完整username唯一索引，数据库约束负责阻止并发重复。重复用户名或DuplicateKeyError返回409及“用户名已存在”。历史重复或索引冲突时不删除用户、不替换索引：已有用户名注册返回409，新用户名注册返回503；健康接口返回503、status=degraded、registration=blocked。登录遇到多条同名记录时拒绝随机选择账号，其余不重复账号沿用原流程，不主动注销现有会话。

以下为管理员维护指引；这些维护步骤未执行，相关数据库状态未核实。

1. 确认网页对应的实际服务进程、MONGODB_URI/MONGODB_DATABASE和目标库。暂停新增账号，备份users及其关联数据，不直接删除任意同名记录。
2. 确认目标库后执行只读检查：

```javascript
use survey_system
db.users.getIndexes()
db.users.aggregate([
  {$group: {_id: "$username", count: {$sum: 1}, user_ids: {$push: "$_id"}}},
  {$match: {count: {$gt: 1}}}
])
```

3. 按每个_id核实账号归属以及surveys.owner_id、responses.respondent_id、sessions.user_id、题库owner_id及共享用户ID引用。不凭创建时间、密码哈希或记录顺序判断可以删除。
4. 管理员与账号所有者确认处理方案后，可为冲突账号分配未占用的小写用户名，保留_id和关联数据。该操作须先审阅再执行；程序不自动改名、合并或重写引用。缺失、非字符串username和大小写不规范记录也须核查；普通字符串唯一索引区分大小写，规范化前必须检查转换后的冲突，不能批量直接覆盖。
5. 若username_1为非唯一或不完整索引，单独评估转换或重建方案，程序不自动删除索引。处理数据及索引冲突后，重启新版服务或下一次新用户注册会重试建立约束，不需要删除数据库。
6. 用getIndexes核对unique=true且无sparse/partialFilterExpression限制；确认健康接口恢复200，再在测试环境复验重复及并发注册。一次注册成功不足以证明约束正确；运行中的旧服务须重新加载代码。

修复过程与历史测试证据见[第二阶段AI日志](AI_USAGE_PHASE2.md)。开发库冲突的实际成因、人工处理及索引建立状态未核实，不因代码测试通过而宣称已经修复开发数据。


## 从问卷保存可复用题目

集合结构保持不变。新复制题目可增加`bank_questions.copied_from={survey_id,instance_id,content_hash}`用于记录来源；不向原surveys或responses写回字段。新族标识由复制者、问卷、实例及内容摘要确定。同内容重试、跨题库保存只保留一个题目族及初版。草稿内容修改后再次复制会成为独立题目，不覆盖先前复制的内容。

对于已有自有来源题，复用其原题目族和已有版本历史，追加题库归属；原问卷所用旧版本仍保留在历史中，不将旧内容覆盖到最新版本。题库列表按最新版本展示，具体历史内容在版本页面查看。规则不复制，因为其目标依赖原问卷实例。

自动化证据仅验证隔离测试库，实际运行库状态与验收边界见[MIGRATION_PHASE2.md](MIGRATION_PHASE2.md)。

