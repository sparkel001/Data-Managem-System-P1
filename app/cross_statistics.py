from collections import Counter
from fastapi import APIRouter, Depends, HTTPException
from .auth import db, current_user
from .banks import accessible_surveys, digest
from .statistics import summarize
from .questions import QuestionInput

router = APIRouter(prefix='/api/bank-questions')


@router.get('/{qid}/stats')
def cross_stats(qid: str, version_id: str | None = None, database=Depends(db), user=Depends(current_user)):
    surveys = accessible_surveys(database, qid, user)
    family = database.bank_questions.find_one({'_id': qid, '$or': [
        {'owner_id': user['_id']}, {'shared_with': user['_id']}]})
    groups = {}

    def group(vid, content, content_hash):
        if digest(content) != content_hash:
            raise HTTPException(409, '题目内容与保存记录不一致，暂时无法统计，请联系管理员。')
        if vid in groups and groups[vid]['content_hash'] != content_hash:
            raise HTTPException(409, '同一版本的题目内容不一致，暂时无法统计，请联系管理员。')
        return groups.setdefault(vid, {'version_id': vid, 'content_hash': content_hash, 'content': content,
                                      'rows': [], 'responses': set(), 'surveys': set(), 'instances': 0})

    # Authorized library readers can also see empty version groups. After sharing
    # is revoked, owners can only see the versions present in their own snapshots.
    if family:
        for v in database.question_versions.find({'question_id': qid}).sort('version_no', 1):
            if version_id is None or v['_id'] == version_id:
                group(v['_id'], v['content'], v['content_hash'])
    all_responses = set()
    for s in surveys:
        instances = [q for q in s['questions'] if q.get('source', {}).get('question_id') == qid
                     and (version_id is None or q['source']['version_id'] == version_id)]
        if not instances: continue
        rows = list(database.responses.find({'survey_id': s['_id']}, {'answers': 1}))
        all_responses.update(r['_id'] for r in rows)
        for q in instances:
            content = {key: q[key] for key in QuestionInput.model_fields}
            g = group(q['source']['version_id'], content, q['source']['content_hash'])
            g['instances'] += 1
            g['surveys'].add(s['_id'])
            g['responses'].update(r['_id'] for r in rows)
            g['rows'].extend({'answers': {'value': r['answers'][q['id']]}}
                             for r in rows if q['id'] in r['answers'])
    if version_id and version_id not in groups: raise HTTPException(404, '所选版本不存在，或您没有查看其统计的权限。')
    result = []
    for g in groups.values():
        summary = summarize({'id': 'value', **g['content']}, g['rows'])
        summary.pop('question_id')
        if g['content']['type'] == 'number':
            counts = Counter(summary['values'])
            summary['distribution'] = [{'value': value, 'count': counts[value]} for value in sorted(counts)]
        result.append({'version_id': g['version_id'], 'content_hash': g['content_hash'],
                       'survey_count': len(g['surveys']), 'instance_count': g['instances'],
                       'total_responses': len(g['responses']), **summary})
    return {'question_id': qid, 'total_responses': len(all_responses), 'groups': result}
