# devlog

> 开发者的"第二大脑"——将碎片化工作上下文结构化存储

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 为什么需要 devlog？

开发者的一天被各种琐事打断：修 Bug、开设计会、线上故障、技术调研...等周五写周报时，"我这周都干了什么？"

**devlog** 是一个轻量级的开发日志工具，帮你在工作中快速记录关键节点，然后自动整理成结构化的 Markdown，周报生成只需一键。

```
工作 → 随手记 → 自动分类 → 周报搞定
```

## 特性

- **结构化分类**：incident / feat / design / ops / bug / learn
- **灵活存储**：全局流水账 + 项目本地文档
- **智能防重**：同一天不记录重复内容
- **周报生成**：自动汇总本周工作
- **零依赖**：单个 Python 脚本，开箱即用

## 安装

```bash
# 克隆仓库
git clone https://github.com/maoruibin/devlog.git ~/.claude/skills/devlog

# 添加到 PATH（可选）
export PATH="$PATH:$HOME/.claude/skills/devlog"
```

## 快速开始

```bash
# 首次运行会提示配置全局日志目录
devlog feat "完成用户登录功能"

# 记录线上故障
devlog incident "首页Crash" -d "Root Cause: NPE in FeedAdapter. Fix: 添加空值检查"

# 记录技术方案（存到项目本地，可提交 git）
devlog design "Feed缓存策略" -d "Cache-Aside + TTL随机化" --here

# 查看今日日志
devlog list

# 生成周报
devlog weekly
```

## 分类体系

| 分类 | 说明 | 示例 |
|------|------|------|
| `incident` | 线上故障（必填根因与修复） | "首页Crash"、"支付超时" |
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

## 在 Claude Code 中使用

安装后配置 SKILL.md，即可通过对话记录：

```
你: 记一下，刚才修复的 Feed 缓存问题
Claude: ✅ 已归档到 ~/devlog/2025-01-21.md
```

## 工作流示例

```bash
# 早上：设计评审
devlog design "用户中心重构方案" --here

# 下午：修 Bug
devlog bug "修复登录 token 过期问题"

# 晚上：线上故障
devlog incident "支付服务超时" -d "原因: 数据库连接池耗尽. 修复: 扩容 + 慢查询优化"

# 周五：生成周报
devlog weekly
```

## License

MIT © [maoruibin](https://github.com/maoruibin)
