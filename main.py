# script/TimeAwareGreetings/main.py

import logging
import os
import sys
import random

# 添加项目根目录到sys.path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.config import owner_id
from app.api import *
from app.switch import load_switch, save_switch

# 数据存储路径，实际开发时，请将TimeAwareGreetings替换为具体的数据存放路径
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "TimeAwareGreetings",
)

# 问候语库
greetings = {
    "morning": [
        "早安～",
        "早什么早，去睡觉！",
        "新的一天，加油！",
        "早上好，今天又是元气满满的一天！",
        "太阳都晒屁股了，快起床吧～",
        "新的一天，新的希望，新的挑战，早安！",
        "你知道今天早上的第一件事该做什么吗？是起床！",
    ],
    "noon": [
        "中午好，记得吃饭哦！",
        "午休时间到了，休息一下吧！",
        "别忘了补充能量，中午好～",
        "午安，充实的午后，别忘了补充维C！",
        "又到了午餐时间，是不是开始想念美食了？",
        "中午好，别让工作占据了你吃饭的时间～",
        "中午要吃饱，下午才有力气打怪！",
        "今天的午餐计划是什么？我猜你已经迫不及待了！",
    ],
    "evening": [
        "晚安，做个好梦！",
        "夜深了，早点休息哦～",
        "别熬夜了，晚安～",
        "深夜时光，祝你有个甜美的梦！",
        "夜晚安静了，只有星星陪着你，晚安！",
        "时间不早了，给自己放个好梦吧～",
        "又是熬夜的一天，晚安，早点休息！",
        "如果这一天很累，就让晚安成为你最甜的祝福。",
        "晚安，愿你早日入梦，梦中有我！",
    ],
    "general": [
        "嘿，今天怎么样？",
        "你好呀！有个好心情吗？",
        "最近过得怎么样？生活愉快吗？",
        "嗨！有没有想我呀？",
        "祝你今天一切顺利，心情愉快！",
        "你今天的状态怎么样？别太累哦～",
        "今天的你，笑容满面吗？如果没有，试试笑一笑！",
        "无论今天发生什么，都不要忘了保持微笑～",
    ],
}


keywords = {
    "morning": ["早安", "早上好", "早", "起床", "起床了"],
    "noon": ["中午好", "午安", "午休", "午休了"],
    "evening": ["晚安", "晚上好", "睡觉", "休息", "休息了", "睡觉了"],
}


def get_time_period_from_keywords(user_message):
    """根据用户输入的关键词匹配到对应的时段"""
    for time_period, keyword_list in keywords.items():
        if any(keyword == user_message.lower() for keyword in keyword_list):
            return time_period
    return None


def get_random_greeting_for_time_period(time_period):
    """根据时段返回随机的问候语"""
    return random.choice(greetings[time_period])


async def handle_TimeAwareGreetings_group_message(websocket, message):
    """处理群组消息并根据关键词回复问候语"""
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        user_message = str(message.get("raw_message"))
        message_id = str(message.get("message_id"))
        group_id = str(message.get("group_id"))

        # 匹配发言中的关键词并确定时段
        time_period = get_time_period_from_keywords(user_message)
        if time_period:
            greeting_reply = get_random_greeting_for_time_period(time_period)
            reply_message = f"[CQ:reply,id={message_id}]{greeting_reply}"
            await send_group_msg(websocket, group_id, reply_message)

    except Exception as e:
        logging.error(f"处理群消息失败: {e}")
        return
