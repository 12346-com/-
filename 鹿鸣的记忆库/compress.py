#!/usr/bin/env python3
"""
鹿鸣记忆系统 - 定期压缩清理脚本
根据重要性分级保留，低重要性短期清理，高重要性长期保留
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = "/root/data/workspaces/default_FriendMessage_3565912658/鹿鸣的记忆库/memory.db"

# 保留策略（天数）
RETENTION = {
    5: 30,   # 重要决定、用户偏好
    4: 14,   # 项目进展、关键信息
    3: 7,    # 一般事件
    2: 3,    # 闲聊
    1: 1,    # 可遗忘
}


def compress():
    """根据重要性分级清理过期记忆"""
    conn = sqlite3.connect(DB_PATH)
    now = datetime.now()
    
    total_before = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    deleted_total = 0
    detail = []
    
    for importance, days in sorted(RETENTION.items()):
        cutoff = (now - timedelta(days=days)).strftime("%Y-%m-%d")
        cursor = conn.execute(
            "SELECT COUNT(*) FROM memories WHERE importance = ? AND created_at < ?",
            (importance, cutoff)
        )
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.execute(
                "DELETE FROM memories WHERE importance = ? AND created_at < ?",
                (importance, cutoff)
            )
            deleted_total += count
            detail.append(f"  重要性{importance}: 删除{count}条 (>{days}天前, 截止{cutoff})")
    
    conn.commit()
    total_after = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    conn.close()
    
    # 日志
    log = [
        f"[{now.strftime('%Y-%m-%d %H:%M')}] 压缩完成",
        f"  压缩前: {total_before} 条",
        f"  压缩后: {total_after} 条",
        f"  共删除: {deleted_total} 条",
    ] + detail
    
    log_text = "\n".join(log)
    print(log_text)
    
    # 写入日志文件
    log_dir = os.path.dirname(DB_PATH)
    log_file = os.path.join(log_dir, "compress.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_text + "\n\n")
    
    return log_text


if __name__ == "__main__":
    compress()
