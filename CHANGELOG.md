# CHANGELOG

所有版本变更记录。格式参考 Keep a Changelog，版本遵循语义化版本。

## [未发版] - 2026-11-16

### 新增
- `TUTORIAL.md`：新手引导（小白教程）——可直接复制的问题清单：装好验证 / 日常查询 / 补领 / 加账号 / 三句话急救 / 需求补充通道；README 顶部新增「小白怎么用」入口章节
- 维护规矩：问题清单按「遇到新问题就补进来」持续维护，每次补充随仓库推送记录本 CHANGELOG

## [v1.0.0] - 2026-11-16

### 新增
- `SKILL.md`：WorkBuddy 积分管家技能定义（通用版，无个人信息）
  - 自动化架构说明：上游脚本、多账号绑定、launchd 定时模板（00:05 首跑 + 每 4 小时轮询）
  - 脚本自动覆盖清单：签到 / 连登兑换 / 补登 / 任务接单领奖 / Buddy 旅行 / 盲盒 / 抽奖
  - 人工活动地图：邀请好友 / Agent 全应用检索隐藏款 / 小程序独立积分池 / 社区发文 / 问卷 / 兑换码
  - 智能体触发职责 + 兜底记账用法
- `scripts/checkin.py`：脚本失效时的本地签到记账兜底（mark / status / report / miss / card）
- `README.md`：30 秒说明、来源与依赖（88lin/workbuddy-auto-signin）、macOS 四步安装、
  Windows 指引、「不用问作者」常见问题自查表、安全风险必读、版本与回退
- `LICENSE`：MIT

### 依赖与致谢
- 签到引擎来自 [88lin/workbuddy-auto-signin](https://github.com/88lin/workbuddy-auto-signin)（MIT），本仓不含也不修改其代码

### 回退
```bash
git tag                       # 看所有版本
git checkout v1.0.0 -- 文件   # 回退单个文件
git checkout v1.0.0           # 整仓临时回看
```
