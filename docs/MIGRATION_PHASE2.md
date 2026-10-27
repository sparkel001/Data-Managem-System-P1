# 题库结构迁移与兼容性

本文说明题库扩展的初始化范围、执行条件、幂等机制和失败处理。实现为`app/migrations.py:migrate`，只创建question_banks、bank_questions、question_versions及其验证规则和索引，不修改原四集合的文档，不为旧题目自动补source。

## 运行方式

在项目根目录查看迁移计划，命令不会建立数据库连接：

```powershell
.\.venv\Scripts\python.exe -m scripts.migrate_phase2 --database survey_system
```

实际执行需`--apply`；非`survey_system_test_<32位UUID>`目标另需`--allow-development`。连接地址读取MONGODB_URI，数据库名必须显式传入。应用启动也调用相同函数，因此启动应用会初始化配置目标库，并非只读检查。既有环境变更前应确认目标和备份。现有验证证据仅来自独立UUID测试库，未证明实际运行库的初始化状态或迁移验收情况。应用启动会调用迁移函数，因此缺少手动迁移命令记录不代表既有运行库从未初始化。

## 重复执行与中断恢复

每个建集合及建索引操作独立幂等。已存在集合必须具有相同validator；不一致时停止，不通过collMod改写。索引冲突也报错，不删除原索引。中途中断后再次执行继续完成剩余步骤，不用提前完成的标志掩盖部分失败。

版本的(question_id,version_no)和(question_id,request_key)唯一索引支持并发及幂等请求。插入已成功但确认丢失时，同键同请求重试返回原版本，同键不同内容拒绝。

## 旧数据兼容

无source的问卷继续执行原编辑、发布、填写、跳转及统计，不自动把相似题认作同一族。用户可在题库页面从自己的问卷复制题目，无需手工重录；该操作不会给源问卷回填source，原问卷仍不纳入该题目族的跨问卷统计。新草稿导入指定版本后才具有明确来源。

users、sessions、surveys、responses不由此迁移改写。用户索引保障是独立初始化逻辑，历史重复数据的保留与维护见[数据模型](DATABASE_PHASE2.md#用户名唯一性维护)。

## 回退边界

旧应用不会管理新增集合，但含source的快照若经旧编辑入口修改，无法保障来源一致性。因此回退须结合备份和只读范围评估，不能删除新增集合或答卷作为回退手段。数据库备份与源码备份用途不同，源码存档不能恢复业务数据。

## 验证依据

[完整用例](TEST_CASES_PHASE2.md)中的P2-AUTO-140（test_additive_repeat_legacy）与P2-AUTO-141（test_migration_retry_and_validation）对应`tests/test_phase2_block1.py`，验证迁移重复执行、旧文档不变、故障恢复及结构校验。这些断言只验证隔离UUID测试库中的行为，不是实际运行库的迁移验收；版本并发及确认丢失重试见`tests/test_phase2_block3.py`和`tests/test_phase2_boundaries.py`。原始分块结果位于test-results/phase2，最新已保存全量证据位于test-results/submission-20261027。上述结果限定于历史隔离测试环境，不能外推实际运行库的状态。
