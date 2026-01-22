#!/usr/bin/env python3
"""
devlog - Development Work Logger
A lightweight tool to archive development work with structured categorization.

Usage:
    devlog incident "首页Crash" -d "NPE in FeedAdapter"
    devlog feat "点赞功能" --here
    devlog design "缓存策略" --path ~/custom/path
"""

import os
import sys
import datetime
import argparse
import re
import json
import subprocess
from pathlib import Path

# ================= Configuration =================
# 配置文件路径
CONFIG_DIR = os.path.expanduser("~/.claude/skills/devlog")
CONFIG_FILE = os.path.join(CONFIG_DIR, ".config")
# 项目本地存储目录名（隐藏目录，避免污染）
LOCAL_DIR_NAME = ".devlog"
# ================================================


class Config:
    """配置管理器"""

    def __init__(self, auto_init=True):
        self.config_file = CONFIG_FILE
        self._config = self._load_or_init(auto_init)

    def _load_or_init(self, auto_init):
        """加载配置或初始化"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                # 配置文件损坏，重新初始化
                if auto_init:
                    return self._init_config()
                return {}
        else:
            if auto_init:
                return self._init_config()
            return {}

    def _init_config(self):
        """首次运行时初始化配置"""
        print()
        print("=" * 50)
        print("👋 Welcome to dlog!")
        print("=" * 50)
        print()
        print("Please set your global log directory:")
        print()

        # 默认建议
        home = os.path.expanduser("~")
        suggestions = [
            f"{home}/code/person/write/work",
            f"{home}/Documents/work/logs",
            f"{home}/work/logs",
        ]

        print("Suggestions (press 1-3 to select, or enter custom path):")
        for i, s in enumerate(suggestions, 1):
            print(f"  {i}. {s}")
        print()

        while True:
            choice = input("Your choice [1-3 or custom path]: ").strip()

            if choice == "1":
                selected_dir = suggestions[0]
                break
            elif choice == "2":
                selected_dir = suggestions[1]
                break
            elif choice == "3":
                selected_dir = suggestions[2]
                break
            elif choice:
                # 自定义路径
                selected_dir = os.path.expanduser(choice)
                break
            else:
                print("❌ Please enter a valid choice.")

        # 确保目录存在
        try:
            Path(selected_dir).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"❌ Failed to create directory: {e}")
            print("Using fallback: ~/dlog")
            selected_dir = os.path.expanduser("~/dlog")
            Path(selected_dir).mkdir(parents=True, exist_ok=True)

        # 构造配置
        config = {
            "global_dir": selected_dir,
            "version": "1.0"
        }

        # 保存配置
        try:
            Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print()
            print(f"✅ Config saved to: {self.config_file}")
            print(f"📂 Global log dir: {selected_dir}")
            print()
        except IOError as e:
            print(f"⚠️  Failed to save config: {e}")

        return config

    @property
    def global_dir(self):
        """获取全局日志目录（支持环境变量覆盖）"""
        return os.environ.get("DEVLOG_GLOBAL_DIR", self._config.get("global_dir", os.path.expanduser("~/devlog")))

    @staticmethod
    def reset():
        """重置配置（删除配置文件，下次运行时重新初始化）"""
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print("✅ Config reset. Run dlog again to reconfigure.")
        else:
            print("ℹ️  No config file found.")

def markdown_to_rtf(markdown_text):
    """转Markdown为RTF格式"""
    # 简单的Markdown转RTF，支持基本格式
    rtf_text = markdown_text
    
    # 移除Markdown格式符号
    rtf_text = re.sub(r'^#{1,6}\s+', '', rtf_text, flags=re.MULTILINE)  # 标题
    rtf_text = re.sub(r'\*\*(.+?)\*\*', r'\1', rtf_text)  # 加粗
    rtf_text = re.sub(r'\*(.+?)\*', r'\1', rtf_text)  # 斜体
    rtf_text = re.sub(r'`(.+?)`', r'\1', rtf_text)  # 代码
    rtf_text = re.sub(r'^[-*+]\s+', '• ', rtf_text, flags=re.MULTILINE)  # 列表
    rtf_text = re.sub(r'^\d+\.\s+', '', rtf_text, flags=re.MULTILINE)  # 编号列表
    rtf_text = re.sub(r'<small>(.+?)</small>', r'\1', rtf_text)  # HTML小字
    
    return rtf_text.strip()

def copy_to_clipboard(text):
    """复制文本到剪贴板（macOS）使用osascript确保UTF-8编码"""
    try:
        # 方法1: 使用 osascript 复制，完美支持 UTF-8 和 emoji
        escaped_text = text.replace('\\', '\\\\').replace('"', '\\"')
        applescript = f'set the clipboard to "{escaped_text}"'
        
        process = subprocess.Popen(
            ['osascript', '-e', applescript],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, error = process.communicate()
        
        if process.returncode == 0:
            return True
        else:
            # 如果 AppleScript 失败，尝试 pbcopy
            raise Exception("osascript failed")
            
    except Exception:
        # 方法2: 退回到 pbcopy
        try:
            process = subprocess.Popen(
                ['pbcopy'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.communicate(text.encode('utf-8'))
            return True
        except Exception as e:
            print(f"⚠️  无法复制到剪贴板: {e}")
            return False

def call_claude_for_summary(log_content, report_type="daily"):
    """调用Claude Code生成工作总结"""
    prompt = f"""请根据以下工作日志生成一份简洁的{'\u65e5\u62a5' if report_type == 'daily' else '\u5468\u62a5'}总结。

日志内容：
{log_content}

请按以下格式输出：
1. 工作概述：一段话总结主要工作
2. 主要成果：列表形式，3-5项
3. 技术亮点：如果有
4. 需要关注：如果有

请用简洁、专业的语言，直接输出纯文本内容，不要使用Markdown格式符号。
"""
    
    try:
        # 调用 claude 命令（Claude Code CLI）
        result = subprocess.run(
            ['claude'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60  # 增加超时时间
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return None
    except FileNotFoundError:
        print("⚠️  未找到 claude 命令，请确保Claude Code已安装")
        return None
    except subprocess.TimeoutExpired:
        print("⚠️  AI 总结超时（60秒）")
        return None
    except Exception as e:
        print(f"⚠️  AI 总结失败: {e}")
        return None

# Terminal colors
class Colors:
    """终端颜色代码"""
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[0m"
    BOLD = "\033[1m"
    GRAY = "\033[90m"


class Logger:
    """日志记录器核心类"""

    # 分类定义
    CATEGORIES = {
        "incident": {"emoji": "🚨", "desc": "线上故障"},
        "feat": {"emoji": "✨", "desc": "业务需求"},
        "design": {"emoji": "📐", "desc": "技术方案"},
        "ops": {"emoji": "🔧", "desc": "运维部署"},
        "bug": {"emoji": "🐛", "desc": "常规Bug"},
        "learn": {"emoji": "📚", "desc": "技术调研"},
        "misc": {"emoji": "📝", "desc": "其他"},
    }

    def __init__(self, verbose=False, compact=False, config=None):
        self.verbose = verbose
        self.compact = compact
        self.c = Colors
        self.config = config or Config()

    def _print(self, msg, color=None):
        """带颜色的打印"""
        if color:
            print(f"{color}{msg}{self.c.RED}")
        else:
            print(msg)

    def get_project_context(self):
        """获取当前项目上下文"""
        cwd = os.getcwd()
        if cwd == os.path.expanduser("~"):
            return "Global"
        return os.path.basename(cwd)

    def is_duplicate(self, filepath, content, category):
        """
        检查是否重复记录
        策略：解析已有条目，检查同一天的相同类别+标题
        """
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content_lines = f.readlines()

            # 获取今天的日期字符串
            today = datetime.date.today().strftime("%Y-%m-%d")

            # 查找今天的所有条目
            for i, line in enumerate(content_lines):
                if line.startswith(f"# 📅 {today}"):
                    # 从这里开始检查今天的条目
                    for j in range(i + 1, len(content_lines)):
                        entry_line = content_lines[j]
                        # 遇到新的一天或文件结束
                        if entry_line.startswith("# 📅"):
                            break
                        # 检查是否是相同条目
                        if entry_line.startswith("### "):
                            pattern = f"{category.upper()}: {content}"
                            if pattern in entry_line:
                                return True
            return False

        except (IOError, UnicodeDecodeError) as e:
            if self.verbose:
                self._print(f"Warning: Duplicate check failed - {e}", self.c.YELLOW)
            return False

    def determine_path(self, use_current_dir, custom_dir):
        """
        决定存储路径
        优先级: 指定 > 当前项目 > 全局默认
        """
        # 1. 用户自定义路径
        if custom_dir:
            target = os.path.abspath(os.path.expanduser(custom_dir))
            Path(target).mkdir(parents=True, exist_ok=True)
            return target, "custom"

        # 2. 当前项目本地
        if use_current_dir:
            target = os.path.join(os.getcwd(), LOCAL_DIR_NAME)
            Path(target).mkdir(parents=True, exist_ok=True)
            return target, "local"

        # 3. 全局默认（从配置读取）
        global_dir = self.config.global_dir
        Path(global_dir).mkdir(parents=True, exist_ok=True)
        return global_dir, "global"

    def format_entry(self, timestamp, project, category, content, detail):
        """格式化单条日志"""
        cat_info = self.CATEGORIES.get(category, self.CATEGORIES["misc"])
        emoji = cat_info["emoji"]

        lines = [
            f"### [{timestamp}] `{project}` {category.upper()}: {content}",
        ]

        if detail:
            # 多行细节，每行加 >
            for line in detail.split("\n"):
                lines.append(f"> {line}")

        return "\n".join(lines) + "\n"

    def write(self, category, content, detail, use_current_dir, custom_dir):
        """写入日志"""
        # 1. 验证分类
        if category not in self.CATEGORIES:
            self._print(f"Error: Invalid category '{category}'", self.c.YELLOW)
            self._print(f"Valid categories: {', '.join(self.CATEGORIES.keys())}", self.c.GRAY)
            return 1

        # 2. 确定路径
        base_dir, location_type = self.determine_path(use_current_dir, custom_dir)
        today = datetime.date.today().strftime("%Y-%m-%d")
        filepath = os.path.join(base_dir, f"{today}.md")

        # 3. 防重检查
        if self.is_duplicate(filepath, content, category):
            self._print(f"{self.c.YELLOW}⚠️  Skipped: Log already exists today{self.c.RED}")
            return 0

        # 4. 构造内容
        timestamp = datetime.datetime.now().strftime("%H:%M")
        project = f"@{self.get_project_context()}"
        entry = self.format_entry(timestamp, project, category, content, detail)

        # 5. 写入文件
        is_new = not os.path.exists(filepath)
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                if is_new:
                    f.write(f"# 📅 {today} Work Log\n\n")
                f.write(entry)
                f.write("\n")  # 条目间隔
        except IOError as e:
            self._print(f"{self.c.RED}❌ Error: Failed to write log - {e}{self.c.RED}", file=sys.stderr)
            return 1

        # 6. 输出反馈
        self.print_feedback(filepath, category, content, detail, location_type)
        return 0

    def print_feedback(self, filepath, category, content, detail, location_type):
        """打印结构化反馈"""
        cat_info = self.CATEGORIES.get(category, self.CATEGORIES["misc"])
        emoji = cat_info["emoji"]

        if self.compact:
            # Compact output for Raycast/Alfred
            print(f"✅ {emoji} {category.upper()}: {content}")
            if detail:
                preview = detail[:60] + "..." if len(detail) > 60 else detail
                print(f"📄 {preview}")
        else:
            # Full output for terminal
            print()
            print(f"{self.c.GREEN}{self.c.BOLD}✅ Log Saved Successfully{self.c.RED}")
            print(f"📂 Path:    {filepath}")
            print(f"🏷️  Type:    {emoji} {category.upper()} - {cat_info['desc']}")
            print(f"📝 Content: {content}")
            if detail:
                preview = detail[:50] + "..." if len(detail) > 50 else detail
                print(f"📄 Detail:  {preview}")
            print(f"📍 Scope:   {location_type.upper()}")
            print("-" * 40)

    def list_today(self, use_current_dir, custom_dir):
        """列出今天的日志"""
        base_dir, _ = self.determine_path(use_current_dir, custom_dir)
        today = datetime.date.today().strftime("%Y-%m-%d")
        filepath = os.path.join(base_dir, f"{today}.md")

        if not os.path.exists(filepath):
            if self.compact:
                print("💭 No logs for today")
            else:
                self._print(f"{self.c.GRAY}No logs found for today.{self.c.RED}")
            return 0

        if not self.compact:
            self._print(f"\n{self.c.BOLD}📋 Today's Logs ({filepath}){self.c.RED}\n")
        with open(filepath, "r", encoding="utf-8") as f:
            print(f.read())
        return 0

    def parse_log_file(self, filepath):
        """解析日志文件，返回按分类聚合的条目"""
        if not os.path.exists(filepath):
            return {}

        entries = {cat: [] for cat in self.CATEGORIES.keys()}

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_detail = []
            current_entry = None

            for line in lines:
                if line.startswith("### "):
                    # 保存前一个条目的 detail
                    if current_entry:
                        entries[current_entry["category"]].append({
                            "title": current_entry["title"],
                            "time": current_entry["time"],
                            "project": current_entry["project"],
                            "detail": "\n".join(current_detail).strip()
                        })

                    # 解析新条目: ### [14:30] `@project` CATEGORY: title
                    current_entry = None
                    current_detail = []

                    # 提取 category 和 title
                    for cat in self.CATEGORIES.keys():
                        cat_pattern = f"{cat.upper()}: "
                        if cat_pattern in line:
                            title = line.split(cat_pattern)[1].strip()
                            current_entry = {
                                "category": cat,
                                "title": title,
                                "time": "未知",
                                "project": "未知"
                            }
                            # 提取时间
                            time_match = re.search(r'\[(\d{2}:\d{2})\]', line)
                            if time_match:
                                current_entry["time"] = time_match.group(1)
                            # 提取项目
                            proj_match = re.search(r'`(@[^`]+)`', line)
                            if proj_match:
                                current_entry["project"] = proj_match.group(1)
                            break

                elif line.startswith("> ") and current_entry:
                    current_detail.append(line[2:].strip())

            # 保存最后一个条目
            if current_entry:
                entries[current_entry["category"]].append({
                    "title": current_entry["title"],
                    "time": current_entry["time"],
                    "project": current_entry["project"],
                    "detail": "\n".join(current_detail).strip()
                })

        except (IOError, UnicodeDecodeError) as e:
            if self.verbose:
                self._print(f"Warning: Failed to parse {filepath} - {e}", self.c.YELLOW)

        return entries

    def generate_weekly(self, days=7, use_current_dir=False, custom_dir=None, ai_summary=False, copy_clipboard=False):
        """生成周报"""
        base_dir, _ = self.determine_path(use_current_dir, custom_dir)

        # 收集指定天数内的日志
        all_entries = {cat: [] for cat in self.CATEGORIES.keys()}
        date_range = []

        for i in range(days):
            date = datetime.date.today() - datetime.timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            filepath = os.path.join(base_dir, f"{date_str}.md")

            if os.path.exists(filepath):
                date_range.append(date_str)
                entries = self.parse_log_file(filepath)
                for cat, items in entries.items():
                    all_entries[cat].extend([(date_str, item) for item in items])

        if not date_range:
            if self.compact:
                print(f"💭 No logs in the past {days} days")
            else:
                print()
                self._print(f"{self.c.GRAY}No logs found in the past {days} days.{self.c.RED}")
                print()
            return 0

        # 生成周报
        if not self.compact:
            print()
            print(f"{self.c.BOLD}{self.c.BLUE}{'=' * 50}{self.c.RED}")
            print(f"{self.c.BOLD}📊 周 报 / Weekly Report{self.c.RED}")
            print(f"{self.c.BLUE}{'=' * 50}{self.c.RED}")
            print()

        # 按分类输出
        category_order = ["incident", "feat", "design", "ops", "bug", "learn", "misc"]

        for cat in category_order:
            items = all_entries[cat]
            if not items:
                continue

            cat_info = self.CATEGORIES[cat]
            print(f"{cat_info['emoji']} **{cat_info['desc']}** ({len(items)})")
            print()

            for date_str, item in items:
                detail_preview = item["detail"][:60] + "..." if item["detail"] and len(item["detail"]) > 60 else (item["detail"] or "")
                print(f"  - {item['title']}")
                if detail_preview:
                    print(f"    <small>{detail_preview}</small>")
            print()

        # 日期范围（仅在非 compact 模式显示）
        if not self.compact:
            print(f"{self.c.GRAY}{'─' * 40}{self.c.RED}")
            print(f"{self.c.GRAY}📅 {date_range[-1]} ~ {date_range[0]}  |  共 {len(date_range)} 天有记录{self.c.RED}")
            print()

        # AI 总结和复制功能
        if ai_summary or copy_clipboard:
            # 构建日志内容用于 AI 总结
            log_content = []
            for cat in category_order:
                items = all_entries[cat]
                if items:
                    cat_info = self.CATEGORIES[cat]
                    log_content.append(f"{cat_info['emoji']} {cat_info['desc']}:")
                    for date_str, item in items:
                        log_content.append(f"  - {item['title']}")
                        if item['detail']:
                            log_content.append(f"    {item['detail']}")
            
            log_text = "\n".join(log_content)
            
            if ai_summary:
                print()
                print(f"{self.c.BOLD}{self.c.BLUE}🤖 正在调用 Claude Code 生成 AI 总结...{self.c.RED}")
                print(f"{self.c.GRAY}ℹ️  请稍候，这可能需要 10-30 秒{self.c.RED}")
                print()
                
                summary = call_claude_for_summary(log_text, "weekly")
                
                if summary:
                    print(f"{self.c.BOLD}{self.c.GREEN}✨ AI 总结完成！{self.c.RED}")
                    print()
                    print(f"{self.c.BOLD}────────────────────{self.c.RED}")
                    print(summary)
                    print(f"{self.c.BOLD}────────────────────{self.c.RED}")
                    print()
                    
                    # 如果需要复制，使用 AI 总结的内容
                    if copy_clipboard:
                        clean_text = markdown_to_rtf(summary)
                        if copy_to_clipboard(clean_text):
                            print(f"{self.c.GREEN}✅ AI 总结已复制到剪贴板，可直接粘贴使用{self.c.RED}")
                else:
                    print(f"{self.c.YELLOW}⚠️  AI 总结失败{self.c.RED}")
                    # AI 总结失败，使用原始内容
                    if copy_clipboard:
                        clean_text = markdown_to_rtf(log_text)
                        if copy_to_clipboard(clean_text):
                            print(f"{self.c.GREEN}✅ 已复制原始内容到剪贴板{self.c.RED}")
            elif copy_clipboard:
                # 只复制不总结
                clean_text = markdown_to_rtf(log_text)
                if copy_to_clipboard(clean_text):
                    print(f"{self.c.GREEN}✅ 已复制到剪贴板{self.c.RED}")

        return 0

    def generate_daily_summary(self, use_current_dir=False, custom_dir=None, ai_summary=False, copy_clipboard=False):
        """生成当日工作总结"""
        base_dir, _ = self.determine_path(use_current_dir, custom_dir)
        today = datetime.date.today().strftime("%Y-%m-%d")
        filepath = os.path.join(base_dir, f"{today}.md")

        if not os.path.exists(filepath):
            if self.compact:
                print("💭 No logs for today")
            else:
                print()
                self._print(f"{self.c.GRAY}No logs found for today.{self.c.RED}")
                print()
            return 0

        # 解析当日日志
        entries = self.parse_log_file(filepath)
        
        # 统计总数
        total_count = sum(len(items) for items in entries.values())
        
        if total_count == 0:
            if self.compact:
                print("💭 No logs for today")
            else:
                print()
                self._print(f"{self.c.GRAY}No logs found for today.{self.c.RED}")
                print()
            return 0

        # 生成日报标题
        if not self.compact:
            print()
            print(f"{self.c.BOLD}{self.c.BLUE}{'=' * 50}{self.c.RED}")
            print(f"{self.c.BOLD}📝 日 报 / Daily Summary - {today}{self.c.RED}")
            print(f"{self.c.BLUE}{'=' * 50}{self.c.RED}")
            print()

        # 工作概览
        print(f"📊 **今日工作概览** (共 {total_count} 项)")
        print()
        
        category_order = ["incident", "feat", "design", "ops", "bug", "learn", "misc"]
        for cat in category_order:
            items = entries[cat]
            if items:
                cat_info = self.CATEGORIES[cat]
                print(f"  {cat_info['emoji']} {cat_info['desc']}: {len(items)} 项")
        print()

        # 详细列表
        print("📋 **详细列表**")
        print()
        
        for cat in category_order:
            items = entries[cat]
            if not items:
                continue

            cat_info = self.CATEGORIES[cat]
            print(f"{cat_info['emoji']} **{cat_info['desc']}**")
            print()

            for item in items:
                time_str = f"[{item['time']}]" if item['time'] != "未知" else ""
                print(f"  - {time_str} {item['title']}")
                if item['detail']:
                    detail_lines = item['detail'].split('\n')
                    for line in detail_lines:
                        if line.strip():
                            print(f"    · {line.strip()}")
            print()

        # 底部信息（仅在非 compact 模式显示）
        if not self.compact:
            print(f"{self.c.GRAY}{'─' * 40}{self.c.RED}")
            print(f"{self.c.GRAY}📅 {today}  |  共完成 {total_count} 项工作{self.c.RED}")
            print()

        # AI 总结和复制功能
        if ai_summary or copy_clipboard:
            # 构建日志内容用于 AI 总结
            log_content = []
            for cat in ["incident", "feat", "design", "ops", "bug", "learn", "misc"]:
                items = entries[cat]
                if items:
                    cat_info = self.CATEGORIES[cat]
                    log_content.append(f"{cat_info['emoji']} {cat_info['desc']}:")
                    for item in items:
                        log_content.append(f"  - {item['title']}")
                        if item['detail']:
                            log_content.append(f"    {item['detail']}")
            
            log_text = "\n".join(log_content)
            
            if ai_summary:
                print()
                print(f"{self.c.BOLD}{self.c.BLUE}🤖 正在调用 Claude Code 生成 AI 总结...{self.c.RED}")
                print(f"{self.c.GRAY}ℹ️  请稍候，这可能需要 10-30 秒{self.c.RED}")
                print()
                
                summary = call_claude_for_summary(log_text, "daily")
                
                if summary:
                    print(f"{self.c.BOLD}{self.c.GREEN}✨ AI 总结完成！{self.c.RED}")
                    print()
                    print(f"{self.c.BOLD}────────────────────{self.c.RED}")
                    print(summary)
                    print(f"{self.c.BOLD}────────────────────{self.c.RED}")
                    print()
                    
                    # 如果需要复制，使用 AI 总结的内容
                    if copy_clipboard:
                        clean_text = markdown_to_rtf(summary)
                        if copy_to_clipboard(clean_text):
                            print(f"{self.c.GREEN}✅ AI 总结已复制到剪贴板，可直接粘贴使用{self.c.RED}")
                else:
                    print(f"{self.c.YELLOW}⚠️  AI 总结失败{self.c.RED}")
                    # AI 总结失败，使用原始内容
                    if copy_clipboard:
                        clean_text = markdown_to_rtf(log_text)
                        if copy_to_clipboard(clean_text):
                            print(f"{self.c.GREEN}✅ 已复制原始内容到剪贴板{self.c.RED}")
            elif copy_clipboard:
                # 只复制不总结
                clean_text = markdown_to_rtf(log_text)
                if copy_to_clipboard(clean_text):
                    print(f"{self.c.GREEN}✅ 已复制到剪贴板{self.c.RED}")

        return 0


def parse_arguments():
    """解析命令行参数 - 支持简洁调用格式"""
    import sys

    # 检查是否是 list 命令
    if len(sys.argv) > 1 and sys.argv[1] in ("list", "ls"):
        # 创建专门的 parser，只处理 list 相关参数
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--here", action="store_true")
        parser.add_argument("--path")
        parser.add_argument("--compact", action="store_true")
        # 只解析 --here 和 --path 之后的参数，跳过第一个 'list'
        args, _ = parser.parse_known_args(sys.argv[2:])
        return {"mode": "list", "here": args.here, "path": args.path, "compact": args.compact}

    # 检查是否是 weekly 命令
    if len(sys.argv) > 1 and sys.argv[1] in ("weekly", "week"):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--here", action="store_true")
        parser.add_argument("--path")
        parser.add_argument("-d", "--days", type=int, default=7)
        parser.add_argument("--compact", action="store_true")
        parser.add_argument("--ai", "--ai-summary", dest="ai_summary", action="store_true", help="Generate AI summary using Claude")
        parser.add_argument("--copy", "--clipboard", dest="copy_clipboard", action="store_true", help="Copy to clipboard")
        args, _ = parser.parse_known_args(sys.argv[2:])
        return {"mode": "weekly", "here": args.here, "path": args.path, "days": args.days, "compact": args.compact, "ai_summary": args.ai_summary, "copy_clipboard": args.copy_clipboard}

    # 检查是否是 daily 命令
    if len(sys.argv) > 1 and sys.argv[1] in ("daily", "today", "summary"):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--here", action="store_true")
        parser.add_argument("--path")
        parser.add_argument("--compact", action="store_true")
        parser.add_argument("--ai", "--ai-summary", dest="ai_summary", action="store_true", help="Generate AI summary using Claude")
        parser.add_argument("--copy", "--clipboard", dest="copy_clipboard", action="store_true", help="Copy to clipboard")
        args, _ = parser.parse_known_args(sys.argv[2:])
        return {"mode": "daily", "here": args.here, "path": args.path, "compact": args.compact, "ai_summary": args.ai_summary, "copy_clipboard": args.copy_clipboard}

    # 检查是否是配置命令
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        if len(sys.argv) > 2 and sys.argv[2] in ("reset", "--reset", "-r"):
            return {"mode": "config-reset"}
        if len(sys.argv) > 2 and sys.argv[2] in ("show", "--show", "-s"):
            return {"mode": "config-show"}
        return {"mode": "config-show"}

    # 默认模式：添加日志
    # 支持: dlog <category> <content> [options]
    parser = argparse.ArgumentParser(
        description="dlog - Daily Work Logger for Developers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dlog incident "首页Crash" -d "NPE in FeedAdapter"
  dlog feat "点赞功能" --here
  dlog design "缓存策略" --path ~/custom/path
  dlog list --here
  dlog config show
  dlog config reset
        """
    )
    parser.add_argument("category", choices=list(Logger.CATEGORIES.keys()))
    parser.add_argument("content", help="Summary title (short)")
    parser.add_argument("-d", "--detail", help="Detailed context", default="")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--here", action="store_true", help="Save to ./.dlog (project level)")
    group.add_argument("--path", metavar="DIR", help="Save to custom directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--compact", action="store_true", help="Compact output for launchers (Raycast/Alfred)")

    args = parser.parse_args()
    return {
        "mode": "write",
        "category": args.category,
        "content": args.content,
        "detail": args.detail,
        "here": args.here,
        "path": args.path,
        "verbose": args.verbose,
        "compact": args.compact,
    }


def main():
    """主入口"""
    args = parse_arguments()

    # 配置命令不需要初始化 Logger
    if args["mode"] == "config-reset":
        Config.reset()
        return 0

    if args["mode"] == "config-show":
        config = Config(auto_init=False)
        print()
        print("📋 devlog Configuration")
        print("-" * 30)
        print(f"Config file: {CONFIG_FILE}")
        if os.path.exists(CONFIG_FILE):
            print(f"Status:      ✅ Configured")
        else:
            print(f"Status:      ⚠️  Not configured (will prompt on first use)")
        print(f"Global dir:  {config.global_dir}")
        print()
        return 0

    # 其他命令需要初始化 Logger（会触发首次配置）
    config = Config()
    logger = Logger(verbose=args.get("verbose", False), compact=args.get("compact", False), config=config)

    if args["mode"] == "list":
        return logger.list_today(args.get("here", False), args.get("path"))

    if args["mode"] == "weekly":
        return logger.generate_weekly(
            days=args.get("days", 7),
            use_current_dir=args.get("here", False),
            custom_dir=args.get("path"),
            ai_summary=args.get("ai_summary", False),
            copy_clipboard=args.get("copy_clipboard", False)
        )

    if args["mode"] == "daily":
        return logger.generate_daily_summary(
            use_current_dir=args.get("here", False),
            custom_dir=args.get("path"),
            ai_summary=args.get("ai_summary", False),
            copy_clipboard=args.get("copy_clipboard", False)
        )

    # write mode
    return logger.write(
        args["category"],
        args["content"],
        args["detail"],
        args.get("here", False),
        args.get("path")
    )


if __name__ == "__main__":
    sys.exit(main())
