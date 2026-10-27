// All display paths use readable text, never exception payloads or status codes.
function readableError(value, fallback='操作未能完成，请稍后重试。') {
  return typeof value === 'string' && /[\u3400-\u9fff]/.test(value) && !/[A-Za-z_{}\[\]<>]/.test(value)
    ? value : fallback;
}
async function api(path, method='GET', body) {
  let response;
  try { response=await fetch('/api'+path, {method,headers:{'Content-Type':'application/json',Authorization:'Bearer '+token},
    body:body===undefined?undefined:JSON.stringify(body)}); }
  catch (_) { throw Error('无法连接服务，请检查网络，并确认服务已经启动。'); }
  const fallback=response.ok?'暂时无法读取返回内容，请刷新页面后重试。':
    ({401:'请先登录后再操作。',403:'您没有权限执行此操作。',404:'没有找到所需内容，或您没有查看权限。',
      409:'内容已发生变化，请刷新后重试。',422:'填写内容不符合要求，请检查后重试。'}[response.status]||'服务暂时无法完成操作，请稍后重试或联系管理员。');
  const type=(response.headers.get('Content-Type')||'').split(';')[0].trim().toLowerCase();
  if(type!=='application/json'&&!type.endsWith('+json')) throw Error(fallback);
  let data;
  try { data=await response.json(); } catch (_) { throw Error(fallback); }
  if(!response.ok) throw Error(readableError(typeof data?.detail==='string'?data.detail:data?.detail?.message,fallback));
  return data;
}
const surveyStatus=value=>({draft:'草稿',published:'已发布',closed:'已关闭'}[value]||'状态暂不可用');
function questionDescription(q) {
  return `<p>题型：${esc(typeName[q.type]||'未知题型')} · ${q.required?'必答':'选答'}</p>
    ${q.options?.length?'<p>选项：'+q.options.map(o=>esc(o.label)).join('、')+'</p>':''}
    ${q.type==='multiple'?`<p>选择数量：${q.min_choices}～${q.max_choices??q.options.length}</p>`:''}
    ${q.type==='text'?`<p>文字长度：${q.min_length}～${q.max_length}</p>`:''}
    ${q.type==='number'?`<p>数字范围：${q.min_value??'不限'}～${q.max_value??'不限'}；${q.integer?'只允许整数':'允许小数'}</p>`:''}`;
}
function answerDescription(s, answers) {
  return Object.entries(answers).map(([id,value])=>{
    const q=s.questions.find(q=>q.id===id);
    const label=v=>q?.options?.find(o=>o.id===v)?.label??v;
    const shown=Array.isArray(value)?value.map(label).join('、'):q?.type==='single'?label(value):value;
    return `<p>${esc(q?.title||'原题目已不可用')}：${esc(shown)}</p>`;
  }).join('');
}
// Use Chinese native-form validation even when the browser language is English.
document.addEventListener('invalid',event=>{
  const input=event.target;
  input.setCustomValidity(input.validity.valueMissing?'请填写此项。':'填写格式不正确，请按页面说明修改。');
},true);
document.addEventListener('input',event=>event.target.setCustomValidity?.(''),true);
document.addEventListener('change',event=>event.target.setCustomValidity?.(''),true);
