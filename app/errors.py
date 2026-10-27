"""Public messages are Chinese; technical diagnostics stay in server logs."""
import logging
import re
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from starlette.exceptions import HTTPException

log = logging.getLogger(__name__)
FALLBACK = '操作未能完成，请稍后重试。'
FIELDS = {'username':'用户名','password':'密码','title':'标题','description':'说明','name':'题库名称',
          'options':'选项','id':'选项编号','label':'选项文字','type':'题型','required':'必答设置',
          'min_choices':'最少选择数量','max_choices':'最多选择数量','min_length':'最短文本长度',
          'max_length':'最长文本长度','min_value':'数字下限','max_value':'数字上限','integer':'整数要求',
          'deadline':'截止时间','rules':'跳转规则','op':'跳转条件','value':'条件值','target':'跳转目标',
          'answers':'填写内容','anonymous':'匿名设置','allow_multiple':'重复填写设置'}


def chinese(text, fallback=FALLBACK):
    return text if isinstance(text, str) and re.search(r'[\u3400-\u9fff]', text) and not re.search(r'[A-Za-z_{}\[\]<>]', text) else fallback


def validation_message(error):
    label = next((FIELDS[k] for k in reversed(error['loc']) if k in FIELDS), '提交内容')
    kind, ctx = error['type'], error.get('ctx', {})
    if kind == 'value_error': return chinese(str(ctx.get('error', '')), f'{label}设置不正确，请检查后重试。')
    if kind == 'missing': return f'请填写{label}。'
    if kind == 'string_too_short': return f'{label}至少需要{ctx.get("min_length", 1)}个字符。'
    if kind == 'string_too_long': return f'{label}不能超过{ctx.get("max_length", 1)}个字符。'
    if kind == 'too_short': return f'{label}至少需要{ctx.get("min_length", 1)}项。'
    if kind == 'too_long': return f'{label}不能超过{ctx.get("max_length", 1)}项。'
    if kind == 'extra_forbidden': return '提交内容包含不支持的设置，请刷新页面后重新操作。'
    if kind == 'string_pattern_mismatch':
        return '用户名请使用英文字母、数字或下划线。' if label == '用户名' else f'{label}格式不正确，请检查后重试。'
    if kind in ('greater_than_equal','greater_than','less_than_equal','less_than'):
        return f'{label}超出允许范围，请按页面提示填写。'
    if kind == 'literal_error': return f'请选择有效的{label}。'
    if 'datetime' in kind: return '截止时间格式不正确，请重新选择日期和时间。'
    if kind in ('float_parsing','int_parsing','float_type','int_type','finite_number'): return f'{label}请填写有效数字。'
    if kind == 'json_invalid': return '提交内容无法读取，请刷新页面后重新操作。'
    return f'{label}格式不正确，请检查后重试。'


def install_error_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation(request, error):
        return JSONResponse(status_code=422, content={'detail': validation_message(error.errors()[0])})

    @app.exception_handler(HTTPException)
    async def business(request, error):
        defaults = {401:'请先登录后再操作。',403:'您没有权限执行此操作。',404:'没有找到所需内容，或您没有查看权限。',
                    405:'当前操作不可用，请返回页面重新选择。'}
        detail = error.detail
        if isinstance(detail, dict):
            detail = {**detail, 'message': chinese(detail.get('message'))}
        else: detail = chinese(detail, defaults.get(error.status_code, FALLBACK))
        return JSONResponse(status_code=error.status_code, content={'detail': detail}, headers=error.headers)

    @app.exception_handler(PyMongoError)
    async def database(request, error):
        log.error('Database request failed', exc_info=(type(error),error,error.__traceback__))
        return JSONResponse(status_code=503, content={'detail':'暂时无法保存或读取数据，请稍后重试；若持续失败，请联系管理员。'})

    @app.exception_handler(Exception)
    async def unexpected(request, error):
        log.error('Unexpected request failure', exc_info=(type(error),error,error.__traceback__))
        return JSONResponse(status_code=500, content={'detail':'服务暂时无法完成操作，请稍后重试或联系管理员。'})
