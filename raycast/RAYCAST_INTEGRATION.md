# Raycast Integration for devlog

这是 devlog 的 Raycast 集成脚本，让你可以通过 Raycast 快速记录和查看开发工作日志。

## ✨ 新增功能

### 1. Compact 输出模式 (`--compact`)
为 Raycast、Alfred 等启动器优化的简洁输出模式，去除了冗余的装饰性内容。

**使用方法：**
```bash
# 记录日志（简洁输出）
devlog feat "完成用户登录" --compact

# 查看今日日志（简洁输出）
devlog list --compact

# 生成周报（简洁输出）
devlog weekly --compact

# 生成日报（简洁输出）
devlog daily --compact
```

### 2. 日报生成功能 (`daily` / `today` / `summary`)
新增当日工作总结功能，自动汇总和分类当天的所有工作记录。

**特性：**
- 📊 工作概览：按分类统计今日完成的工作数量
- 📋 详细列表：展示每项工作的时间、标题和详细说明
- 🏷️ 分类展示：按线上故障、业务需求、技术方案等分类组织

**使用方法：**
```bash
# 生成当日工作总结
devlog daily

# 简写方式
devlog today
devlog summary

# 使用 compact 模式（适合 Raycast）
devlog daily --compact
```

## 📦 Raycast 脚本

本目录包含以下 Raycast 脚本：

| 脚本 | 功能 | 快捷触发 | AI 总结 |
|------|──────|---------|----------|
| `devlog.sh` | 记录开发工作 | `log` | - |
| `devlog-list.sh` | 查看今日日志 | `view today` | - |
| `devlog-daily.sh` | 生成今日总结 | `daily summary` | ✅ 启用 |
| `devlog-weekly.sh` | 生成周报 | `weekly` | ✅ 启用 |

## 🚀 安装指南

### 1. 安装脚本到 Raycast

```bash
# 将此目录添加到 Raycast Script Commands
# 在 Raycast 中:
# 1. 打开设置 (⌘,)
# 2. Extensions → Script Commands
# 3. Add Directory → 选择此目录
```

或者复制到标准 Raycast 脚本目录：
```bash
mkdir -p ~/raycast-scripts
cp -r . ~/raycast-scripts/devlog/
```

### 2. 验证安装

在 Raycast 中输入：
- `log` - 应该显示 "Log Dev Work"
- `daily` - 应该显示 "Generate Daily Summary"
- `view today` - 应该显示 "View Today's Dev Log"
- `weekly` - 应该显示 "Generate Weekly Report"

## 💡 使用示例

### 记录工作

1. 打开 Raycast (`⌘Space`)
2. 输入 `log`
3. 选择分类（如 🐛 Bug）
4. 输入标题："修复登录超时问题"
5. 输入详情："增加重试机制和超时处理"
6. 回车确认

**输出示例：**
```
✅ 🐛 BUG: 修复登录超时问题
📄 增加重试机制和超时处理
```

### 查看今日日志

输入 `view today`，显示原始 Markdown 格式的所有今日记录。

### 生成日报总结

输入 `daily summary`，自动生成结构化的工作总结：

```
📊 **今日工作概览** (共 5 项)

  🔧 运维部署: 2 项
  🐛 常规Bug: 2 项
  📚 技术调研: 1 项

📋 **详细列表**

🔧 **运维部署**
  - [15:56] 数据上传功能优化
  - [16:00] 对象存储配置更新

🐛 **常规Bug**
  - [16:01] 修复登录超时问题
    · 增加重试机制和超时处理
  - [16:10] 处理页面加载失败
```

### 生成周报

输入 `weekly`，默认生成最近 7 天的工作汇总。

## 🎨 输出对比

### 普通模式 vs Compact 模式

**普通模式（Terminal）：**
```
==================================================
✅ Log Saved Successfully
==================================================
📂 Path:    /Users/you/devlog/2026-01-22.md
🏷️  Type:    🐛 BUG - 常规Bug
📝 Content: 修复登录超时
📄 Detail:  增加重试机制
📍 Scope:   GLOBAL
----------------------------------------
```

**Compact 模式（Raycast）：**
```
✅ 🐛 BUG: 修复登录超时
📄 增加重试机制
```

## 🔧 技术细节

### 脚本结构
- 所有脚本调用 `~/.claude/skills/devlog/devlog.py`
- 使用 `--compact` 参数优化输出
- 支持 `--here` 和 `--path` 参数控制存储位置

### 兼容性
- macOS 10.15+
- Python 3.6+
- Raycast 1.0+

## 📝 最佳实践

1. **即时记录**：完成任务后立即记录，保持信息新鲜
2. **简洁标题**：用一句话概括工作内容
3. **关键细节**：在详情中记录重要的技术点、原因、方案
4. **日报总结**：每天下班前生成日报，回顾当天工作
5. **周报汇总**：每周五生成周报，准备周会材料

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

遵循 devlog 原项目许可证
