import os
import django
from django.core.management import call_command

# 设置 Django 项目的环境变量，指向项目的 settings 模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "algaecideDB.settings")

# 初始化 Django 环境
django.setup()

# 导出数据到 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", stdout=f, indent=2)
