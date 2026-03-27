# 如何将 GitHub Copilot 网页 Chat 设置为简体中文

本指南介绍三种方法，帮助你把 GitHub Copilot 网页版 Chat（copilot.github.com）的界面语言切换为简体中文。按照以下步骤逐一尝试，直到界面显示为中文为止。

---

## 方法一：修改 GitHub 账号显示语言（推荐）

GitHub 网页 Chat 的界面语言默认跟随你的 GitHub 账号语言偏好。

1. 登录 [github.com](https://github.com)。
2. 点击页面右上角的**头像**，选择 **Settings（设置）**。

   > 截图占位符：`[账号设置入口截图]`

3. 在左侧导航栏向下滚动，找到 **Appearance（外观）** 或 **Account（账号）** 部分（具体名称因版本而异）。
4. 找到 **Language / Display language（显示语言）** 选项，从下拉菜单中选择 **简体中文 (Simplified Chinese)**。

   > 截图占位符：`[语言下拉菜单截图 – 显示"简体中文"选中状态]`

5. 点击 **Save（保存）** 按钮。
6. 刷新浏览器，访问 [copilot.github.com](https://copilot.github.com)，界面应已切换为中文。

**期望看到的中文 UI 文本示例：**

| 英文原文 | 切换后中文显示 |
|---|---|
| Ask Copilot | 向 Copilot 提问 |
| New conversation | 新建对话 |
| Suggestions | 建议 |
| Sign out | 退出登录 |

---

## 方法二：检查 Copilot 网页语言切换器

部分版本的 Copilot 网页在界面内提供了独立的语言切换器。

1. 打开 [copilot.github.com](https://copilot.github.com)。
2. 查看页面**底部页脚区域**，寻找语言名称（例如 "English"）或地球图标（🌐）。

   > 截图占位符：`[页脚语言切换器截图]`

3. 点击该语言标签，在弹出的列表中选择 **中文 (简体)**。
4. 页面刷新后界面即变为中文。

> **提示：** 如果找不到语言切换器，说明当前版本的 Copilot 网页不提供独立切换入口，请使用方法一或方法三。

---

## 方法三：调整浏览器首选语言

当 GitHub 账号设置无效，或你希望所有中文网站都优先显示中文时，可以修改浏览器语言优先级。

### Chrome / Edge

1. 打开浏览器设置（地址栏输入 `chrome://settings/languages` 或 `edge://settings/languages`）。
2. 在 **语言** 部分，点击 **添加语言**，搜索并添加 **中文（简体）**（`zh-CN`）。

   > 截图占位符：`[Chrome 语言设置页截图 – 添加 zh-CN]`

3. 将 **中文（简体）** 拖动到列表最顶部（最高优先级）。
4. 如提示，点击 **以该语言显示 Google Chrome** 或 **重启**。
5. 重启浏览器后，访问 [copilot.github.com](https://copilot.github.com)，界面应显示为中文。

### Firefox

1. 打开 `about:preferences`，找到 **语言与外观** → **选择您偏好的显示语言**。
2. 点击 **选择** → 搜索 **中文（简体）**，添加并移动到列表顶部。
3. 重启 Firefox 后刷新 Copilot 页面。

### Safari（macOS）

1. 打开 **系统设置** → **语言与地区** → **首选语言**。
2. 点击 `+`，搜索并添加 **简体中文**，拖到列表首位。
3. 重启 Safari 后访问 Copilot 网页。

---

## 常见问题

**Q：按照上述步骤操作后，界面仍显示英文，怎么办？**

- 确保在方法一中点击了**保存**，并**强制刷新**页面（`Ctrl + Shift + R` / `Cmd + Shift + R`）。
- 如果使用 VPN 或代理，尝试关闭后重试。
- 清除浏览器缓存和 Cookie 后再访问 Copilot 网页。

**Q：Copilot Chat 的回复语言也能切换成中文吗？**

是的。即使界面语言还是英文，你也可以在对话开始时直接输入：

```
请用中文回答我所有问题。
```

Copilot 会在整个对话中以中文回复。

---

## 相关链接

- [web-language-preference.md](./web-language-preference.md) – 在 Chat UI 中添加语言切换开关的设计提案
- [GitHub 账号设置](https://github.com/settings/profile)
- [Copilot 网页版](https://copilot.github.com)
