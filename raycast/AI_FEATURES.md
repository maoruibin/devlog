# AI 总结和剪贴板功能

## 🤖 AI 智能总结

使用 Claude AI 自动生成工作日报和周报的专业总结。

###  功能特性

- **智能分析**：自动分析工作日志，提取关键信息
- **结构化输出**：生成包含工作概述、主要成果、技术亮点的总结
- **自动去格式**：输出纯文本，去除 Markdown 格式
- **一键复制**：自动复制到剪贴板，方便粘贴到其他应用

### 使用方法

**日报 + AI 总结 + 复制：**
```bash
devlog daily --ai --copy
# 或简写
devlog daily --ai-summary --clipboard
```

**周报 + AI 总结 + 复制：**
```bash
devlog weekly --ai --copy
# 指定天数
devlog weekly --days 14 --ai --copy
```

**仅复制不总结：**
```bash
devlog daily --copy
devlog weekly --copy
```

### 在 Raycast 中使用

已经为 Raycast 脚本预配置了 AI 总结和自动复制功能：

1. **生成日报**
   ```
   Raycast → daily → 自动 AI 总结 → 复制到剪贴板 → 直接粘贴使用
   ```

2. **生成周报**
   ```
   Raycast → weekly → 自动 AI 总结 → 复制到剪贴板 → 直接粘贴使用
   注：可输入天数，默认 7 天
   ```

### 输出示例

**原始日志：**
```
✨ 业务需求:
  - 完成用户登录功能
    实现 JWT 认证
  - 优化首页加载速度
🐛 常规Bug:
  - 修复登录超时问题
    增加重试机制
```

**AI 总结后：**
```
工作概述：
今日完成 2 项业务需求开发和 1 项 Bug 修复，主要聚焦在用户认证和性能优化方面。

主要成果：
• 完成用户登录功能，采用 JWT 认证机制，提升安全性
• 优化首页加载速度，改善用户体验
• 修复登录超时问题，通过增加重试机制提高稳定性

技术亮点：
JWT 认证的引入为后续的微服务架构奠定了基础，同时重试机制的实现提升了系统的容错能力。
```

**特点：**
- 纯文本格式，无 Markdown 符号
- 可以直接粘贴到钉钉、飞书、企业微信等
- 保留 emoji 和项目符号，美观易读

## 📋 剪贴板功能

### 自动去除格式

复制到剪贴板时，会自动处理以下格式：

| Markdown | 转换后 |
|----------|--------|
| `**粗体**` | 粗体 |
| `*斜体*` | 斜体 |
| `` `代码` `` | 代码 |
| `# 标题` | 标题 |
| `- 列表` | • 列表 |
| `<small>小字</small>` | 小字 |

### 使用场景

1. **即时汇报**：生成日报后直接粘贴到沟通工具
2. **周会材料**：一键生成周报并复制，准备周会分享
3. **工作记录**：快速生成总结并存档到文档系统
4. **团队协作**：分享工作进展到项目管理工具

## 🔧 安装要求

### Claude Code CLI（AI 总结功能需要）

AI 总结功能使用 `claude` 命令（Claude Code CLI）：

**安装方式：**
1. 从 Claude.ai 下载 Claude Code
2. 安装后，`claude` 命令会自动可用
3. 不需要额外配置 API Key

**验证安装：**
```bash
# 检查 claude 命令是否可用
which claude

# 测试 claude 命令
echo "Hello" | claude
```

**如果没有 Claude Code：**
- 访问 https://claude.ai 下载 Claude Code
- 或者使用 `--copy` 参数仅复制原始内容，不使用 AI 总结

### 测试

```bash
# 测试剪贴板功能（不需要 AI）
devlog daily --copy
pbpaste  # 查看剪贴板内容

# 测试 AI 总结（需要 Claude Code）
devlog daily --ai

# 测试 AI 总结 + 复制
devlog daily --ai --copy
pbpaste  # 查看 AI 总结的内容
```

## ⚙️ 配置选项

### 命令行参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--ai-summary` | `--ai` | 使用 AI 生成总结 |
| `--clipboard` | `--copy` | 复制到剪贴板 |
| `--compact` | - | 简洁输出模式 |

### 组合使用

```bash
# 日报：AI 总结 + 复制
devlog daily --ai --copy

# 周报：AI 总结 + 复制 + 简洁模式
devlog weekly --ai --copy --compact

# 只复制原始内容
devlog daily --copy

# 只显示 AI 总结，不复制
devlog daily --ai
```

## 🎯 最佳实践

### 日常工作流

**早上**：
```bash
# 查看昨天的日志
devlog list
```

**工作中**：
```bash
# 即时记录
devlog feat "完成功能" -d "详细说明"
```

**下班前**：
```bash
# 生成 AI 总结并复制，发送日报
devlog daily --ai --copy
# 直接粘贴到钉钉/飞书/邮件
```

**周五**：
```bash
# 生成周报并复制
devlog weekly --ai --copy
# 准备周会材料
```

### 使用技巧

1. **自定义 prompt**：编辑 `devlog.py` 中的 `call_claude_for_summary` 函数，自定义 AI 总结的格式
2. **快捷键**：在 Raycast 中为常用命令设置快捷键
3. **模板化**：保持日志记录的格式一致，AI 总结效果更好
4. **定期回顾**：结合 AI 总结，定期回顾工作内容

## ⚠️ 注意事项

1. **API 费用**：Claude API 按使用量计费，请注意控制成本
2. **网络连接**：AI 总结需要网络连接
3. **超时设置**：默认 30 秒超时，大量日志可能需要更长时间
4. **隐私安全**：敏感信息不要使用 AI 总结功能
5. **降级机制**：AI 失败时自动使用原始内容

## 🔍 故障排查

### AI 总结失败

```bash
# 检查 claude 命令是否存在
which claude

# 手动测试
echo "请总结：今天完成了3个任务" | claude

# 如果命令不存在，安装 Claude Code
# 访问 https://claude.ai
```

**常见问题：**
1. **命令找不到**：确保 Claude Code 已安装并正确配置 PATH
2. **超时**：网络问题或内容过多，可以重试
3. **空输出**：检查 Claude Code 是否正常启动

### 剪贴板问题

```bash
# 测试剪贴板
echo "test" | pbcopy
pbpaste

# 权限问题（macOS）
# 系统偏好设置 → 安全性与隐私 → 辅助功能
```

### 超时问题

如果 AI 总结经常超时，可以修改超时设置：

编辑 `devlog.py` 第 187 行：
```python
timeout=30  # 改为 timeout=60
```

## 📚 更多信息

- Claude API 文档：https://docs.anthropic.com
- Raycast 脚本文档：https://developers.raycast.com
- devlog 项目：https://github.com/maoruibin/devlog
