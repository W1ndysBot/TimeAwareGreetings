# script/TimeAwareGreetings/main.py

import logging
import os
import sys
from datetime import datetime
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
        "还没到点，滚去睡觉。",
        "新的一天，加油！",
    ],
    "noon": [
        "中午好，记得吃饭哦！",
        "午休时间到了，休息一下吧！",
        "别忘了补充能量，中午好～",
    ],
    "evening": [
        "晚安，做个好梦！",
        "夜深了，早点休息哦～",
        "别熬夜了，晚安～",
    ],
}

# 匹配关键词库
keywords = {
    "morning": ["早安", "早上好", "早"],
    "noon": ["中午好", "午安"],
    "evening": ["晚安", "晚上好"],
}


def get_time_period():
    """根据当前时间返回时段（早、中、晚）"""
    current_hour = datetime.now().hour
    if 5 <= current_hour < 11:
        return "morning"
    elif 11 <= current_hour < 17:
        return "noon"
    elif 17 <= current_hour <= 23 or 0 <= current_hour < 5:
        return "evening"


def match_keywords(input_text):
    """匹配用户输入的内容所属的时段"""
    for time_period, word_list in keywords.items():
        if any(word in input_text.lower() for word in word_list):
            return time_period
    return None


def get_random_greeting(time_period):
    """随机返回指定时段的问候语"""
    return random.choice(greetings[time_period])


def respond_to_user(input_text):
    """根据用户输入返回对应的问候"""
    time_period = get_time_period()
    if time_period:
        print(f"匹配到时段：{time_period}")
        return get_random_greeting(time_period)
    return None


# 查看功能开关状态
def load_function_status(group_id):
    return load_switch(group_id, "TimeAwareGreetings")


# 保存功能开关状态
def save_function_status(group_id, status):
    save_switch(group_id, "TimeAwareGreetings", status)


# 群消息处理函数
async def handle_TimeAwareGreetings_group_message(websocket, msg):
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        user_id = str(msg.get("user_id"))
        group_id = str(msg.get("group_id"))
        raw_message = str(msg.get("raw_message"))
        role = str(msg.get("sender", {}).get("role"))
        message_id = str(msg.get("message_id"))

        # 获取当前时段
        time_period = get_time_period(raw_message)


        if time_period:
            if raw_message in keywords[time_period]:
                reply = respond_to_user(raw_message)
                if reply:
                    reply = f"[CQ:reply,id={message_id}]{reply}"
                    await send_group_msg(websocket, group_id, reply)

    except Exception as e:
        logging.error(f"处理TimeAwareGreetings群消息失败: {e}")
        return
