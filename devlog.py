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

    def __init__(self, verbose=False, config=None):
        self.verbose = verbose
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
            self._print(f"{self.c.GRAY}No logs found for today.{self.c.RED}")
            return 0

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

    def generate_weekly(self, days=7, use_current_dir=False, custom_dir=None):
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

        # 生成周报
        print()
        print(f"{self.c.BOLD}{self.c.BLUE}{'=' * 50}{self.c.RED}")
        print(f"{self.c.BOLD}📊 周 报 / Weekly Report{self.c.RED}")
        print(f"{self.c.BLUE}{'=' * 50}{self.c.RED}")
        print()

        if not date_range:
            self._print(f"{self.c.GRAY}No logs found in the past {days} days.{self.c.RED}")
            return 0

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

        # 日期范围
        print(f"{self.c.GRAY}{'─' * 40}{self.c.RED}")
        print(f"{self.c.GRAY}📅 {date_range[-1]} ~ {date_range[0]}  |  共 {len(date_range)} 天有记录{self.c.RED}")
        print()

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
        # 只解析 --here 和 --path 之后的参数，跳过第一个 'list'
        args, _ = parser.parse_known_args(sys.argv[2:])
        return {"mode": "list", "here": args.here, "path": args.path}

    # 检查是否是 weekly 命令
    if len(sys.argv) > 1 and sys.argv[1] in ("weekly", "week"):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--here", action="store_true")
        parser.add_argument("--path")
        parser.add_argument("-d", "--days", type=int, default=7)
        args, _ = parser.parse_known_args(sys.argv[2:])
        return {"mode": "weekly", "here": args.here, "path": args.path, "days": args.days}

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

    args = parser.parse_args()
    return {
        "mode": "write",
        "category": args.category,
        "content": args.content,
        "detail": args.detail,
        "here": args.here,
        "path": args.path,
        "verbose": args.verbose,
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
    logger = Logger(verbose=args.get("verbose", False), config=config)

    if args["mode"] == "list":
        return logger.list_today(args.get("here", False), args.get("path"))

    if args["mode"] == "weekly":
        return logger.generate_weekly(
            days=args.get("days", 7),
            use_current_dir=args.get("here", False),
            custom_dir=args.get("path")
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
