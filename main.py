from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from html_temp import CHALLENGE_HTML

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def challenge_page(
    *,
    username: str = Query(..., title="username"),
    gt: str = Query(..., title="gt"),
    challenge: str = Query(..., title="challenge")
):
    return CHALLENGE_HTML.format(gt, challenge, username)


@app.get("/gt.js", response_class=HTMLResponse)
async def gt():
    with open("gt.js", "r", encoding="utf-8") as f:
        return f.read()
