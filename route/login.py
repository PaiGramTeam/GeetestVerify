from typing import Optional

from fastapi import APIRouter
from genshin import GenshinClient, Region
from genshin.models import SessionMMT, ActionTicket, SessionMMTResult, CookieLoginResult
from pydantic import BaseModel
from starlette.requests import Request

from .templates import templates

router = APIRouter()
code_map = {
    0: "登录成功",
    1: "未知错误",
    2: "需要邮箱验证",
    3: "需要过验证",
}


class LoginRequest(BaseModel):
    email: str
    password: str
    mmt_result: Optional[SessionMMTResult] = None
    code: Optional[str] = None
    ticket: Optional[ActionTicket] = None


class LoginResult(BaseModel):
    code: int
    message: str
    result: Optional[str] = None
    mmt: Optional[SessionMMT] = None
    ticket: Optional[ActionTicket] = None


class CookieResult(CookieLoginResult):
    stoken: str
    mid: str
    account_id: str


@router.get("/login_start")
async def login_start(request: Request):
    return templates.TemplateResponse("login_email.html", {"request": request})


async def do_login_session_mmt(data: SessionMMT):
    return LoginResult(code=3, message="需要过验证", mmt=data)


async def do_login_action_ticket(client: GenshinClient, result: ActionTicket):
    # 需要邮箱验证
    try:
        email_result = await client._send_verification_email(result)
    except Exception as exc:
        return LoginResult(code=1, message=str(exc))  # 未知错误
    if isinstance(email_result, SessionMMT):
        # 需要过验证
        return await do_login_session_mmt(email_result)
    return LoginResult(code=2, message="需要邮箱验证")


async def do_login(data: LoginRequest):
    client = GenshinClient(
        region=Region.OVERSEAS,
        lang="zh-cn",
    )
    if data.code and data.ticket:
        try:
            await client._verify_email(data.code, data.ticket)
        except Exception as exc:
            return LoginResult(code=1, message=str(exc))  # 未知错误
    try:
        result = await client._app_login(
            data.email.strip(),
            data.password,
            mmt_result=data.mmt_result,
            ticket=data.ticket,
        )
    except Exception as exc:
        return LoginResult(code=1, message=str(exc))  # 未知错误

    if isinstance(result, SessionMMT):
        # 需要过验证
        return await do_login_session_mmt(result)
    elif isinstance(result, ActionTicket):
        # 需要邮箱验证
        return await do_login_action_ticket(client, result)
    # 登录成功
    ck = CookieResult(
        stoken=result.stoken,
        mid=result.account_mid_v2,
        account_id=result.account_id_v2,
    )
    return LoginResult(code=0, message="登录成功", result=ck.to_str())


@router.post("/login_start")
async def login_form(data: LoginRequest):
    if not data.email or not data.password:
        return LoginResult(code=1, message="邮箱或者密码不能为空")
    if data.ticket and not data.code:
        return LoginResult(code=1, message="邮箱验证码不能为空")
    return await do_login(data)
