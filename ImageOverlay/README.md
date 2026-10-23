# 图片文字中文覆盖层

本轮采用独立的运行时文字层：原 Texture2D 和 Sprite 数据保持原样，在屏幕上对相应精灵追加深灰半透明底与中文。没有重新绘制或擦除原图。

## 当前覆盖
- 暂停菜单四项、退出/重开确认框。
- 手柄推荐提示及部分章节的继续、新游戏、附赠内容按钮。
- 营地欢迎信（保留签名与日期）、约定女厕所见面的便条、托付女儿的便条。
- 15 个精灵名称、20 个覆盖区，对应 15 条独立译文；覆盖表见 overlay_map.json。

## 用户测试
1. 自行启动游戏，打开暂停菜单，检查中文与高亮选项是否对应。
2. 按 F8 对照原图，再按 F8 恢复中文；覆盖层不应抢占按钮输入。
3. 遇到上述便条时检查位置、字号、换行和灰底范围；不同分辨率也建议各检查一次。

这里只完成静态校验，尚未在游戏中验证。实现通过 SpriteRenderer 的名称和投影位置定位；摄像机、排序或特效导致的错位需实机反馈后调整。世界内很小的便条图标不叠字，避免出现巨大提示框。

## 文件
- `ChineseOverlay.cs`：覆盖层逻辑；Windows 字体使用 Microsoft YaHei 等系统中文字体。
- `PatchBootstrap.cs`：仅在 SteamManager.Awake 开头增加安装覆盖层的一次调用。
- `build_overlay.py`：核验已通过翻译流程导出的 CSV，编译 DLL，验证挂接，生成本地预览及载荷清单；要求已构建基础 Patch。
- `preview.html` / `preview.png`：静态排版预览，非游戏截图。HTML 按钮可切换原图/覆盖效果。
- `static_check.py` / `static_validation.json`：验证部署哈希，核对原始 Texture2D 和 Sprite 数据未被修改。

## 构建与恢复
关闭游戏后在主项目目录运行：

```powershell
python ImageOverlay/build_overlay.py
python deploy_patch.py
```

整体恢复（同时还原前一轮文本试验版）仍为：

```powershell
python deploy_patch.py --restore
```

独立关闭图片中文层可直接按 F8；不需要还原原图。原 DLL 备份在 `Backups/original/Lakeview Cabin Collection_Data/Managed/Assembly-CSharp.dll`。首次新增的 `LakeviewChineseOverlay.dll` 还原时按哈希校验后删除。

用户不允许控制电脑或自行启动游戏；本轮只做文件、编译和静态渲染校验，实机测试由用户完成。静态预览由无窗口的网页渲染生成，未操作用户的浏览器或桌面。
