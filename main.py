import logging
import os
import sys
import random
from datetime import datetime

# 添加项目根目录到sys.path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.config import owner_id
from app.api import *
from app.switch import load_switch, save_switch

# 数据存储路径，实际开发时，请将TimeAwareGreetings替换为具体的数据位置
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
        "清晨的阳光洒在你脸上，带着希望醒来吧！",
        "一日之计在于晨，祝你今天万事顺利！",
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
        "午间小憩一下，下午会更有精神哦！",
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
        "夜幕降临，静谧时刻，晚安～",
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
        "你好！今天的天气如何？希望你心情明媚如阳光！",
    ],
}

# 不合时宜的提示语库
misfit_greetings = {
    "morning": [
        "起什么起，滚去睡觉！",
        "现在还不到早起的时候哦，继续睡吧！",
        "清晨时分，还是被窝最暖，回去睡觉吧～",
    ],
    "noon": [
        "太阳都晒屁股了，这才起床啊！",
        "中午了才说早安，你是猫头鹰吗？",
        "现在是午餐时间，早餐是不是省了？",
    ],
    "evening": [
        "睡什么睡，还不到点！",
        "现在就睡？难道不看星星吗？",
        "天还没黑透呢，早睡会错过美好的夜晚哦！",
    ],
}


# 时间段分类
def get_current_time_period():
    """根据当前时间返回对应的时间段"""
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "noon"
    elif 18 <= current_hour < 24:
        return "evening"
    else:
        return "night"  # 夜晚特别处理


# 根据关键词判断时段
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


def get_random_misfit_greeting_for_time_period(time_period):
    """根据时段返回随机的不合时宜提示"""
    return random.choice(misfit_greetings[time_period])


async def handle_TimeAwareGreetings_group_message(websocket, message):
    """处理群组消息并根据关键词回复问候语"""
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        user_message = str(message.get("raw_message"))
        message_id = str(message.get("message_id"))
        group_id = str(message.get("group_id"))

        # 匹配发言中的关键词并确定时段
        user_time_period = get_time_period_from_keywords(user_message)
        current_time_period = get_current_time_period()

        if user_time_period:
            if user_time_period == current_time_period:
                # 时间匹配，发送正常问候语
                greeting_reply = get_random_greeting_for_time_period(user_time_period)
            else:
                # 时间不匹配，发送不合时宜的提示
                greeting_reply = get_random_misfit_greeting_for_time_period(
                    user_time_period
                )

            reply_message = f"[CQ:reply,id={message_id}]{greeting_reply}"
            await send_group_msg(websocket, group_id, reply_message)

    except Exception as e:
        logging.error(f"处理群消息失败: {e}")
        return


# 统一事件处理入口
async def handle_events(websocket, msg):
    """统一事件处理入口"""
    post_type = msg.get("post_type", "response")  # 添加默认值
    try:
        # 处理回调事件
        if msg.get("status") == "ok":
            return

        post_type = msg.get("post_type")

        # 处理元事件
        if post_type == "meta_event":
            return

        # 处理消息事件
        elif post_type == "message":
            message_type = msg.get("message_type")
            if message_type == "group":
                # 调用TimeAwareGreetings的群组消息处理函数
                await handle_TimeAwareGreetings_group_message(websocket, msg)
            elif message_type == "private":
                return

        # 处理通知事件
        elif post_type == "notice":
            return

        # 处理请求事件
        elif post_type == "request":
            return

    except Exception as e:
        error_type = {
            "message": "消息",
            "notice": "通知",
            "request": "请求",
            "meta_event": "元事件",
        }.get(post_type, "未知")

        logging.error(f"处理TimeAwareGreetings{error_type}事件失败: {e}")

        # 发送错误提示
        if post_type == "message":
            message_type = msg.get("message_type")
            if message_type == "group":
                await send_group_msg(
                    websocket,
                    msg.get("group_id"),
                    f"处理TimeAwareGreetings{error_type}事件失败，错误信息：{str(e)}",
                )
            elif message_type == "private":
                await send_private_msg(
                    websocket,
                    msg.get("user_id"),
                    f"处理TimeAwareGreetings{error_type}事件失败，错误信息：{str(e)}",
                )
