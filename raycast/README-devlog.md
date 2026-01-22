# DevLog Raycast 集成

这是一个用于在 Raycast 中快速记录开发工作日志的脚本集合。

## 功能特点

- 📝 **快速记录**: 通过 Raycast 快速记录开发工作
- 🏷️ **结构化分类**: 支持 7 种工作类型分类
- 📊 **自动汇总**: 生成每日日志和周报
- 💾 **灵活存储**: 支持全局存储或项目本地存储

## 安装步骤

### 1. 添加脚本到 Raycast

在 Raycast 中：
1. 打开 Raycast 设置 (⌘,)
2. 进入 Extensions → Script Commands
3. 点击 "Add Directory" 或 "+"
4. 选择 `~/raycast-scripts` 目录

### 2. 验证安装

在 Raycast 中输入 "log" 或 "devlog"，应该能看到以下命令：
- 📝 Log Dev Work - 记录开发工作
- 📋 View Today's Dev Log - 查看今日日志
- 📊 Generate Weekly Report - 生成周报

## 使用方法

### 记录工作日志

1. 打开 Raycast (⌘Space)
2. 输入 "Log Dev Work" 或 "log"
3. 选择分类：
   - 🚨 **incident** - 线上故障
   - ✨ **feat** - 业务需求
   - 📐 **design** - 技术方案
   - 🔧 **ops** - 运维部署
   - 🐛 **bug** - 常规Bug
   - 📚 **learn** - 技术调研
   - 📝 **misc** - 其他
4. 输入标题（必填）
5. 输入详细说明（可选）

### 查看今日日志

1. 打开 Raycast
2. 输入 "View Today's Dev Log"
3. 查看当天所有记录

### 生成周报

1. 打开 Raycast
2. 输入 "Generate Weekly Report"
3. 可选：输入天数（默认 7 天）

## 分类说明

根据 [maoruibin/devlog](https://github.com/maoruibin/devlog) 的设计：

| 分类 | 图标 | 说明 | 使用场景 |
|------|------|------|----------|
| incident | 🚨 | 线上故障 | 生产环境问题、紧急修复 |
| feat | ✨ | 业务需求 | 新功能开发、需求实现 |
| design | 📐 | 技术方案 | 架构设计、技术方案讨论 |
| ops | 🔧 | 运维部署 | 部署、配置、环境管理 |
| bug | 🐛 | 常规Bug | 日常 Bug 修复 |
| learn | 📚 | 技术调研 | 学习新技术、调研方案 |
| misc | 📝 | 其他 | 其他杂项工作 |

## 使用示例

### 记录线上故障
- **分类**: Incident
- **标题**: 首页加载超时
- **详情**: Redis 连接池耗尽，已增加连接数配置

### 记录新功能
- **分类**: Feature
- **标题**: 实现用户点赞功能
- **详情**: 完成前端 UI 和后端 API

### 记录技术方案
- **分类**: Design
- **标题**: Feed 缓存策略优化
- **详情**: 采用 Cache-Aside + TTL 随机化防止缓存雪崩

## 高级用法

### 命令行直接使用

```bash
# 记录日志
python3 ~/.claude/skills/devlog/devlog.py feat "完成用户登录" -d "实现 JWT 认证"

# 存储到项目本地
python3 ~/.claude/skills/devlog/devlog.py design "架构设计" --here

# 查看今日日志
python3 ~/.claude/skills/devlog/devlog.py list

# 生成周报
python3 ~/.claude/skills/devlog/devlog.py weekly --days 7

# 查看配置
python3 ~/.claude/skills/devlog/devlog.py config show

# 重置配置
python3 ~/.claude/skills/devlog/devlog.py config reset
```

### 添加到 PATH（可选）

如果想在终端直接使用 `devlog` 命令，可以添加到 PATH：

```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
echo 'export PATH="$PATH:$HOME/.claude/skills/devlog"' >> ~/.zshrc
echo 'alias devlog="python3 $HOME/.claude/skills/devlog/devlog.py"' >> ~/.zshrc
source ~/.zshrc

# 现在可以直接使用
devlog feat "新功能" -d "详细说明"
```

## 日志格式

日志以 Markdown 格式存储，默认路径：`~/你配置的目录/YYYY-MM-DD.md`

示例：
```markdown
# 📅 2026-01-22 Work Log

### [14:30] `@my-project` INCIDENT: 修复首页 Crash
> Root Cause: NPE in FeedAdapter.notifyDataSetChanged()
> Fix: 添加空值检查，已提交 PR #123

### [11:15] `@my-project` DESIGN: Feed 缓存策略方案
> 采用 Cache-Aside + TTL 随机化防止雪崩
```

## 配置

首次运行会提示配置全局日志目录，建议路径：
- `~/code/person/write/work`
- `~/Documents/work/logs`
- `~/work/logs`
- 或自定义路径

配置文件位置：`~/.claude/skills/devlog/.config`

## 故障排查

### 脚本不显示在 Raycast

1. 确认脚本有执行权限：`chmod +x ~/raycast-scripts/*.sh`
2. 在 Raycast 设置中重新加载脚本目录
3. 检查脚本是否包含正确的 Raycast 元数据注释

### Python 版本问题

确保使用 Python 3：
```bash
python3 --version
```

### 权限问题

如果遇到权限错误，检查：
```bash
ls -la ~/.claude/skills/devlog/devlog.py
chmod +x ~/.claude/skills/devlog/devlog.py
```

## 参考资源

- 原项目：https://github.com/maoruibin/devlog
- Raycast Script Commands: https://github.com/raycast/script-commands

## 最佳实践

1. **即时记录**: 完成工作后立即记录，保持信息准确
2. **简洁标题**: 标题简明扼要，突出重点
3. **详细说明**: 在 Detail 中记录关键信息（原因、方案、结果）
4. **定期回顾**: 每周生成周报，回顾工作内容
5. **分类准确**: 选择最合适的分类，便于后续统计

## 许可证

本集成脚本基于 devlog 项目，遵循原项目许可证。
