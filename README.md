# devlog

> **Claude Code 技能**——在 Vibe Coding 时代，结构化记录你的每一天

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-7c3aed.svg)](https://claude.ai/code)

## 背景：Vibe Coding 时代的记录困境

我们正处在一个新的开发时代：

- 每天和 AI 结对编程，快速迭代
- 终端里敲下无数命令，解决各种问题
- 和 AI 对话中完成了大量工作，但留不下痕迹
- 到了周五写周报时："我这周都干了什么？"

**devlog** 是我为 Claude Code 开发的一个技能，帮你把与 AI 协作的关键节点结构化记录下来，让每一天的工作都有迹可循。

```
AI 对话 → 随手记 → 结构化存储 → 周报/复盘搞定
```

## 为什么需要这个技能？

作为 Claude Code 用户，我发现：

1. **对话即工作**——和 AI 讨论方案、调试代码、修复 Bug，这些都是有价值的工作
2. **速度快**——AI 帮我们快速完成，但来不及记录
3. **碎片化**——一天处理多个问题，很难系统梳理

devlog 技能让 AI 帮你记录，无需打断工作流：

```
你: 记一下，刚才修复的 Feed 缓存问题
Claude: ✅ 已归档到 ~/devlog/2025-01-21.md
```

## 特性

- **对话式记录**：与 Claude 自然对话即可记录
- **结构化分类**：incident / feat / design / ops / bug / learn
- **灵活存储**：全局流水账 + 项目本地文档
- **智能防重**：同一天不记录重复内容
- **周报生成**：自动汇总本周工作
- **零依赖**：单个 Python 脚本

## 安装

```bash
# 克隆到 Claude Code 技能目录
git clone https://github.com/maoruibin/devlog.git ~/.claude/skills/devlog

# 添加到 PATH（可选，用于命令行直接调用）
export PATH="$PATH:$HOME/.claude/skills/devlog"
```

## 快速开始

### 在 Claude Code 中使用

1. 将 `SKILL.md` 内容复制到你的技能配置中
2. 开始对话：

```
你: 记一下，刚才修复的 Feed 缓存问题
Claude: ✅ 已归档到 ~/devlog/2025-01-21.md

你: 记录刚才讨论的用户中心重构方案，存到项目里
Claude: ✅ 已归档到 ./.devlog/2025-01-21.md
```

### 命令行使用

```bash
# 记录工作
devlog feat "完成用户登录功能"
devlog incident "首页Crash" -d "Root Cause: NPE in FeedAdapter. Fix: 添加空值检查"
devlog design "Feed缓存策略" -d "Cache-Aside + TTL随机化" --here

# 查看日志
devlog list

# 生成周报
devlog weekly
```

## 分类体系

| 分类 | 说明 | 示例 |
|------|------|------|
| `incident` | 线上故障（必填根因和修复） | "首页Crash"、"支付超时" |
| `feat` | 业务需求 | "点赞功能"、"评论折叠" |
| `design` | 技术方案 | "缓存策略"、"架构选型" |
| `ops` | 运维部署 | "配置变更"、"数据订正" |
| `bug` | 常规 Bug | "修复登录失败" |
| `learn` | 技术调研 | "Rust 异步学习" |

## 存储策略

| 选项 | 路径 | 适用场景 |
|------|------|----------|
| 无参数 | `~/devlog/` (可配置) | 个人全局流水账，周报素材 |
| `--here` | `./.devlog/` | 项目技术文档，随代码提交 |
| `--path DIR` | 自定义 | 特殊需求 |

## 命令参考

```bash
# 记录日志
devlog <category> "<title>" [-d "<detail>"] [--here] [--path DIR]

# 查看日志
devlog list [--here] [--path DIR]

# 生成周报（默认最近7天）
devlog weekly [--days N]

# 配置管理
devlog config show    # 查看配置
devlog config reset   # 重置配置
```

## 输出格式

日志以 Markdown 格式存储：

```markdown
# 📅 2025-01-21 Work Log

### [14:30] `@my-project` INCIDENT: 修复首页 Crash
> Root Cause: NPE in FeedAdapter.notifyDataSetChanged()
> Fix: 添加空值检查，已提交 PR #123

### [11:15] `@my-project` DESIGN: Feed 缓存策略方案
> 采用 Cache-Aside + TTL 随机化防止雪崩

---
```

## 配置

**首次运行**：首次使用时会提示选择全局日志目录

**配置文件**：`~/.claude/skills/devlog/.config`

```json
{
  "global_dir": "/Users/yourname/devlog",
  "version": "1.0"
}
```

**环境变量**：支持 `DEVLOG_GLOBAL_DIR` 临时覆盖

```bash
export DEVLOG_GLOBAL_DIR="/custom/path"
```

## 工作流示例

```bash
# 早上：和 AI 讨论架构
devlog design "用户中心重构方案" --here

# 下午：AI 帮忙修 Bug
devlog bug "修复登录 token 过期问题"

# 晚上：线上故障
devlog incident "支付服务超时" -d "原因: 数据库连接池耗尽. 修复: 扩容 + 慢查询优化"

# 周五：生成周报
devlog weekly
```

## Vibe Coding 时代的开发日志

传统开发日志只记录代码变更，但在 AI 辅助开发的今天：

- **对话即设计**——和 AI 讨论的方案是宝贵的设计文档
- **调试即学习**——AI 帮你排查问题的过程值得记录
- **快速迭代**——一天完成的工作更多，更需要记录

devlog 让这些"隐性工作"显性化，让你的每一天都清晰可见。

## License

MIT © [maoruibin](https://github.com/maoruibin)

---

**一键体验**：

```bash
git clone https://github.com/maoruibin/devlog.git ~/.claude/skills/devlog
devlog feat "第一次使用 devlog"
```
