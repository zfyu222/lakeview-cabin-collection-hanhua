# Lakeview Cabin Collection 汉化项目

## 游戏信息
- 原名：Lakeview Cabin Collection
- 中文名：湖景小屋合集（项目暂译，非官方中文名）
- 开发商 / 发行商：Roope Tamminen
- 发行平台：Steam，App ID 361990；商店发售日期 2015-03-25。
- 本次目标平台：Windows；本地 Steam Build ID 2415026。
- 引擎：Unity 5.3.4f1（本地 output_log.txt 与资源头确认），Mono 托管脚本，PlayMaker 状态机。
- 原语言：商店列出英语界面、完整音频与字幕；资源中另有少量芬兰语致谢。
- 游戏安装目录：`D:/Program Files (x86)/Steam/steamapps/common/Lakeview Cabin Collection`，通过 `Game/` junction 引用。

## 游戏简介
以七八十年代恐怖电影为灵感的二维动作解谜游戏。玩家操控同伴，利用场景物品求生，各章节有不同主题与机制。商店介绍四个主要篇章；本地版本还包含额外模式。开发者的成人内容提示包含低分辨率裸体及性场景。
来源：[Steam 官方商店](https://store.steampowered.com/app/361990/Lakeview_Cabin_Collection/)。

## 汉化目标
- 范围：先完成可复现的文本与字体汉化尝试，并覆盖关键菜单图片；图片、场景及隐藏内容需分别核对，未验证前不宣称全覆盖。
- 目标语言：简体中文。
- 文体：恐怖片与黑色幽默，便条自然直白，角色社交动态保留口语、粗俗语气与笑点；不补写背景。工作人员姓名保留原文。

## 技术栈
| 环节 | 工具 | 版本 |
|------|------|------|
| 提取 | dnSpy.Console、UnityPy、TypeTreeGeneratorAPI | UnityPy 1.25.4；其余见 Analysis 证据 |
| 翻译 | game-translate 共用 API 流程 | 用户选择 API，沿用 api.local.jsonc 默认项 |
| 回填 | 待验证 | 待定 |

## 文本提取
- 文本位置：`*_Data/level*` 的 TextMesh、PlayMakerFSM 数据；部分菜单与便条为 Texture2D 图片。
- 托管程序集：`Managed/Assembly-CSharp.dll`，源码分析副本在 `Analysis/decompiled/`。
- 脚本：`Analysis/scan_assets.py`（资源清单、TextMesh、字体、源哈希）；`Analysis/scan_playmaker.py`（状态机字段定位）。
- 重建托管类型时发现 TypeTreeGeneratorAPI 对旧版 MonoBehaviour 头与原始类型数组产生不适合 UnityPy 的节点；项目适配在 `Analysis/managed_types.py`，只影响内存读取，不修改工具全局安装。
- 图片预览：`Analysis/images/`，`Analysis/preview_images.py` 可重建。
- 完整提取数量、来源映射与排除规则：分析结束后补充。

## 翻译
- 路线：API；用户 2026-10-23 明确选择，授权沿用工作区现有配置。
- 当前默认 API：`yjapi`，模型 `deepseek-v4.1-flash`（启动时由本地配置读取，凭据不入项目）。
- 全部翻译中间产物放 `TranslateFiles/`；术语整理、语义审校和冻结先于正文。
- 当前状态：源文分析中，尚未发送翻译请求。

## 回填
- 计划：修改资源副本并替换动态字体；基于原文件哈希验证后部署，保留可恢复备份。
- 验证方法：实际启动，检查菜单、中文字体、便条、字幕、排版和章节切换。
- 当前状态：尚未回填。

## 已知问题
- 菜单、控制提示与部分便条使用图片文字，不能仅替换字符串。
- Crazy-creation 与 PressStart2P 为原游戏字体，需检查并补足中文字形。
- 场景存在占位文字、数字/房间代码和 FSM 内部标识，不能盲目翻译原始字符串清单。

## 对外发布
- 未发布；须通过实机验证后再制作补丁。

## 版本记录
- 2026-10-23：初始化独立 Git 仓库与 Game 链接，确认 Unity/Mono/PlayMaker 技术栈，开始提取及可行性验证。

### 本轮提取结果
- 61 条不同显示文本，映射到 476 个资源字段；10 个占位/编码实例保留原样。CSV 按逻辑记录对应，含多行引号字段，不以物理行计数。
- `Analysis/source_mapping.json` 记录每条 CSV 的资源文件、pathId、字段路径及动态 FSM 名；`source_hashes.json` 记录源资源 SHA-256。
- 共完整解析 14,525 个 PlayMaker 组件，解析错误为 0；从 Blurp/Blurber 显示动态、预填消息数组和加载日志属性选择实际文字，排除 FSM 状态名、事件名及内部键。
- 当前覆盖：场景笔记、职员表、计分/奖励标签及角色社交台词。图片文字未纳入本轮；托管代码检索发现的第三方测试/调试 UI 未纳入。
