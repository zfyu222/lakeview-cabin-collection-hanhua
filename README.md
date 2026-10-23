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
- 本轮提取：61条不同文本，476个字段，45个对象；映射见 Analysis/source_mapping.json，图片文字不在本轮覆盖中。

## 翻译
- 路线：API；用户 2026-10-23 明确选择，授权沿用工作区现有配置。
- 当前默认 API：`yjapi`，模型 `deepseek-v4.1-flash`（启动时由本地配置读取，凭据不入项目）。
- 全部翻译中间产物放 `TranslateFiles/`；术语整理、语义审校和冻结先于正文。
- 当前状态：61条正式译文已通过全文独立审校，并由程序 export 导出。

## 回填
- 计划：修改资源副本并替换动态字体；基于原文件哈希验证后部署，保留可恢复备份。
- 验证方法：实际启动，检查菜单、中文字体、便条、字幕、排版和章节切换。
- 当前状态：16个资源文件已部署为本地试验版；476个字段构建后逐项重读核对通过，正常启动及职员表诊断通过，后续场景仍待测。

## 已知问题
- 当前为部分汉化试验版：图片菜单/控制提示/部分图片便条仍为英文。
- 字体在职员表诊断中可显示中文，但字号偏小；章节便条、动态台词、剧情与任务未完成全流程实测。
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

## 首次服务故障记录（已恢复，2026-10-23）
- 提取完成并提交：61 条不同文本，476 个资源字段，45 个实际对象。完整 PlayMaker 解析 14,525 个组件，无解析失败。
- 读取/写回原始对象的无修改重建验证：45/45 字节一致，见 `Analysis/roundtrip_report.json`。这是文件结构验证，不是实机汉化验证。
- 工具版本：UnityPy 1.25.4、TypeTreeGeneratorAPI 0.0.10、fontTools 4.63.0。
- 字体候选：`Tools/Fonts/NotoSC/NotoSansSC-variable.ttf`，已核对中文及常用标点 cmap。构建脚本会实例化成静态字重 400 并按实际字符取子集；后续实机诊断已确认职员表中文显示，其他场景仍待测。
- `build_patch.py` 已准备：只读取正式导出 CSV，并核验 `final_validation.json` 的原文/译文 SHA-256；未通过流程导出时拒绝构建。按字段写资源副本，重读核对，并输出到 `Patch/`，不自动部署。
- API 状态：2026-10-23 首次 `extract` 请求返回 `InternalServerError:503`，没有可用结果，未开始正文。当时流程暂停；服务未报告 Token 用量，不推断为零费用。
- 执行回执：`TranslateFiles/reports/api_runs/a290c08a57ba497eb343e622d3756e4f.json`；待恢复 session：`e354a908a93045f6baada843381cb64c`。原执行器已结束，无重复请求在途。

## 翻译验收结果（2026-10-23）
- API：yjapi / deepseek-v4.1-flash；首次503后经用户授权重试成功，随后各阶段正常完成。
- 术语：r2，13个候选完成独立语义审校并冻结；文件 TranslateFiles/glossary/r2/freeze_47b6b570/built/glossary_reviewed.json。
- 61条试译由主AI阅读并接受；正文61条全部完成独立六维语义审校，结构/术语扫描0个剩余问题；无遗留争议，不触发额外Sol裁决。
- 占位符：保护原有换行、特殊字符、数字；职员署名原样保留，社交标签为游戏内自然语言，允许汉化。FSM状态名与内部键不翻译。
- 正式译文：lakeview-cabin-collection_text_translated.csv，SHA-256 29d7bdc552eacb4c240c77c73067baf6fa4ebaa10b146b8140458150cb1c80e0。
- 报告：TranslateFiles/reports/final_validation.json；实机状态尚未通过。

## 本地试验版安装与恢复
- 已部署：Patch/manifest.json 内16个资源文件，476处文字字段，并替换2个动态字体资源。
- 原文件备份：Backups/original/，按游戏根目录相对路径保存，不入库。
- 构建：python build_patch.py；要求正式原文/译文与 final_validation.json 的 SHA-256 一致，且游戏源文件为原版。
- 部署：先退出游戏，再运行 python deploy_patch.py。
- 恢复：先退出游戏，再运行 python deploy_patch.py --restore。脚本逐文件检查载荷、当前文件及备份的 SHA-256，遇到未知改动即停止。
- 图片菜单、标题及便条未处理，仍显示英文；本次不构成完整汉化发布。

## 回填实机检查（2026-10-23）
- 工具：UnityPy 1.25.4、TypeTreeGeneratorAPI 0.0.10、fontTools 4.63.0；静态实例化 Noto Sans SC 400 并按实际字符子集化。
- 已检查：正常启动进入城市/合集场景，打开和返回暂停菜单；未发现阻止场景加载的问题。原游戏日志包含缺失脚本/重复对象池提示，未据此断言由汉化引入。
- 中文诊断：临时将已汉化 level4 职员表资源作为 level0 启动，实际看到导演、感谢句等中文，无方框缺字；这是诊断入口，不是正常游玩抵达场景。
- 诊断后已关闭游戏，将原始 level0 恢复，SHA-256 与 source_hashes.json 一致。16个正式试验载荷均与 Patch/manifest.json 的哈希一致。
- 结果：部分验证。字体偏小，后续便条/动态台词的字体与长句排版、剧情及任务尚未完成实测，不能通过发布验收。
- 证据：Analysis/evidence/credits_diagnostic.png、Analysis/evidence/credits_chinese.png；测试报告 Analysis/game_test_report.json。
- 当前安装目录已保留本地试验版，可正常从 Steam 启动；未生成对外分发 ZIP。
