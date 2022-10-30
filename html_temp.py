CHALLENGE_HTML = """
<!DOCTYPE html>
<html lang="zh" class="h-full w-full">
<head>
    <meta charset="UTF-8">
    <title>Login Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            color: #495057;
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body class="h-full w-full">
<div class="container mx-auto h-full w-full">
    <div class="flex flex-col h-full w-full">
        <div class="m-auto w-full max-w-xl">
                <div class="rounded-t-lg bg-white ring-0 ring-black ring-opacity-20 m-auto text-6xl
                submit m-4 transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-105 ">
                    <button class="w-full p-4 2" id="submit">点击开始验证</button>
            </div>
        </div>
    </div>
</div>
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
        captcha.appendTo("submit");
        captcha.onSuccess(() => {{
          document.getElementById("submit").innerHTML = "验证成功，页面跳转中...";
          window.location.href = "https://t.me/{2}?start=challenge_" + captcha.getValidate().geetest_validate;
        }});
        captcha.onError(function (error) {{
          document.getElementById("submit").innerHTML = "发生错误：" + error.msg;
        }});
        document.getElementById("submit").onclick = () => {{
          return captcha.verify();
        }};
      }}
    )
  </script>
</html>
"""
