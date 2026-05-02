# fnhdd.xyz 网站

## 编辑器

- **访问地址**：https://fnhdd.xyz/code-editor.html
- **脚本目录**：https://fnhdd.xyz/code/scripts/（静态文件访问）

### 目录结构
```
workspace/
├── code/
│   ├── scripts/          ← 存放所有预览脚本
│   ├── scripts.json      ← 脚本列表（自动生成）
│   └── scan_scripts.py   ← 脚本扫描器
├── code-editor.html      ← 编辑器页面
└── 鹿鸣的知识库/
```

### 构建步骤
1. 创建 HTML 文件：`code-editor.html`（纯静态，无需构建）
2. nginx 已配置 root 指向 workspace 目录
3. 新增脚本后运行 `python3 code/scan_scripts.py` 更新列表

### 编辑器功能
- **左侧**：脚本列表（自动加载 scripts.json）
- **中间**：代码输入框（textarea）
- **右侧**：iframe 实时预览
- **▶ 运行**：手动运行代码（或 Ctrl+Enter）
- **🔄 刷新脚本**：重新扫描脚本目录
- **📋 示例代码**：加载计数器示例
- **🗑️ 清空**：清空编辑器
- **拖拽分隔条**：调整面板宽度

---

## 主页

- **服务**：Python HTTP 服务在 8080 端口（`/root/fnhdd_server.py`）
- **反代**：Nginx 443 → 8080，Let's Encrypt 证书（E8 签名）
- **当前页面**：「超级更新中」
- **问题**：从外部访问一直加载中，curl 本地正常（200），但外部请求未到达服务器
- **待排查**：DNS 解析是否正确、运营商是否屏蔽 443

### nginx 配置
- 配置文件：`/etc/nginx/sites-enabled/fnhdd`
- root 目录：`/root/data/workspaces/default_FriendMessage_3565912658`
- SSL 证书：`/etc/letsencrypt/live/fnhdd.xyz-0002/`
- ⚠️ `/root` 目录权限需为 755，否则 nginx 返回 403

---

## 控制面板

- **地址**：https://fnhdd.xyz/dashboard/
- **后端**：Python HTTP Server 在 8222 端口
- **功能**：记忆库管理、知识库编辑、项目进度查看

---

## 状态：⚠️ 主页待修复

---

*最后更新：2026-05-02*
