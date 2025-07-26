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
    3: "需要过登录人机验证",
    4: "需要过邮箱人机验证",
}


class LoginRequest(BaseModel):
    email: str
    password: str
    device_id: str
    mmt_result: Optional[SessionMMTResult] = None
    old_code: Optional[int] = None
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
    device_id = GenshinClient.generate_app_device_id()
    return templates.TemplateResponse(
        "login_email.html", {"request": request, "device_id": device_id}
    )


async def do_login_session_mmt(
    mode: str, data: SessionMMT, ticket: Optional[ActionTicket] = None
):
    return LoginResult(code=3, message=f"需要过验证 {mode}", mmt=data, ticket=ticket)


async def do_login_action_ticket(client: GenshinClient, result: ActionTicket):
    # 需要邮箱验证
    try:
        email_result = await client._send_verification_email(result)
    except Exception as exc:
        return LoginResult(code=1, message=str(exc))  # 未知错误
    if isinstance(email_result, SessionMMT):
        # 需要过验证
        return LoginResult(
            code=4, message="需要过邮箱人机验证", mmt=email_result, ticket=result
        )
    return LoginResult(code=2, message="需要邮箱验证", ticket=result)


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
            device_id=data.device_id,
            mmt_result=data.mmt_result if data.old_code == 3 else None,
            ticket=data.ticket,
        )
    except Exception as exc:
        return LoginResult(code=1, message=str(exc))  # 未知错误

    if isinstance(result, SessionMMT):
        # 需要过验证
        return LoginResult(code=3, message="需要过登录人机验证", mmt=result)
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
    return await do_login(data)
