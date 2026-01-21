# 掘金/知乎/公众号 发布文案

---

## 标题建议

**方案1（直击痛点）**：
> 周五还在愁周报？我用 200 行 Python 搞定了

**方案2（工具介绍）**：
> devlog：一个拯救开发者周报的轻量级工具

**方案3（效率提升）**：
> 开发者的第二大脑：随手记录，自动生成周报

---

## 正文

### 引言

你是不是也有过这样的经历：

- 周一修了 3 个 Bug，周二开了 2 个设计会，周三处理了线上故障...
- 到了周五写周报时，脑子里一片空白："我这周都干了什么？"
- 翻 Git 记录？翻聊天记录？翻 Jira 票？费时费力

作为一名开发者，我每天都在处理各种碎片化的工作：修 Bug、写方案、查线上问题、技术调研...这些工作如果不及时记录，一周下来真记不清自己干了什么。

所以我写了 **devlog** —— 一个轻量级的开发日志工具。

### devlog 是什么？

devlog 是一个命令行工具，帮你快速记录工作中的关键节点，并自动整理成结构化的 Markdown 文件。

核心设计理念：

1. **随手记** - 命令简单，3 秒完成记录
2. **结构化** - 按分类存储，方便后续查找
3. **周报友好** - 一键汇总本周工作

### 快速上手

```bash
# 安装
git clone https://github.com/maoruibin/devlog.git ~/.claude/skills/devlog

# 记录一个 Bug 修复
devlog bug "修复登录 token 过期问题"

# 记录线上故障（带详细说明）
devlog incident "首页Crash" -d "Root Cause: NPE in FeedAdapter. Fix: 添加空值检查"

# 记录技术方案（存到项目本地，可提交 git）
devlog design "Feed缓存策略" -d "Cache-Aside + TTL随机化" --here

# 周五生成周报
devlog weekly
```

### 核心功能

**1. 结构化分类**

| 分类 | 说明 |
|------|------|
| `incident` | 线上故障（必填根因和修复） |
| `feat` | 业务需求 |
| `design` | 技术方案 |
| `ops` | 运维部署 |
| `bug` | 常规 Bug |
| `learn` | 技术调研 |

**2. 灵活存储**

- 全局存储：个人工作流水，适合生成周报
- 项目本地（`--here`）：项目技术文档，可随代码提交
- 自定义路径：按需指定

**3. 智能防重**

同一天不会记录重复内容，避免误操作。

**4. 周报生成**

```bash
devlog weekly    # 查看最近 7 天的工作汇总
devlog weekly --days 14    # 查看最近两周
```

### 实际工作流

```bash
# 早上：参加设计评审
devlog design "用户中心重构方案" --here

# 下午：修复 Bug
devlog bug "修复点赞数不刷新"

# 晚上：线上故障
devlog incident "支付超时" -d "原因: 数据库连接池耗尽. 修复: 扩容"

# 周五：生成周报
devlog weekly
```

输出示例：

```
📊 周 报 / Weekly Report
==================================================

🚨 **线上故障** (1)
  - 支付超时
    <small>原因: 数据库连接池耗尽. 修复: 扩容</small>

✨ **业务需求** (0)

📐 **技术方案** (1)
  - 用户中心重构方案

🐛 **常规Bug** (1)
  - 修复点赞数不刷新

────────────────────────────────────────────────────
📅 2025-01-15 ~ 2025-01-21  |  共 5 天有记录
```

### 与 Claude Code 集成

如果你使用 Claude Code，可以配置成对话式记录：

```
你: 记一下，刚才修复的 Feed 缓存问题
Claude: ✅ 已归档到 ~/devlog/2025-01-21.md
```

### 为什么不是...？

| 工具 | 问题 |
|------|------|
| 记事本/备忘录 | 不结构化，周报时需要重新整理 |
| Git commit message | 只能记录代码变更，无法记录会议、故障等 |
| Jira/禅道 | 太重，打开网页慢，不适合随手记 |
| Notion/Obsidian | 功能太多，打开需要时间 |

devlog 的优势：**够快、够轻、够专注**

### 开源地址

**GitHub**: https://github.com/maoruibin/devlog

欢迎 Star / Issue / PR！

### 写在最后

这个工具是我自己在用，先解决了自己的周报痛点，现在开源出来分享给大家。

如果你也有类似的困扰，欢迎试试。有任何建议欢迎提 Issue！

---

**一键体验**：

```bash
git clone https://github.com/maoruibin/devlog.git ~/.claude/skills/devlog
export PATH="$PATH:$HOME/.claude/skills/devlog"
devlog feat "第一次使用 devlog"
```
