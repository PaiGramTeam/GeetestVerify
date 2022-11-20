from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/img", StaticFiles(directory="public/img"), name="img")
app.mount("/js", StaticFiles(directory="public/js"), name="js")

templates = Jinja2Templates(directory="public/templates")


@app.get("/", response_class=HTMLResponse)
async def debug_challenge_page(
        request: Request,
        username: str = Query(..., title="username"),
        command: str = Query(..., title="command"),
        uid: str = Query(..., title="uid"),
        gt: str = Query(..., title="gt"),
        challenge: str = Query(..., title="challenge"),
):
    user = {"username": username, "uid": uid, "command": command}
    geetest = {
        "gt": gt,
        "challenge": challenge,
    }
    return templates.TemplateResponse(
        "example.html", {"request": request, "user": user, "geetest": geetest}
    )


@app.get("/webapp", response_class=HTMLResponse)
async def debug_challenge_page(
        request: Request,
        username: str = Query(..., title="username"),
        command: str = Query(..., title="command"),
        uid: str = Query(..., title="uid"),
        gt: str = Query(..., title="gt"),
        challenge: str = Query(..., title="challenge"),
):
    user = {"username": username, "uid": uid, "command": command}
    geetest = {
        "gt": gt,
        "challenge": challenge,
    }
    return templates.TemplateResponse(
        "webapp.html", {"request": request, "user": user, "geetest": geetest}
    )
