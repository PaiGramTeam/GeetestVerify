CHALLENGE_HTML = """
<!DOCTYPE html>
<html>
  <body>
    <button type="button" id="login">点击开始验证</button>
  </body>
  <script src="./gt.js"></script>
  <script>
    window.initGeetest(
      {{
        gt: "{0}",
        challenge: "{1}",
        new_captcha: true,
        offline: false,
        product: "bind",
        https: true,
      }},
      (captcha) => {{
        captcha.appendTo("login");
        captcha.onSuccess(() => {{
          document.body.innerHTML = "验证成功，页面跳转中...";
          window.location.href = "https://t.me/{2}?start=challenge_" + captcha.getValidate().geetest_validate;
        }});
        captcha.onError(function (error) {{
          document.body.innerHTML = "发生错误：" + error.msg;
        }});
        document.getElementById("login").onclick = () => {{
          return captcha.verify();
        }};
      }}
    )
  </script>
</html>
"""
