# 翻译操作记录

- 工作流：custom
- 执行路线（codex=SubAgent，api=API）：api
- 原文：项目根目录 `lakeview-cabin-collection-image-audit_text.csv`
- 正式译文：项目根目录 `lakeview-cabin-collection-image-audit_text_translated.csv`
- 中间产物：`TranslateFiles/`

由 game-translate 技能调用共用流程程序；路线为 SubAgent（codex）或 API（api）。正文前完成全文术语整理及冻结。
试译：固定随机样本 → pilot_translate → pilot-report → 主 AI pilot-decide；按需 pilot-retry。
试译用于校准流程和风格，不要求逐句零错误；正式译文仍须完整独立审校和导出验收。

## 2026-10-23 图片复查交付
- yjapi / deepseek-v4.1-flash；36项术语候选经审校并冻结。93条完成试译校准、正文、草稿检查及全文独立语义审校，最终0条遗留，正式导出通过；无须额外争议裁决。
- 原文SHA-256：c18542d4005d20f590da53ecf61fa7a324333d4ed385858b94f91167ac6d40ab。
- 译文SHA-256：7b8b985f2de93ad852b14eb03541bc9a042515ae7a68fd55c936976488e41777。
- 原文与正式译文同步至主项目根目录 image_audit_text CSV；保护数字、按键、截断和伪蓝屏剧情语境，字母拼图保留；翻译已验收，游戏验证待用户进行。
