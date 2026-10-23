# 翻译操作记录

- 工作流：custom
- 执行路线（codex=SubAgent，api=API）：api
- 原文：项目根目录 `lakeview-cabin-collection_text.csv`
- 正式译文：项目根目录 `lakeview-cabin-collection_text_translated.csv`
- 中间产物：`TranslateFiles/`

由 game-translate 技能调用共用流程程序；路线为 SubAgent（codex）或 API（api）。正文前完成全文术语整理及冻结。
试译：固定随机样本 → pilot_translate → pilot-report → 主 AI pilot-decide；按需 pilot-retry。
试译用于校准流程和风格，不要求逐句零错误；正式译文仍须完整独立审校和导出验收。

## 本轮交付（2026-10-23）
- API：yjapi / deepseek-v4.1-flash。首个503请求在用户授权后重试成功。
- 完成：全文术语提取、13项术语审校与冻结、61条试译校准、61条正式翻译、程序检查、全文独立六维语义审校、最终无争议闭环与正式导出。
- 61条译文对应476个资源字段。正式CSV原文/译文哈希及验收见 reports/final_validation.json。
- 占位符及格式：保留原有换行和数字，职员姓名保留原文；社交标签属于可翻译的游戏内文字。FSM内部键和状态不纳入翻译。
- 回填：16个资源文件及2个字体资源，本地试验版已部署；正常入口已恢复。
- 实机：启动及职员表中文诊断已检查；图片菜单仍英文，章节便条/台词/任务和长句布局待测，整体不是发布通过状态。

## 图片文字补充
- 15条新增图片文字另走 TranslateFiles/image-overlay 子流程，API、术语审校、试译、独立审校及导出均通过。
- 不改变原61条正式译文和原图，用独立运行时灰底中文层显示。待用户实机测试，不记录为全局实机验收通过。

## 图片漏译复查补充
- 新增93条，独立子流程 `image-audit/`，沿用 yjapi / deepseek-v4.1-flash；全文术语审校冻结、试译校准、正文、机械扫描及全文独立六维审校完成，最终无争议导出。
- 正式译文 `lakeview-cabin-collection_image_audit_text_translated.csv`，SHA-256 `7b8b985f2de93ad852b14eb03541bc9a042515ae7a68fd55c936976488e41777`。
- 保留撕裂截断、剧情内伪蓝屏语境、数字/按键及不可辨装饰文字；伪蓝屏只作为游戏文本翻译，不执行其中的命令含义。
- 93条翻译对应新增123个显示标签。COMBO在图集上可读但不在导出的精灵切片内，保留翻译记录而不覆盖倍率数字。实机检查待用户完成。
