#!/usr/bin/env python3
"""
鹿鸣记忆系统 - 每6小时自动总结脚本
由 AstrBot cron 触发，总结过去6小时的对话并存入 SQLite（唯一数据源）
"""

import sqlite3
from datetime import datetime

DB_PATH = "/root/data/workspaces/default_FriendMessage_3565912658/鹿鸣的记忆库/memory.db"


def ensure_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            importance INTEGER DEFAULT 3,
            created_at TEXT NOT NULL,
            created_at_full TEXT,
            week TEXT NOT NULL
        )
    """)
    # 兼容旧表：如果缺少 created_at_full 列则添加
    cols = [c[1] for c in conn.execute("PRAGMA table_info(memories)").fetchall()]
    if "created_at_full" not in cols:
        conn.execute("ALTER TABLE memories ADD COLUMN created_at_full TEXT")
        # 回填已有数据
        conn.execute("UPDATE memories SET created_at_full = created_at WHERE created_at_full IS NULL")
    conn.commit()
    conn.close()


def insert_memory(mtype, content, importance):
    """插入记忆到 SQLite"""
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    full = now.strftime("%Y-%m-%d %H:%M")
    week = now.strftime("%GW%V")

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO memories (type, content, importance, created_at, created_at_full, week) VALUES (?, ?, ?, ?, ?, ?)",
        (mtype, content, importance, today, full, week)
    )
    conn.commit()
    conn.close()
    print(f"[{full}] 记忆已存入: [{mtype}] {content[:50]}...")


if __name__ == "__main__":
    ensure_table()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 鹿鸣记忆系统 - 自动总结脚本就绪")
    print("此脚本由 AstrBot cron 触发，总结内容由 AI 生成后调用 insert_memory() 存入数据库")
