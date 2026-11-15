#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buddy 加油站签到记账（本地、零依赖、零 token）

用法:
  python3 checkin.py mark      # 记今天已签
  python3 checkin.py status    # 查看状态
  python3 checkin.py report    # 本月损失折算
  python3 checkin.py miss      # 记昨天断签
  python3 checkin.py card      # 用掉一张补登卡
"""
import json
import os
import sys
from datetime import date, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data", "checkin.json")

DAILY = 100          # 每日签到积分
CYCLE_BONUS = 1000   # 连签 7 天额外奖励
POINT_YUAN = 0.05    # 按加量包 50 元 / 1000 积分折算


def load():
    if not os.path.exists(DATA):
        return {"last_checkin": None, "streak": 0, "makeup_cards": 4,
                "history": {}, "missed_this_month": 0, "month": None}
    with open(DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def save(d):
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def today():
    return date.today().isoformat()


def roll_month(d):
    m = date.today().strftime("%Y-%m")
    if d.get("month") != m:
        d["month"] = m
        d["missed_this_month"] = 0
    return d


def mark(d):
    d = roll_month(d)
    t = today()
    if d.get("last_checkin") == t:
        return "今天已经记过了，连签第 %d 天。" % d["streak"]
    y = (date.today() - timedelta(days=1)).isoformat()
    d["streak"] = d["streak"] + 1 if d.get("last_checkin") == y else 1
    d["last_checkin"] = t
    d["history"][t] = True
    save(d)
    return status_line(d)


def miss(d):
    d = roll_month(d)
    y = (date.today() - timedelta(days=1)).isoformat()
    d["history"][y] = False
    d["missed_this_month"] = d.get("missed_this_month", 0) + 1
    d["streak"] = 0
    save(d)
    return "已记昨天（%s）断签，连签清零。本月已漏 %d 次。" % (y, d["missed_this_month"])


def card(d):
    if d.get("makeup_cards", 0) <= 0:
        return "补登卡已用完（上限 4 张）。这次只能认了，连签从头开始。"
    d["makeup_cards"] -= 1
    save(d)
    return "已用 1 张补登卡，剩余 %d 张。建议留给真有事的日子。" % d["makeup_cards"]


def status_line(d):
    t = date.today()
    st = d.get("streak", 0)
    to_bonus = 7 if st % 7 == 0 else 7 - st % 7
    lines = []
    lines.append("连签：第 %d 天" % st)
    if st % 7 == 0 and st > 0:
        lines.append("今天正好是第 %d 天，额外 1000 分到手。" % st)
    else:
        lines.append("距 7 天档奖励还差 %d 天（第 %d 天可拿额外 1000 分）。" % (to_bonus, st + to_bonus))
    lines.append("补登卡：%d 张" % d.get("makeup_cards", 0))
    lines.append("本月漏签：%d 次" % d.get("missed_this_month", 0))
    if d.get("last_checkin") != t.isoformat():
        lines.append("⚠️ 今天还没打卡。")
    return " ｜ ".join(lines)


def report(d):
    d = roll_month(d)
    missed = d.get("missed_this_month", 0)
    lost = missed * DAILY * POINT_YUAN
    streak_now = d.get("streak", 0)
    cycles = streak_now // 7
    print("本月漏签 %d 次，直接损失约 %.0f 元（按 100 分 = 5 元折算）。" % (missed, lost))
    if missed:
        print("若因此断了连签，还会丢掉 7 天档的 1000 分（约 50 元）。")
    print("当前连签 %d 天，已拿满 %d 轮 7 天奖励。" % (streak_now, cycles))
    if streak_now and streak_now % 7:
        print("还差 %d 天拿下一轮 1000 分。" % (7 - streak_now % 7))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    d = load()
    if cmd == "mark":
        print(mark(d))
    elif cmd == "miss":
        print(miss(d))
    elif cmd == "card":
        print(card(d))
    elif cmd == "report":
        report(d)
    elif cmd == "status":
        print(status_line(d))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
