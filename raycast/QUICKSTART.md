# 快速开始 - Raycast + devlog

## 🚀 5 分钟上手

### 第一步：验证环境

```bash
# 确认 Python 已安装
python3 --version

# 确认 devlog 已安装
ls ~/.claude/skills/devlog/devlog.py
```

### 第二步：添加到 Raycast

1. 打开 Raycast（按 `⌘Space`）
2. 输入 `Script Commands` 并回车
3. 点击右上角的 `+` → `Add Directory`
4. 选择此目录

### 第三步：测试功能

在 Raycast 中测试以下命令：

```
log          → 记录工作
daily        → 生成日报
view today   → 查看今日日志
weekly       → 生成周报
```

## 📝 第一次记录

1. 打开 Raycast（`⌘Space`）
2. 输入 `log`
3. 选择 `🐛 Bug - 常规Bug`
4. 标题：`修复首页加载问题`
5. 详情：`优化图片加载逻辑，减少内存占用`
6. 回车确认

看到这个输出就成功了：
```
✅ 🐛 BUG: 修复首页加载问题
📄 优化图片加载逻辑，减少内存占用
```

## 🎯 日常工作流

### 早上
开始工作前，查看昨天的日志：
```
Raycast → view today
```

### 工作中
完成任务后立即记录：
```
Raycast → log → 选择分类 → 输入信息
```

### 下班前
生成日报，回顾今天的工作：
```
Raycast → daily
```

### 周五
准备周会材料：
```
Raycast → weekly
```

## 💡 Pro Tips

1. **快捷键**：为常用命令设置 Raycast 快捷键（如 `⌘⌥L` 触发 log）
2. **模板**：在详情中使用固定格式，如 `问题: XXX | 方案: YYY | 结果: ZZZ`
3. **项目隔离**：在项目目录下使用 `--here` 将日志保存到项目本地
4. **定期回顾**：每周五使用 `weekly` 回顾本周工作，找出改进点

## 🔧 故障排查

### 脚本不显示
```bash
# 检查权限
chmod +x devlog*.sh

# 重新加载 Raycast
Raycast → Reload All Commands
```

### Python 错误
```bash
# 确认路径正确
cat devlog.sh | grep DEVLOG_PATH

# 手动测试
python3 ~/.claude/skills/devlog/devlog.py --help
```

### 配置问题
```bash
# 查看配置
python3 ~/.claude/skills/devlog/devlog.py config show

# 重置配置
python3 ~/.claude/skills/devlog/devlog.py config reset
```

## 📚 进阶使用

### 命令行直接使用

```bash
# 添加别名
echo 'alias dlog="python3 ~/.claude/skills/devlog/devlog.py"' >> ~/.zshrc
source ~/.zshrc

# 现在可以直接使用
dlog feat "新功能" -d "详细说明"
dlog daily
dlog weekly --days 14
```

### 项目本地日志

```bash
# 在项目目录下
cd ~/projects/my-app
dlog design "架构重构方案" --here

# 日志保存在 ~/projects/my-app/.devlog/
```

### 自定义存储路径

```bash
# 保存到指定目录
dlog ops "服务器部署" --path ~/work/ops-logs/
```

## 🎉 完成！

现在你已经可以：
- ✅ 通过 Raycast 快速记录工作
- ✅ 生成每日工作总结
- ✅ 生成周报材料
- ✅ 管理多个项目的日志

享受高效的工作记录体验吧！

---

**需要帮助？**
- 查看 [RAYCAST_INTEGRATION.md](./RAYCAST_INTEGRATION.md) 了解详细功能
- 查看 [PR_DESCRIPTION.md](./PR_DESCRIPTION.md) 了解技术细节
- 访问 [原项目](https://github.com/maoruibin/devlog) 了解更多
