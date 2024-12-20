import random, threading
from modules.get_plan_id import get_plan_id
from modules.get_login_token import get_token
from modules.crypto_aes import create_sign
from modules.check_sign_in import check_sign
from modules.save_user_info import save_user_info
from datetime import datetime, timezone, timedelta
from modules.load_config import dprint


# 操作地时区设置
shanghai_tz = timezone(timedelta(hours=8))
gmt_time = datetime.now(shanghai_tz)
now = datetime.now(shanghai_tz)
# 以17时为分界线, 判断打卡是上班还是下班
is_start = now.hour < 17
# 中文映射字典, 用于控制台输出罢了
sign_type_mapping = {"START": "上班", "END": "下班"}
# 收集所有线程签到结果
global_sign_results = []
# 覆盖打卡，设置为True会导致每次运行都不检查签到历史从而重复签到，用于测试环境调试
RepeatCheckIn = True


# 处理单个用户的签到流程, 包括获取登录令牌、签到计划 ID、检查是否已签到以及执行签到操作。
def send_sign_in(user_info, timeout):
    try:
        timer = threading.Timer(timeout, lambda: None)
        timer.start()
        userInfo = get_token(user_info)
        phone = user_info["phone"]
        remark = user_info.get("remark", "")

        user_info_prefix = f"[{remark}/{phone}]"

        # ❗开发环境输出, 包含敏感内容, 打印登录响应内容
        # dprint(f"{user_info_prefix} 登录响应: {userInfo}\n")

        # 随机化经纬度
        if user_info.get("randomLocation", False):
            user_info["latitude"] = user_info["latitude"][0:-1] + str(
                random.randint(0, 9)
            )
            user_info["longitude"] = user_info["longitude"][0:-1] + str(
                random.randint(0, 9)
            )

        if not user_info:
            global_sign_results.append(
                f"{user_info_prefix}打卡失败, 错误原因: {userInfo['msg']}"
            )
            return
        userId = userInfo["userId"]
        token = userInfo["token"]
        sign_info = create_sign(userId + "student")
        planId = get_plan_id(user_info, token, sign_info)
        # 使用上海时间判断是上班还是下班
        signType = "START" if is_start else "END"
        # 检查是否已经打过卡，避免重复打卡, 不需要检查的话可以注释掉整个if块
        if check_sign(token, signType) and not RepeatCheckIn:
            dprint(f"{user_info_prefix}")
            print(f"已打过{sign_type_mapping[signType]}卡, 任务跳过。\n")
            return
        dprint(f"{user_info_prefix}", end="")
        print(f"准备{sign_type_mapping[signType]}打卡\n")
        # 发送请求
        try:
            signResp, msg, full_response = save_user_info(
                user_info,
                userId,
                token,
                planId,
                user_info["province"],
                user_info["address"],
                signType=signType,
                latitude=user_info["latitude"],
                longitude=user_info["longitude"],
            )
        except Exception as e:
            error_message = f"{user_info_prefix}打卡失败, 错误原因: {str(e)}"
            dprint(error_message)
            global_sign_results.append(error_message)
            return
        # 打印完整的打卡响应内容
        dprint(f"{user_info_prefix}打卡响应: {full_response}\n")
        # 构建推送消息
        pushSignType = "上班" if signType == "START" else "下班"
        pushSignIsOK = "成功！" if signResp else "失败！"
        signStatus = "打卡"
        hourNow = gmt_time.hour
        if hourNow == 11 or hourNow == 23:
            signStatus = "补签"
        global_sign_results.append(
            f"{user_info_prefix}工学云{pushSignType}{signStatus}{pushSignIsOK}\n"
        )
    finally:
        timer.cancel()
