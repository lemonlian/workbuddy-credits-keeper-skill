<div align="center">

# 🎯 workbuddy-credits-keeper-skill

**WorkBuddy 积分管家技能包：多账号每日自动签到 + 成长中心全流程领取 + 积分活动全景地图**

给 WorkBuddy 用户分享安装 · 基于 [88lin/workbuddy-auto-signin](https://github.com/88lin/workbuddy-auto-signin) 开源脚本 · MIT 协议

</div>

---

## 这是什么（30 秒）

- **是什么**：一个 WorkBuddy（腾讯 AI 办公助手）的**智能体技能包**。装进 WorkBuddy 后，你的 AI 助手会按一套成熟方法帮你运维积分：每日自动签到、自动领成长中心的任务/盲盒/旅行/抽奖奖励、签到失败主动诊断、凭据过期带你刷新。
- **给谁用**：用 WorkBuddy、不想每天手动点「Buddy 加油站」领积分的人，尤其是有多账号的人。
- **解决什么**：忘签到断连签、任务领了忘点奖励、Buddy 旅行礼物压到第二天过期、多账号来回切换登录。

**每日能自动拿到的**：签到 100 分 + 连登档位奖励 + 任务奖 + 旅行礼物 10~20 分 + 盲盒 + 抽奖，两个账号各一份。

## 来源与依赖（这就是它来自哪里）

| 组件 | 来源 | 说明 |
|---|---|---|
| 自动签到脚本 | **https://github.com/88lin/workbuddy-auto-signin** | 干活的引擎，MIT，腾讯改版后的修复都在这个仓库发布，建议 Star |
| 本技能包 | 本仓库 | 积分活动全景地图 + 运维方法 + 兜底记账，包装层 |

本技能包**不包含也不修改**上游脚本，只指导安装与运维；接口失效时请到上游仓库更新。

## 安装（macOS，照抄即可）

### 第 1 步：装自动签到脚本

```bash
cd ~
git clone https://github.com/88lin/workbuddy-auto-signin.git
```

### 第 2 步：绑定账号（多账号逐个绑）

1. WorkBuddy 客户端登录**第一个**微信账号，登进去停住
2. 绑定：
   ```bash
   cd ~/workbuddy-auto-signin && python3 bind_one.py 主号
   ```
3. 客户端退出登录 → 换**第二个**微信扫码登录 → 再绑：
   ```bash
   cd ~/workbuddy-auto-signin && python3 bind_one.py 第二号
   ```
4. 绑完回到常用账号。查看已绑账号：
   ```bash
   python3 ~/workbuddy-auto-signin/signin.py accounts
   ```

### 第 3 步：装定时任务（每天自动跑）

创建 `~/Library/LaunchAgents/workbuddy-auto-signin.plist`（把 `<你的用户名>` 换掉）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
    <key>Label</key><string>workbuddy-auto-signin</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/<你的用户名>/workbuddy-auto-signin/signin.py</string>
        <string>auto</string>
    </array>
    <key>WorkingDirectory</key><string>/Users/<你的用户名>/workbuddy-auto-signin</string>
    <key>StartCalendarInterval</key>
    <array><dict><key>Hour</key><integer>0</integer><key>Minute</key><integer>5</integer></dict></array>
    <key>StartInterval</key><integer>14400</integer>
    <key>RunAtLoad</key><true/>
    <key>StandardOutPath</key><string>/tmp/workbuddy-auto-signin.out</string>
    <key>StandardErrorPath</key><string>/tmp/workbuddy-auto-signin.err</string>
</dict></plist>
```

加载并立即试跑：

```bash
launchctl load ~/Library/LaunchAgents/workbuddy-auto-signin.plist
cat /tmp/workbuddy-auto-signin.out
```

效果：每天 00:05 首跑 + 每 4 小时轮询一次补漏（接住 Buddy 旅行返程、盲盒、抽奖），关机错过开机补跑。

### 第 4 步：装技能包进 WorkBuddy（可选，强烈建议）

把本仓库 `SKILL.md` 复制到 WorkBuddy 技能目录：

```bash
mkdir -p ~/.workbuddy/skills/buddy-checkin-keeper
git clone https://github.com/lemonlian/workbuddy-credits-keeper-skill.git /tmp/ck
cp /tmp/ck/SKILL.md ~/.workbuddy/skills/buddy-checkin-keeper/SKILL.md
cp /tmp/ck/scripts/checkin.py ~/.workbuddy/skills/buddy-checkin-keeper/scripts/
```

装好后对 WorkBuddy 说「**签到状态**」验证，它会用服务端数据汇报连签天数和累计积分。

### Windows 用户

上游仓库提供一键安装脚本（任务计划程序模式），直接看：
https://github.com/88lin/workbuddy-auto-signin#--每日定时自动化

## 不用问作者：常见问题自查

| 现象 | 原因 | 处理 |
|---|---|---|
| 签到突然失败 | 凭据过期 / 腾讯改版 | 客户端登录该号 → `python3 bind_one.py <账号名>` 刷新；仍失败去上游仓库看新版本 |
| 想看绑了几个号 | - | `python3 ~/workbuddy-auto-signin/signin.py accounts`（含凭据到期时间） |
| 提示「该账号已绑定」 | 当前客户端登的是已绑账号 | 先换号再 bind |
| 绑定命令没反应 | macOS 安全拦截 | 右键 → 打开 → 允许 |
| 机器人不认识技能 | SKILL.md 没放对位置 | 确认在 `~/.workbuddy/skills/buddy-checkin-keeper/SKILL.md` |
| 想查今天领了多少 | - | `python3 ~/workbuddy-auto-signin/signin.py` 看输出的 `report` 字段 |
| 换电脑 | - | clone 本仓库 + 上游仓库，重走第 1~4 步；旧机器 `accounts/` 不要带走同步 |

## 安全与风险（必读）

1. `accounts/` 目录存的是**登录凭据副本，等同密码**。不要放进 iCloud / 网盘 / 任何自动同步目录。
2. 脚本通过逆向桌面端接口实现，官方规则把「利用脚本刷取活跃或奖励」列为禁止情形，存在积分追回或账号处理风险。**是否使用自行判断**。
3. 上游脚本不含任何内置密钥，只读取你本机的登录凭据；源码可审计（单文件 `signin.py`）。
4. 使用前建议备份 `~/.workbuddy/skills` 与 WorkBuddy 资料库。

## 版本与回退

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0.0 | 2026-11-16 | 首版：通用化 SKILL.md（多账号地图 + 人工活动清单 + 兜底记账）+ macOS launchd 安装模板 |

回退命令：

```bash
git tag                  # 看所有版本
git checkout v1.0.0 -- SKILL.md   # 只回退单个文件
git checkout v1.0.0               # 整仓临时回看
```

## 协议

MIT。上游脚本版权归 88lin 所有，见其仓库 LICENSE。
