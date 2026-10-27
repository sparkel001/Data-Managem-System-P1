// Library views extend the existing dashboard and question editor.
function actions(selector, fn) {
  root.querySelectorAll(selector).forEach(button => button.onclick = async () => {
    try { await fn(button); } catch (error) { message(error.message, true); }
  });
}
function familyCards(items) {
  return items.map(q => `<section><h2>${esc(q.latest_version?.content.title || '尚未完成保存')}</h2>
    <p>${q.owned ? '我的题目' : '共享题目'} · ${esc(q.latest_version ? 'V'+q.latest_version.version_no : '')}</p>
    <button data-family="${esc(q.id)}">版本与使用情况</button></section>`).join('') || '<p>暂无题目。</p>';
}
async function banksHome() {
  const [banks, own, shared] = await Promise.all([api('/question-banks'), api('/bank-questions'), api('/shared-questions')]);
  root.innerHTML = `<button id="back" class="secondary">我的问卷</button><h1>题库与共享题目</h1>
    <button id="newBank">新建题库</button><div>${banks.map(b => `<section><h2>${esc(b.name)}</h2><p>${esc(b.description)}</p>
    <button data-bank="${esc(b.id)}">打开题库</button><button data-bank-edit="${esc(b.id)}" class="secondary">编辑题库</button></section>`).join('')}</div>
    <h2>我的全部题目（含已移出题库的题目）</h2>${familyCards(own)}<h2>分享给我的题目</h2>${familyCards(shared)}`;
  bind('back', 'click', dashboard); bind('newBank', 'click', () => bankForm());
  actions('[data-bank]', b => bankView(b.dataset.bank));
  actions('[data-bank-edit]', b => bankForm(banks.find(x => x.id === b.dataset.bankEdit)));
  actions('[data-family]', b => familyView(b.dataset.family));
}
function bankForm(bank=null) {
  root.innerHTML = `<h1>${bank ? '编辑' : '创建'}题库</h1><section><form id="bankForm">
    <label>名称<input id="bankName" required maxlength="200" value="${esc(bank?.name)}"></label>
    <label>说明<textarea id="bankDescription" maxlength="3000">${esc(bank?.description)}</textarea></label>
    <button>保存题库</button><button type="button" id="back" class="secondary">返回</button></form></section>`;
  bind('back', 'click', banksHome);
  bind('bankForm', 'submit', async () => {
    await api('/question-banks'+(bank?'/'+bank.id:''), bank?'PUT':'POST', {
      name:document.querySelector('#bankName').value, description:document.querySelector('#bankDescription').value});
    await banksHome();
  });
}
async function bankView(bid) {
  const [items, candidates] = await Promise.all([
    api('/question-banks/'+bid+'/questions'), api('/bank-questions?exclude_bank_id='+encodeURIComponent(bid))]);
  root.innerHTML=`<button id="back" class="secondary">所有题库</button><h1>题库题目</h1>
    <section><h2>从问卷中保存题目</h2><p>问卷里的题目不会自动出现在题库中。可以从自己的草稿、已发布或已关闭问卷复制题目，无需重新填写；原问卷和答卷保持不变。</p>
    <button id="copyFromSurvey">从我的问卷选择题目</button></section>
    <section><h2>加入已有题库题目</h2><p>这里列出您已保存为可复用题目、但尚未加入当前题库的题目。加入只改变所属题库，不新建题目或覆盖版本。别人分享的题目可在“题库与共享”的共享列表中查看并选入问卷。</p>
    ${candidates.length?`<form id="membership"><label>可加入的题目<select id="existingFamily">${candidates.map(q=>`<option value="${esc(q.id)}">${esc(q.latest_version.content.title)}</option>`).join('')}</select></label><button>加入当前题库</button></form>`:
    '<p id="noCandidates">没有可加入的题库题目：您还没有保存可复用题目，或已有题目都已加入此库。可使用上方“从我的问卷选择题目”，也可在下方创建新题目。</p>'}</section>
    <section><h2>编写全新题目</h2><p>需要一道新题时，在这里填写题干、选项和作答要求。问卷中已有的题目请直接使用上方的复制功能。</p><button id="newBankQuestion">创建新题目</button></section>
    <h2>当前题库中的题目</h2>${items.map(q=>`<section><h3>${esc(q.latest_version?.content.title||'题目尚未完成保存')}</h3><button data-family="${esc(q.id)}">版本与使用情况</button>
    <button data-remove-family="${esc(q.id)}" class="secondary">移出题库</button></section>`).join('')||'<p>此题库还没有题目，请选择上方任一种方式添加。</p>'}`;
  bind('back','click',banksHome);
  bind('copyFromSurvey','click',()=>copySurveyView(bid));
  bind('newBankQuestion','click',()=>{
    const key=crypto.randomUUID();
    editQuestion(null,null,async content=>{
      await api('/question-banks/'+bid+'/questions','POST',{content,request_key:key});
      await bankView(bid);message('新题目已保存到题库。');
    },()=>bankView(bid));
  });
  bind('membership','submit',async()=>{
    const id=document.querySelector('#existingFamily').value;
    if(!id) throw Error('请选择要加入的题库题目。');
    const result=await api(`/question-banks/${bid}/questions/${id}`,'PUT');
    await bankView(bid);message(result.message);
  });
  actions('[data-family]',b=>familyView(b.dataset.family));
  actions('[data-remove-family]',async b=>{
    await api(`/question-banks/${bid}/questions/${b.dataset.removeFamily}`,'DELETE');
    await bankView(bid);message('已从此题库移出，题目历史和已有问卷均保留。');
  });
}
async function copySurveyView(bid) {
  const surveys=await api('/surveys');
  const selectable=surveys.filter(s=>s.questions.length);
  root.innerHTML=`<button id="back" class="secondary">返回题库</button><h1>从我的问卷保存题目</h1>
    <p>复制题干、题型、选项和校验设置。跳转规则只适用于原问卷，不会复制到题库。重复保存同一份题目内容不会生成重复题目。</p>
    ${selectable.length?`<label>选择问卷<select id="sourceSurvey"><option value="">请选择问卷</option>${selectable.map(s=>`<option value="${esc(s.id)}">${esc(s.title)}（${surveyStatus(s.status)}）</option>`).join('')}</select></label><div id="sourceQuestions"></div>`:
    '<section><p>您的问卷中还没有可复制的题目。可以返回题库创建新题目，或先在“我的问卷”中添加题目。</p><button id="mySurveys">前往我的问卷</button></section>'}`;
  bind('back','click',()=>bankView(bid));bind('mySurveys','click',dashboard);
  bind('sourceSurvey','change',()=>{
    const survey=selectable.find(s=>s.id===document.querySelector('#sourceSurvey').value);
    document.querySelector('#sourceQuestions').innerHTML=survey?survey.questions.map(q=>`<section><h2>${esc(q.title)}</h2>${questionDescription(q)}<button data-copy-question="${esc(q.id)}">保存到当前题库</button></section>`).join(''):'';
    actions('[data-copy-question]',async button=>{
      button.disabled=true;
      try {
        const result=await api('/question-banks/'+bid+'/from-survey','POST',{survey_id:survey.id,instance_id:button.dataset.copyQuestion});
        await bankView(bid);message(result.message);
      }finally{button.disabled=false;}
    });
  });
}
async function familyView(qid) {
  const [q, versions] = await Promise.all([api('/bank-questions/'+qid),api('/bank-questions/'+qid+'/versions')]);
  const shares=q.owned?await api('/bank-questions/'+qid+'/shares'):[];
  root.innerHTML=`<button id="back" class="secondary">题库首页</button><h1>${esc(q.latest_version?.content.title || '题目版本')}</h1>
    <p>历史版本不可覆盖。分支选择其父版本；恢复生成新版本，不更新已有问卷。</p><button id="usages">查询使用问卷</button><button id="crossStats">跨问卷统计</button>
    ${q.owned?`<section><h2>分享权限</h2><form id="shareForm"><label>已注册用户名<input id="shareUsername" required></label><button>分享题目</button></form>
    ${shares.map(s=>`<p>${esc(s.username)} <button data-revoke="${esc(s.username)}" class="secondary">撤销分享</button></p>`).join('')}</section>`:'<p>您可查看和复用题目；不能修改原题或查看作者的问卷。</p>'}
    <h2>版本历史</h2>${versions.map(v=>`<section data-version-row="${esc(v.id)}"><h3>V${v.version_no} · ${esc(v.content.title)}</h3>
    <p>版本 ID：${esc(v.id)}</p><p>父版本：${esc(v.parent_version_id||'无')} · 恢复来源：${esc(v.restored_from_version_id||'无')}</p>
    <details><summary>查看版本内容</summary>${questionDescription(v.content)}</details>
    ${q.owned?`<button data-branch="${esc(v.id)}">从此版本创建分支</button><button data-restore="${esc(v.id)}" class="secondary">恢复此版本为新版本</button>`:''}</section>`).join('')}`;
  bind('back','click',banksHome); bind('usages','click',()=>usageView(qid)); bind('crossStats','click',()=>crossView(qid));
  bind('shareForm','submit',async()=>{await api('/bank-questions/'+qid+'/shares','POST',{username:document.querySelector('#shareUsername').value});await familyView(qid);message('已分享');});
  actions('[data-revoke]',async b=>{await api('/bank-questions/'+qid+'/shares/'+encodeURIComponent(b.dataset.revoke),'DELETE');await familyView(qid);message('已撤销分享，已有问卷快照保持不变');});
  actions('[data-branch]',b=>{
    const v=versions.find(x=>x.id===b.dataset.branch), key=crypto.randomUUID();
    editQuestion(null,v.content,async content=>{
      await api('/bank-questions/'+qid+'/versions','POST',{content,parent_version_id:v.id,request_key:key});
      await familyView(qid);message('已创建新版本');
    },()=>familyView(qid));
  });
  root.querySelectorAll('[data-restore]').forEach(b=>{
    const key=crypto.randomUUID();
    b.onclick=async()=>{try {
      await api(`/bank-questions/${qid}/versions/${b.dataset.restore}/restore`,'POST',{parent_version_id:q.latest_version.id,request_key:key});
      await familyView(qid);message('已恢复为新版本');
    }catch(e){message(e.message,true);}};
  });
}
async function chooseLibrary(sid, instance=null) {
  const own=await api('/bank-questions'), shared=await api('/shared-questions');
  const items=instance?[...own,...shared].filter(q=>q.id===instance.source.question_id):[...own,...shared];
  root.innerHTML=`<button id="back" class="secondary">管理问卷</button><h1>${instance?'为草稿题目换版':'从题库选择题目'}</h1>
    <p>选择明确版本后复制完整快照。不会随题库后续修改而更新。</p>${familyCards(items)}<div id="versionPicker"></div>`;
  bind('back','click',()=>manage(sid));
  actions('[data-family]',async button=>{
    const qid=button.dataset.family, versions=await api('/bank-questions/'+qid+'/versions');
    document.querySelector('#versionPicker').innerHTML=versions.map(v=>`<section><h2>V${v.version_no} · ${esc(v.content.title)}</h2>
      <details><summary>查看内容</summary>${questionDescription(v.content)}</details><button data-pick="${esc(v.id)}">${instance?'使用此版本':'加入问卷'}</button></section>`).join('');
    actions('[data-pick]',async b=>{
      await api(`/surveys/${sid}`+(instance?`/questions/${instance.id}/version`:'/library-questions'),instance?'PUT':'POST',{question_id:qid,version_id:b.dataset.pick});
      await manage(sid);message(instance?'草稿已换版':'已加入独立题目快照');
    });
  });
}
async function usageView(qid) {
  const rows=await api('/bank-questions/'+qid+'/usages');
  root.innerHTML=`<button id="back" class="secondary">题库首页</button><h1>使用此题的问卷</h1><p>仅显示您有权管理的问卷。</p>
    ${rows.map(s=>`<section><h2>${esc(s.title)}</h2><p>${esc(surveyStatus(s.status))} · ${s.instances.length} 个题目实例</p><button data-open-survey="${esc(s.survey_id)}">管理问卷</button></section>`).join('')||'<p>暂无使用记录。</p>'}`;
  bind('back','click',banksHome);actions('[data-open-survey]',b=>manage(b.dataset.openSurvey));
}
async function crossView(qid, selected='') {
  const data=await api('/bank-questions/'+qid+'/stats');
  const displayed=selected?(await api('/bank-questions/'+qid+'/stats?version_id='+encodeURIComponent(selected))):data;
  root.innerHTML=`<button id="back" class="secondary">我的问卷</button><h1>跨问卷统计</h1><p>只统计自己的问卷，各版本独立。总答卷数按答卷去重；回答数按题目实例计数。</p>
    <label>版本筛选<select id="versionFilter"><option value="">全部版本（分组）</option>${data.groups.map(g=>`<option value="${esc(g.version_id)}" ${selected===g.version_id?'selected':''}>${esc(g.title)} · ${esc(g.version_id)}</option>`).join('')}</select></label>
    <section><h2>总答卷数：${displayed.total_responses}</h2></section>${displayed.groups.map(g=>`<section><h2>${esc(g.title)}</h2><p>版本：${esc(g.version_id)}</p>
    <p>问卷数：${g.survey_count} · 实例数：${g.instance_count} · 答卷数：${g.total_responses} · 回答数：${g.answer_count}</p>
    ${g.options?'<table><tr><th>选项</th><th>次数</th></tr>'+g.options.map(o=>`<tr><td>${esc(o.label)}</td><td>${o.count}</td></tr>`).join('')+'</table>':''}
    ${g.values?`<p>答案：${esc(g.values.join('、'))}</p>`:''}${g.type==='number'?`<p>平均值：${g.average??'暂无数据'}</p><p>分布：${esc(g.distribution.map(x=>x.value+' × '+x.count).join('；'))}</p>`:''}</section>`).join('')}`;
  bind('back','click',dashboard);bind('versionFilter','change',()=>crossView(qid,document.querySelector('#versionFilter').value));
}
