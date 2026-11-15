---
name: buddy-checkin-keeper
description: WorkBuddy 积分管家——基于本机 88lin/workbuddy-auto-signin 脚本，支持多账号每日自动签到与成长中心全流程领取（签到、连登兑换、补登、任务领奖、Buddy 旅行、盲盒、抽奖）。含积分活动全景地图：哪些脚本自动覆盖、哪些需要人工操作。触发词：签到、打卡、领积分、Buddy 加油站、成长计划、积分活动、连签、补登卡、积分漏领。
agent_created: true
---

# WorkBuddy 积分管家（脚本全自动版）

本技能是 **WorkBuddy AI 助手（Agent）的技能包**。安装后，你的 WorkBuddy 智能体会按本文件的方法，
帮你运维每日积分领取：查状态、诊断失败、刷新凭据、提醒人工活动。

> **事实来源**：签到与成长中心状态一律以 `signin.py` 返回的服务端数据为准，
> 本技能 `data/checkin.json` 的本地记账仅作脚本失效时的兜底。

> **风险知情**：签到脚本通过逆向桌面端接口实现，官方规则将「利用脚本刷取活跃或奖励」列为禁止情形，
> 存在积分追回或账号处理风险。是否使用由你自行决定；使用前请备份你的 WorkBuddy 技能目录与资料库。

## 一、自动化架构（一次性装好，之后无人值守）

- **脚本**：`~/workbuddy-auto-signin/signin.py`（上游仓库：https://github.com/88lin/workbuddy-auto-signin ，腾讯改版后的修复都在那里发布）
- **账号清单**：`accounts/accounts.json`（凭据副本在 `accounts/`，等同密码，**禁止放入 iCloud / 同步网盘**）
- **定时**：launchd 任务 `workbuddy-auto-signin.plist`，每天 00:05 首跑 + 每 4 小时轮询补漏；
  `auto` 模式自动遍历全部已绑定账号，多账号无需额外配置
- **日志**：`~/workbuddy-auto-signin/signin.log`、`/tmp/workbuddy-auto-signin.out|.err`
- **常用命令**：

```bash
python3 ~/workbuddy-auto-signin/signin.py            # 签到+成长中心，全部账号
python3 ~/workbuddy-auto-signin/signin.py growth     # 仅成长中心
python3 ~/workbuddy-auto-signin/signin.py status     # 查签到状态
python3 ~/workbuddy-auto-signin/signin.py accounts   # 查绑定账号与凭据到期时间
cd ~/workbuddy-auto-signin && /usr/bin/python3 bind_one.py <账号名>   # 绑定/刷新当前客户端登录的账号
```

## 二、脚本自动覆盖的积分活动（每日，无需人工）

| 活动 | 说明 |
|---|---|
| 每日签到 | +100 积分/天，多账号各领一份 |
| 连登奖励兑换 | 7/14/28 天档位：积分、能量、补登卡、抽奖次数，自动兑换 |
| 断签自动补登 | 自动用补登卡补，上限 4 张 |
| 成长计划任务接单+领奖 | 自动 accept + claim（任务进度仍需实际使用客户端达成） |
| Buddy 旅行 | 领旅行礼物（10~20 积分/次）+ 自动派出，4 小时轮询接住返程 |
| 盲盒 | 能量 ≥10 自动开 |
| 限时连登抽奖 | 有抽奖次数自动抽 |

## 三、脚本覆盖不了、需要人工的活动（让智能体提醒你，它带路）

| 活动 | 入口 | 收益 | 备注 |
|---|---|---|---|
| 邀请好友 | 头像 → 去邀约 | 最高 650 分/人，好友注册得 2000 | 社交行为，不代做 |
| 隐藏款：Agent 全应用检索首次绑定 | 设置 → 智能体 → 开启 | +100（一次性限时） | 每个号各领一次 |
| 小程序独立积分池 | 微信搜「腾讯 WorkBuddy 小程序」→ 成长计划 | 独立于桌面端的积分池 | 与桌面端分开算，等于多领一份 |
| 社区发文 | 腾讯云开发者社区，带 #WorkBuddy# 标签原创 | 心得/教程/精选逐级提高 | 账号需与客户端一致 |
| 意见反馈/内测问卷 | 头像 → 意见反馈、官方内测招募 | 积分或体验金 | 审核制 |
| 官方群兑换码 | WorkBuddy 公众号/官方社群公告 | 不定期 | 在「套餐与积分」页兑换 |
| 限时/节日活动 | 客户端 banner、公众号 | 连登抽奖、打卡挑战等 | 当期为准 |

**做任务的省分技巧**：把模型切到 Hy3（限时免费 0.00x）再跑任务进度，几乎零消耗；
任务完成后必须回成长计划点「领取奖励」，不会自动到账。

## 四、成长计划任务样例（数值随档期浮动，以客户端为准）

新建任务并发起对话 300 ｜ 设计创意模式建画布 300 ｜ 探索优秀灵感 100 ｜ 桌面端对话 1 次 100 ｜
体验资料库 100 ｜ 体验「发现应用」100 ｜ 关注公众号满 24h 100 ｜ 体验指定专家 50 ｜
召唤 3 次专家团 100 ｜ 使用 5 个模板 100。一次性任务做完即止。

## 五、智能体职责（每次被触发时）

1. 被问到签到/积分 → 跑 `signin.py status` / `accounts` 用服务端数据汇报，不凭本地记录猜。
2. 发现 `needs_attention: true` 或连续失败 → 诊断（凭据过期最常见），提示用户在客户端登录对应账号后跑 `bind_one.py` 刷新。
3. 用户说做了某个人工活动 → 记录跟进，提醒去任务页点领取。
4. 每月 1 号提醒：积分当月有效不结转，补登卡计数重置。

## 六、WorkBuddy 之外的白嫖 token 渠道（独立账号，需本人注册）

以下与 WorkBuddy 积分无关，是第三方 API 平台，需要本人注册账号，智能体不代注册：

- **AgentRouter**（agentrouter.org）：公益 API 聚合，注册送额度，每日签到得额度，GitHub/LinuxDo 可登录，国内直连。
- **SheApi** 等中转平台：每日签到领免费额度。
- **Qoder CN**：每日 100 Credits，上游仓库自带 `qoder_signin.py` 可选装（独立计划任务）。

## 七、边界

- 不模拟客户端点击、不操作用户账号之外的身份、不代注册第三方平台账号。
- 凭据刷新只能由用户先在客户端登录对应账号，再执行 bind。
- 脚本失效（腾讯改版）时：到上游仓库拉新版本，或回退到「提醒 + 本地记账」模式（`scripts/checkin.py` 兜底流程）。

## 八、兜底记账（脚本失效时用）

```bash
python3 scripts/checkin.py mark      # 记今天已签
python3 scripts/checkin.py status    # 出状态（连签、漏签、下一档奖励）
python3 scripts/checkin.py report    # 本月损失折算
python3 scripts/checkin.py miss      # 记昨天断签
python3 scripts/checkin.py card      # 用掉一张补登卡
```
