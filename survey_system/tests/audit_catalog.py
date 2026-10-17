"""Human-reviewed mapping of existing assertions to course requirements.

Values: categories, steps, inputs, expected. Parametrized data are added by pytest.
This catalog describes existing tests; it does not change their assertions.
"""
LEGACY = {
    "test_health": (["其他"], "GET /api/health。", "无请求体。", "200，返回的数据库名以 survey_system_test_ 开头。"),
    "test_auth": (["其他"], "注册登录、检查身份、错误登录、重复注册、查看密码字段、退出并复查。", "alice/password123；错误密码incorrect。", "认证200；未登录/错误密码/退出后401；重复409；数据库仅存密码哈希。"),
    "test_ownership": (["其他"], "在测试库插入所有者a的问卷s；分别使用a/b调用owned。", "survey_id=s，owner_id=a。", "a读取成功；b抛HTTPException且状态404。"),
    "test_management": (["创建问卷"], "注册两用户；创建、查分享链接、越权查询、编辑、空问卷发布；测试库植入占位题再发布关闭。", "课堂调查→修改标题；用户alice/bobby；占位题q1。", "创建201；分享路径匹配；越权404/空列表；空问卷发布422；发布published；发布后编辑409；关闭closed。此用例使用直接写库占位题，不能单独证明加题API完整。"),
    "test_deadline": (["创建问卷"], "创建无时区时间；创建带时区过去时间；测试库植入占位题并发布。", "2020-01-01T12:00:00与2020-01-01T12:00:00Z。", "无时区创建422；带时区过去时间可存草稿，但发布422。"),
    "test_add_edit": (["添加题目"], "建草稿；添加文本题；改为数字题并比较ID；添加无选项单选。", "姓名/text→年龄/number/integer=true；single无options。", "添加201；编辑保持原题ID；无选项单选422。此用例未独立断言编辑请求状态码。"),
    "test_invalid": (["答案校验"], "用QuestionInput构造题目；对指定输入调用validate_answer。", "完整题目q与value见各实例参数。", "抛HTTPException。原断言未验证异常状态码或具体消息；新增API测试补充422与零写入断言。"),
    "test_valid": (["答案校验"], "分别验证选答空值、数字上边界、中文文本精确长度。", "required=false/null；整数0～120输入120；2字文本输入中文。", "分别返回None、120、中文。"),
    "test_jump": (["跳转逻辑"], "构造带规则题与被跳过题；检查规则；完整walk；再加入路径外答案。", "kind/op/value/answer见实例参数；命中目标END；路径外题skip。", "匹配路径仅[q]；包含skip答案时抛HTTPException。"),
    "test_bad_target": (["跳转逻辑"], "构造数字题q，设置gt 0规则到目标，调用validate_rules。", "target=q或missing。", "自跳/不存在目标均抛HTTPException。"),
    "test_rule_persistence": (["跳转逻辑"], "通过API创建问卷、数字题、规则，然后读取MongoDB。", "lt 18→END。", "配置规则200；数据库rules与请求一致。"),
    "test_submit": (["提交问卷"], "发布匿名数字问卷；检查未登录读取、next、非法提交、合法提交、再次提交；创建者/他人读取答卷。", "必答整数0～120；200→20→21；独立filler用户。", "读取未登录401；next首题；非法422；合法201；重复409；仅一答卷，隐藏respondent、respondent_id、once_key；他人详情404。注意原用例401针对读取，不是提交。"),
    "test_repeated": (["提交问卷"], "根据多次配置发布；同用户提交10、20；关闭后提交30。", "multiple和expected见实例参数。", "首次201；第二次按配置201或409；关闭后404。"),
    "test_page": (["其他"], "请求首页、分享页面和脚本。", "/、/survey/example、/static/app.js。", "均200，仅验证路由可达，不代表人工浏览器验收。"),
    "test_statistics": (["统计结果"], "添加四题并发布；查空统计；提交两份完整答卷；查全卷、数字单题及越权统计。", "single:a/b；multiple:[a,b]/[b]；text:甲/乙；number:10/20；允许多次。", "空总数0且均值null；提交各201；总数2；单选[1,1]、多选[1,2]、文本[甲,乙]、数字均值15；数字单题count2；越权整卷/单题404。"),
    "test_concurrent_submit": (["提交问卷"], "每人一次问卷；4线程同用户同时提交；查询库数量。", "数字答案30，共4次并发。", "状态码排序[201,409,409,409]；数据库仅1条答卷。"),
    "test_expired": (["提交问卷"], "发布后在测试库设置已过期时间；读取与提交；查询答卷数量。", "deadline=now-1秒；数字10。", "读取/提交410；答卷0。时间状态由测试库直接设置，未等待真实时间。"),
    "test_full_jump_workflow": (["跳转逻辑", "提交问卷", "统计结果"], "通过API创建3题；设置首题跳第三题；发布；尝试改规则；逐题next、提交、读库和统计。", "年龄number、职业text、反馈text；年龄lt18跳反馈；答案16/很好。", "发布200；发布后改409；next为第三题；提交201；answers/path不含职业；职业count0、反馈values[很好]。"),
    "test_edit_invalidates_rule": (["跳转逻辑"], "数字题配置gt规则；改题型为文本；重新读取。", "gt10→END；number→text。", "编辑422；题型仍number。"),
    "test_schema_rejects": (["添加题目", "答案校验"], "直接构造QuestionInput，不通过HTTP；以pytest.raises检查。", "非法kwargs见各参数实例。", "抛ValueError：文本上下限、数字上下限、选项ID重复、多选最少超出选项数。"),
    "test_missing_unknown_and_priority": (["跳转逻辑", "答案校验"], "构造两条同时匹配的规则；完整walk；再传未知题或缺失必答。", "number q：gt0→END优先于gt0→later；答案q=1/unknown=1/q=0。", "首匹配路径[q]；未知题与缺少later必答均抛HTTPException。"),
    "test_real_name_details": (["提交问卷"], "发布实名问卷；filler填写；创建者读详情。", "anonymous=false；数字22。", "详情respondent.username=filler。原用例没有独立断言提交状态。"),
    "test_offline_docs": (["其他"], "读取/docs、OpenAPI；扫描本地静态文件。", "5个本地资源文件。", "docs200；schema含单题统计路径与QuestionInput；静态文件没有外部http链接。"),
    "test_documentation_present": (["其他"], "检查7份文档存在且长度大于100；检查.env.example。", "DATABASE/API/LOGIC/MANUAL_TESTS/REPORT_TEMPLATE/AI_USAGE_LOG/TEST_RESULTS。", "文档非空且环境示例含MONGODB_URI；仅检查存在性，不证明文档业务覆盖。"),
}
