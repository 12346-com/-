# 鹿鸣的记忆库 - 自我引导说明

> 每次新会话必读。

---

## 一、系统简介

用 **SQLite 数据库**（单一数据源）存储对话记忆。

**核心定位：记忆库 = 对话记录**
- 每6小时自动总结对话内容（0:00、6:00、12:00、18:00），存入 SQLite
- 记住聊了什么、用户反馈了什么、做了什么决定
- 偏短期、动态、会话导向
- 每次新会话读取记忆库，了解近期对话上下文

**知识库 ≠ 记忆库**
- 知识库（`鹿鸣的知识库/`）存长期静态知识：用户画像、技术笔记、项目进度、重要锚点
- 知识库由 AI 主动维护：遇到大事件、重要决定、用户偏好变化、项目进展时更新
- 记忆库是对话记录，知识库是提炼后的长期记忆

**数据库路径：** `/root/data/workspaces/default_FriendMessage_3565912658/鹿鸣的记忆库/memory.db`

---

## 二、表结构

```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,           -- 'event'(事件), 'knowledge'(知识), 'decision'(决定)
    content TEXT NOT NULL,        -- 内容
    importance INTEGER DEFAULT 3, -- 重要性 1-5
    created_at TEXT NOT NULL,     -- 创建日期 YYYY-MM-DD
    created_at_full TEXT,         -- 完整时间 YYYY-MM-DD HH:MM
    week TEXT NOT NULL            -- 归档周数 YYYY-WW
);
```

---

## 三、操作说明

### 3.1 存入记忆

AI 认为重要时，直接执行 SQL INSERT：

```sql
INSERT INTO memories (type, content, importance, created_at, created_at_full, week)
VALUES ('event', '内容', 3, '2026-05-02', '2026-05-02 17:30', '2026-W18');
```

**type 规则：**
- `event` - 一般事件
- `knowledge` - 知识/偏好
- `decision` - 重要决定

**importance 规则：**
- 5 = 重要决定、用户偏好
- 4 = 项目进展、关键信息
- 3 = 一般事件
- 2 = 闲聊（一般不存）
- 1 = 可遗忘

### 3.2 搜索记忆

```sql
SELECT * FROM memories
WHERE content LIKE '%关键词%'
ORDER BY importance DESC, created_at_full DESC
LIMIT 5;
```

### 3.3 压缩清理

每天凌晨3点执行 `compress.py`，根据重要性分级保留：

| 重要性 | 保留时长 |
|--------|----------|
| 5 | 30 天 |
| 4 | 14 天 |
| 3 | 7 天 |
| 2 | 3 天 |
| 1 | 1 天 |

### 3.4 统计

```sql
SELECT type, COUNT(*) FROM memories GROUP BY type;
SELECT COUNT(*) FROM memories;
```

---

## 四、自动总结（每6小时）

1. AI 回顾过去6小时对话
2. 提取关键信息
3. 生成总结 + 标签
4. 调用 `auto_summarize.py` 的 `insert_memory()` 存入 SQLite

---

## 五、自主记录规则

遇到以下情况，主动 INSERT：
- 重要决定 → type=decision, importance=5
- 项目进展 → type=event, importance=4
- 用户偏好 → type=knowledge, importance=5
- 关键信息 → type=knowledge, importance=4
- 待办事项 → type=event, importance=3

---

## 六、工具

**视觉识别脚本：** `鹿鸣的记忆库/tools/glm_vision.py`

```bash
python3 鹿鸣的记忆库/tools/glm_vision.py <图片路径> [提示词]
```

---

## 七、文件结构

```
鹿鸣的记忆库/
├── memory.db            # SQLite 数据库（唯一数据源）
├── auto_summarize.py    # 自动总结脚本
├── compress.py          # 分级清理脚本
├── compress.log         # 清理日志（自动生成）
├── SELF_GUIDE.md        # 本文件
└── tools/
    └── glm_vision.py    # GLM-4.6V 视觉识别
```

---

*最后更新：2026-05-02（重构：废弃 JSON 双轨，统一 SQLite，分级压缩）*
