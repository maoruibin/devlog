# V2EX 发布文案

---

## 标题

**devlog：一个拯救周报的轻量级开发日志工具**

---

## 正文

每周五下午，群里就开始哀嚎：

> "周报怎么写？"
> "我这周好像啥也没干？"
> "翻 Git 记录太累了..."

我也是这样，所以写了个小工具拯救自己。

### devlog 是什么？

一个命令行工具，帮你快速记录工作，然后一键生成周报。

```bash
# 记录工作
devlog bug "修复登录失败"
devlog incident "支付超时" -d "数据库连接池耗尽，已扩容"

# 生成周报
devlog weekly
```

### 核心特性

- **6 种分类**：incident / feat / design / ops / bug / learn
- **灵活存储**：全局流水账 + 项目本地文档
- **智能防重**：同一天不记录重复内容
- **一键周报**：自动汇总最近 N 天的工作
- **零依赖**：单个 Python 脚本

### 使用场景

```bash
# 早上设计评审
devlog design "用户中心重构" --here

# 下午修 Bug
devlog bug "修复点赞数不刷新"

# 晚上线上故障
devlog incident "首页Crash" -d "NPE in FeedAdapter，已修复"

# 周五生成周报
devlog weekly
```

### 开源地址

https://github.com/maoruibin/devlog

MIT 协议，欢迎 Star / PR / 喷

---

PS: 第一次开源工具，轻喷 😅

