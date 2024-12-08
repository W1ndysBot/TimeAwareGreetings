from datetime import datetime
import random

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
    return "听不懂你在说什么～"


# 示例交互
if __name__ == "__main__":
    user_input = input("用户：")
    reply = respond_to_user(user_input)
    print(f"机器人：{reply}")
