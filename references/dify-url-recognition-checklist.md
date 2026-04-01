# Dify URL 识别检查单

当用户提供 Dify URL 时，依次检查：

1. 这是部署根网址，还是 app/workflow 页面 URL？
2. URL 中是否直接包含 app id？
3. 当前页面是否已经登录？
4. 当前 URL 与页面标题是否一致？若不一致，以 URL/app id 为准。
5. 如果用户说“改了没变化”，先检查是否改错 app / draft。
6. 如果需要真实写入：先锁 app，再改 draft，再 publish，再回读。
