import streamlit as st
from datetime import datetime
from datetime import time

import pytz
timezone = pytz.timezone('Asia/Shanghai')

st.set_page_config(page_title='Fruit Time Calculator', page_icon="🍎", layout='wide', initial_sidebar_state='auto')

def hour2min(hour, min):
    return hour * 60 + min

def min2hour(min):
    return int(min // 60), int(min % 60)

def get_fruit_time(fruit_time):
    now = datetime.now().hour * 60 + datetime.now().minute
    fruit_time_min = now + fruit_time
    fruit_hour, fruit_min = min2hour(fruit_time_min)
    fruit_hour %= 24
    return fruit_hour, fruit_min

def fresh_continue_from_type(type=32):
    if type == 6:
        water_fresh_continue_time = (2, 0)
        fruit_input = (3, 0)
        water_now_continue_input = (2, 0)
    elif type == 12:
        water_fresh_continue_time = (4, 0)
        fruit_input = (6, 0)
        water_now_continue_input = (4, 0)
    elif type == 16:
        water_fresh_continue_time = (5, 20)
        fruit_input = (8, 0)
        water_now_continue_input = (5, 20)
    elif type == 32:
        water_fresh_continue_time = (10, 40)
        fruit_input = (16, 0)
        water_now_continue_input = (10, 40)
        return water_fresh_continue_time, fruit_input, water_now_continue_input
    else:
        raise Exception("未知的水果类型")

# Streamlit 应用开始
st.title('🍎 Fruit Time Calculator 🍎')
st.markdown("""
    <div style="background-color:#464e59;padding:8px;border-radius:7px">
        <h4 style="color:white;text-align:center;">Author: 春饼侠</h4>
    </div>
    """, unsafe_allow_html=True)
st.markdown("第一个填水果类型，第二个是水果成熟剩余时间，第三个是水分还能维持时间（需要游戏内点击蓝色小问号查看)")
st.markdown("注意事项：时间仅包含小时和分钟，不包含天数/秒数，请根据实际情况填0")
# 创建一个选择器来选择水果类型
fruit_type = st.selectbox('🍇 Select fruit type', [32, 16, 12, 6])
st.warning(f"Selected crop type: {fruit_type} hours")

# 计算水果的新鲜持续时间, 预设的时间
WATER_FRESH_CONTINUE, fruit_input, water_now_continue_input = fresh_continue_from_type(
    fruit_type)

# 创建小时和分钟的下拉菜单选项
hours = list(range(24))
minutes = list(range(60))

fruit_input_hour = st.selectbox('🍉 Fruit hour', hours, index=fruit_input[0])
fruit_input_min = st.selectbox('🍉 Fruit minute', minutes, index=fruit_input[1])
fruit_showed_time = (fruit_input_hour, fruit_input_min)
st.warning(f"Display maturity time: {fruit_showed_time[0]} hours {fruit_showed_time[1]} minutes")

water_now_continue_hour = st.selectbox('💧 Water continue hour', hours, index=water_now_continue_input[0])
water_now_continue_min = st.selectbox('💧 Water continue minute', minutes, index=water_now_continue_input[1])
water_now_contiue = (water_now_continue_hour, water_now_continue_min)
st.warning(f'Water can still be maintained (click the question mark to view): {water_now_contiue[0]} hours {water_now_contiue[1]} minutes')

# 计算水果的成熟时间
fresh_water_passed_time = hour2min(*WATER_FRESH_CONTINUE) - hour2min(*water_now_contiue)
fresh_water_fruit_time = hour2min(*fruit_showed_time) + fresh_water_passed_time
fastest_water_fruit_needed = fresh_water_fruit_time / 5 * 4
fastest_now_fruit_needed = fastest_water_fruit_needed - fresh_water_passed_time
fruit_hour = get_fruit_time(fastest_now_fruit_needed)

# 显示结果
st.success(f"🌱 Predicts: The fastest maturity time is {fruit_hour[0]}:{fruit_hour[1]}")

if fresh_water_passed_time > fastest_water_fruit_needed:
    st.success("🌱 浇水就能收: The fruit has matured, please harvest it in time")