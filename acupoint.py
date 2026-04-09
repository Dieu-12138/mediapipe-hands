import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import mediapipe as mp
import numpy as np
import time
from datetime import datetime, timedelta  # 用于显示时钟
from count import *
from ancor import *

# 定义主题颜色
COLORS = {
    'primary': '#FFB6C1',  # 柔和的粉色
    'secondary': '#E6E6FA',  # 淡紫色
    'accent': '#98FB98',  # 淡绿色
    'text': '#4A4A4A',  # 深灰色文字
    'background': '#FFF0F5',  # 淡粉色背景
    'highlight': '#FF69B4',  # 亮粉色
    'dropdown_bg': '#FFFFFF',  # 白色背景
    'dropdown_border': '#E6E6FA',  # 下拉框边框颜色
    'status_text': '#666666',  # 状态文字颜色
    'glass_bg': '#F8F8FF',  # 毛玻璃效果背景色
    'hover_bg': '#FFE4E1',  # 悬停背景色
    'prompt_text': '#FF69B4',  # 提示文字颜色
    'tab_border': '#FFB6C1'  # 标签页边框颜色
}

# 创建圆角矩形
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# 创建主窗口
root = tk.Tk()
root.title("明穴智疗")
root.configure(bg=COLORS['background'])

# 创建变量
selected_var = tk.StringVar(root)

# 设置窗口大小和位置
window_width = 1200
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 创建自定义样式
style = ttk.Style()
style.configure('Custom.TNotebook', 
                background=COLORS['background'],
                borderwidth=0)
style.configure('Custom.TNotebook.Tab', 
                padding=[20, 10],
                font=('幼圆', 12),
                background=COLORS['background'],
                foreground=COLORS['text'],
                borderwidth=1,
                relief='flat')
style.map('Custom.TNotebook.Tab',
          background=[('selected', COLORS['primary'])],
          foreground=[('selected', COLORS['text'])],
          borderwidth=[('selected', 1)],
          relief=[('selected', 'flat')])
style.configure('Custom.TFrame', 
                background=COLORS['background'])
style.configure('Custom.TCombobox', 
                fieldbackground=COLORS['glass_bg'],
                background=COLORS['glass_bg'],
                foreground=COLORS['text'],
                arrowcolor=COLORS['text'],
                borderwidth=0,
                relief='flat',
                font=('幼圆', 12))
style.map('Custom.TCombobox',
          fieldbackground=[('readonly', COLORS['glass_bg'])],
          selectbackground=[('readonly', COLORS['hover_bg'])],
          selectforeground=[('readonly', COLORS['text'])])
style.configure('Custom.TLabelframe', 
                background=COLORS['background'],
                borderwidth=0)
style.configure('Custom.TLabelframe.Label', 
                background=COLORS['background'],
                foreground=COLORS['text'],
                font=('幼圆', 12))

# 创建标题标签
title_font = ('幼圆', 28, 'bold')
title_label = tk.Label(root, 
                      text="明穴智疗 - 您的智能穴位按摩助手",
                      font=title_font,
                      bg=COLORS['background'],
                      fg=COLORS['text'])
title_label.pack(pady=20)

# 创建notebook
notebook = ttk.Notebook(root, style='Custom.TNotebook')
notebook.pack(pady=20, fill='both', expand=True)

# 创建各个页面
symptom_frame = ttk.Frame(notebook, style='Custom.TFrame')
meridian_frame = ttk.Frame(notebook, style='Custom.TFrame')
time_frame = ttk.Frame(notebook, style='Custom.TFrame')

notebook.add(symptom_frame, text="症状按摩舒缓")
notebook.add(meridian_frame, text="经络学习")
notebook.add(time_frame, text="此刻时辰对应之经络")

# 创建症状选择区域
symptom_container = ttk.Frame(symptom_frame, style='Custom.TFrame')
symptom_container.pack(pady=20, padx=40, fill='x')

symptom_label = tk.Label(symptom_container,
                        text="请选择您想要缓解的症状：",
                        font=('幼圆', 16),
                        bg=COLORS['background'],
                        fg=COLORS['text'])
symptom_label.pack(pady=10)

# 创建圆角下拉菜单
dropdown = ttk.Combobox(symptom_container,
                       textvariable=selected_var,
                       style='Custom.TCombobox',
                       font=('幼圆', 14))
dropdown["values"] = (
    "哮喘", "降血压", "牙齿痛", "落枕", "中暑", "中风",
    "经痛", "头痛", "手指麻木", "结膜炎", "昏迷", "心肌炎", "心烦"
)
dropdown.pack(pady=10, fill='x')

# 创建经络选择区域
meridian_container = ttk.Frame(meridian_frame, style='Custom.TFrame')
meridian_container.pack(pady=20, padx=40, fill='x')

meridian_label = tk.Label(meridian_container,
                         text="请选择您想要学习的经络：",
                         font=('幼圆', 16),
                         bg=COLORS['background'],
                         fg=COLORS['text'])
meridian_label.pack(pady=10)

# 创建圆角下拉菜单
meridian_dropdown = ttk.Combobox(meridian_container,
                                textvariable=selected_var,
                                style='Custom.TCombobox',
                                font=('幼圆', 14))
meridian_dropdown["values"] = (
    "手太阴肺经", "手阳明大肠经", "手厥阴心包经",
    "手少阳三焦经", "手少阴心经", "手太阳小肠经"
)
meridian_dropdown.pack(pady=10, fill='x')

# 创建视频显示区域
video_frame = ttk.Frame(symptom_frame, style='Custom.TFrame')
video_frame.pack(pady=0, padx=0, expand=True, fill='both')

# 创建圆角视频容器
video_container = tk.Frame(video_frame,
                         bg=COLORS['background'],  # 统一为主背景色，避免白色横框
                         highlightthickness=0)
video_container.pack(pady=0, padx=0, expand=True, fill='both')

video_label_symptom = tk.Label(video_container, bg=COLORS['background'])
video_label_symptom.pack(pady=0, padx=0, expand=True, fill='both')

video_label_meridian = tk.Label(meridian_frame)
video_label_meridian.pack(pady=0, padx=0, expand=True, fill='both')

# 创建状态提示标签
status_frame = tk.Frame(root,
                       bg=COLORS['background'],
                       highlightthickness=0)
status_frame.pack(pady=10)

status_label = tk.Label(status_frame,
                       text="请将手掌放在摄像头前",
                       font=('幼圆', 14),
                       bg=COLORS['background'],
                       fg=COLORS['status_text'])
status_label.pack()

# 获取当前时辰对应的索引，用于判断现在是什么时辰
def get_current_hour_index():
    current_hour = time.localtime().tm_hour  # 获取当前小时
    # 根据时辰规则计算出时辰索引（2小时为一时辰）
    return (current_hour + 1) // 2 % 12
# 自订的时钟数字和时辰对应的布局
numbers = ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23']  # 12个小时对应的数字
chinese_hours = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']  # 中国时辰名称
meridians = ['胆经', '肝经', '肺经', '大肠经', '胃经', '脾经', '心经', '小肠经', '膀胱经', '肾经', '心包经', '三焦经']  # 对应的经络

# 创建显示模拟时钟的函数
def draw_clock():
    w = 600  # 设置时钟图像的宽度
    h = 600  # 设置时钟图像的高度
    # 创建一个白色背景的图像（大小可以根据窗口进行调整）
    clock_img = Image.new('RGB', (w, h), 'white')  # 创建一个白色背景的图像
    draw = ImageDraw.Draw(clock_img)  # 准备画图像

    font_path = "simsun.ttc"  # 字体文件路径，根据系统调整
    font = ImageFont.truetype(font_path, 16, encoding="utf-8")  # 设置字体和大小

    current_hour_index = get_current_hour_index()  # 获取当前的时辰索引
    center = (w // 2, h // 2)  # 定义时钟的中心点
    radius = 200  # 设定时钟的半径
    # 画一个圆形来表示时钟的外围
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline='black', width=4)

    # 根据12个时辰绘制数字、时辰和经络
    for i in range(12):
        angle = math.radians(30 * i - 75)  # 计算每个数字的角度位置
        num_x = center[0] + radius * 0.85 * math.cos(angle)  # 计算数字的X坐标
        num_y = center[1] + radius * 0.85 * math.sin(angle)  # 计算数字的Y坐标

        angle = math.radians(30 * i - 90)  # 调整角度以便绘制时辰和经络名称
        hour_x = center[0] + radius * 0.65 * math.cos(angle)  # 计算时辰的X坐标
        hour_y = center[1] + radius * 0.65 * math.sin(angle)  # 计算时辰的Y坐标
        meridiansr_x = center[0] - 20 + radius * 1.2 * math.cos(angle)  # 计算经络名称的X坐标
        meridiansr_y = center[1] + radius * 1.2 * math.sin(angle)  # 计算经络名称的Y坐标

        draw.text((num_x - 10, num_y - 10), numbers[i], font=font, fill='black')  # 绘制对应的数字

        hour_color = 'blue' if i == current_hour_index else 'black'  # 当前时辰显示为蓝色，其它为黑色
        draw.text((hour_x - 10, hour_y - 10), chinese_hours[i], font=font, fill=hour_color)  # 绘制对应的时辰
        draw.text((meridiansr_x - 10, meridiansr_y - 10), meridians[i], font=font, fill=hour_color)  # 绘制对应的经络名称

    return clock_img


# 更新并显示时钟
def update_clock():
    clock_img = draw_clock()
    imgtk = ImageTk.PhotoImage(image=clock_img)
    time_label.imgtk = imgtk  # 需要保存引用，防止图像被垃圾回收
    time_label.config(image=imgtk)
    time_label.after(1000, update_clock)  # 每秒更新一次


# 在 "此刻时辰" 页面显示模拟时钟
time_label = tk.Label(time_frame)
time_label.pack(pady=20)
update_clock()  # 启动时钟更新

# 打开视频捕获设备
cap = cv2.VideoCapture(0)

# 加载 Mediapipe 手部和姿势模型
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)

# 创建视频显示的标签，分别在症状按摩舒缓和经络学习页面
video_label_symptom = tk.Label(symptom_frame)
video_label_symptom.pack()

video_label_meridian = tk.Label(meridian_frame)
video_label_meridian.pack()


# 更新视频帧
def update_frame():
    ret, frame = cap.read()  # 读取视频帧
    data_list = []
    hand_orientations = {}
    hand_landmarks_dict = {}
    global timer_started, start_time, massage_complete  # 告诉 Python 这些是全域变量
    # 定义加大的阀值，比如 10
    massage_threshold = 13  # 按摩范围
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换为 RGB 颜色格式
        frame = cv2.flip(frame, 1)  # 水平翻转图像
        imgHeight = frame.shape[0]
        imgWidth = frame.shape[1]
        x = imgWidth // 2.5
        y = imgHeight // 2.5

        # 调用 Mediapipe 检测手部关键点
        hand_results = hands.process(frame)

        if not hand_results.multi_hand_landmarks:
            # 如果没有检测到手部，显示提示
            frame = cv2ImgAddText(frame, "请将手掌放在摄像头前", imgWidth // 2.5, imgHeight // 2.5, COLORS['prompt_text'], 30)

        else:
            for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                hand_label = handedness.classification[0].label  # 'Left' or 'Right'
                hand_landmarks_dict[hand_label] = hand_landmarks

                finger_points = []  # 记录手指节点坐标的串列
                for lm in hand_landmarks.landmark:
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)
                    finger_points.append((xPos, yPos))  # 将每个节点的坐标加入列表

                # 如果 finger_points 有资料，计算手指角度
                if finger_points:
                    finger_angle = hand_angle(finger_points)  # 计算手指的角度，返回5个数值的列表
                    hand_position_text = hand_pos(finger_angle)  # 根据手指角度判断手势
                    # cv2.putText(frame, hand_position_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)  # 显示手势判断结果

                # 显示节点8（食指指尖）
                xPos_8 = int(hand_landmarks.landmark[8].x * imgWidth)
                yPos_8 = int(hand_landmarks.landmark[8].y * imgHeight)
                # cv2.circle(frame, (xPos_8, yPos_8), 5, (255, 255, 255), -1)  # 显示白色圆圈（被注解掉）

                data_list.clear()
                for i, lm in enumerate(hand_landmarks.landmark):
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)
                    cv2.putText(frame, str(i), (xPos - 25, yPos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                (300, 255, 400))  # 标记数值
                    data_list.append((i, xPos, yPos))  # 储存每个节点的编号与坐标

                # 提取部分关键点的坐标
                cx0, cy0 = data_list[0][1], data_list[0][2]
                cx1, cy1 = data_list[1][1], data_list[1][2]
                cx2, cy2 = data_list[2][1], data_list[2][2]
                cx3, cy3 = data_list[3][1], data_list[3][2]
                cx4, cy4 = data_list[4][1], data_list[4][2]
                cx5, cy5 = data_list[5][1], data_list[5][2]
                cx6, cy6 = data_list[6][1], data_list[6][2]
                cx7, cy7 = data_list[7][1], data_list[7][2]
                cx8, cy8 = data_list[8][1], data_list[8][2]
                cx9, cy9 = data_list[9][1], data_list[9][2]
                cx12, cy12 = data_list[12][1], data_list[12][2]
                cx13, cy13 = data_list[13][1], data_list[13][2]
                cx14, cy14 = data_list[14][1], data_list[14][2]
                cx15, cy15 = data_list[15][1], data_list[15][2]
                cx16, cy16 = data_list[16][1], data_list[16][2]
                cx17, cy17 = data_list[17][1], data_list[17][2]
                cx18, cy18 = data_list[18][1], data_list[18][2]
                cx19, cy19 = data_list[19][1], data_list[19][2]
                cx20, cy20 = data_list[20][1], data_list[20][2]
                cx7_8 = int((cx7 + cx8) / 2)
                cy7_8 = int((cy7 + cy8) / 2)
                cx15_16 = int((cx15 + cx16) / 2)
                cy15_16 = int((cy15 + cy16) / 2)
                cx19_20 = int((cx19 + cx20) / 2)
                cy19_20 = int((cy19 + cy20) / 2)

                # cv2.line(frame, (cx5, cy5), (cx17, cy17), (0, 0, 255), 2)
                direction_vector = np.array([1, 0])  # 水平方向矢量
                l_vector = np.array([0, 1])  # 垂直方向矢量
                # 定义线段的长度（例如 100 像素）
                line_length = -200
                linel_length = -200
                point = (cx17, cy17)
                pointl = (cx5, cy5)
                # 计算线段终点
                line_point = point + direction_vector * line_length  # 根据方向矢量计算终点
                line_x = int(line_point[0])
                line_y = int(line_point[1])

                line_pointl = pointl + l_vector * linel_length  # 根据方向矢量计算终点
                linel_x = int(line_pointl[0])
                linel_y = int(line_pointl[1])

                # cv2.line(frame, (cx17, cy17), (line_x, line_y), (255, 0, 0), 2)
                # cv2.line(frame, (cx5, cy5), (linel_x, linel_y), (255, 0, 0), 2)
                # 起点和方向矢量
                direction_vector1 = np.array(direction_vector)  # 第一条线的方向矢量
                direction_vector2 = np.array(l_vector)  # 第二条线的方向矢量

                # 构建线性方程组 Ax = b
                A = np.array([direction_vector1, -direction_vector2]).T  # 方向矢量组成矩阵
                b = np.array(pointl) - np.array(point)  # 起点之间的差

                '''劳宫穴'''
                lgmid_x = int((cx0 + cx5 + cx9) / 3)
                lgmid_y = int((cy0 + cy5 + cy9) / 3)
                '''少府穴 中渚穴'''
                cfmid_x = int((cx0 + cx13 + cx18) / 3)
                cfmid_y = int((cy0 + cy13 + cy18) / 3)
                '''鱼际穴'''
                fishmid_x = (cx1 + cx2) / 2
                fishmid_y = (cy1 + cy2) / 2
                fishmid_x = int((cx1 + fishmid_x) / 2)
                fishmid_y = int((cy1 + fishmid_y) / 2)
                # '''少商穴'''
                # smid_x = int((cx4 + cx3) / 2)
                # smid_y = int((cy4 + cy3) / 2)
                '''三间穴'''
                tk_x = int((cx5 + cx1) / 2)
                tk_y = int((cy0 + cy5 + cy5 + cy5) / 4)
                '''合谷穴'''
                cg_x = int((cx0 + cx2 + cx5) / 3)
                cg_y = int((cy0 + cy2 + cy2 + cy5) / 4)
                '''液门穴'''
                line1 = [(cx13, cy13), (cx18, cy18)]  # 13-18
                line2 = [(cx14, cy14), (cx17, cy17)]  # 14-17
                intersection = line_intersection(line1, line2)
                '''少商穴'''
                # 左手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[3], hand_landmarks.landmark[4], -20,
                                                           frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sm = line_intersection(line1_points, line2_points)
                    sml_x = int(intersection_sm[0])
                    sml_y = int(intersection_sm[1])
                except Exception as e:
                    print(str(e))
                # 右手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[3], hand_landmarks.landmark[4], 20,
                                                           frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sm = line_intersection(line1_points, line2_points)
                    smr_x = int(intersection_sm[0])
                    smr_y = int(intersection_sm[1])
                except Exception as e:
                    print(str(e))
                '''商阳穴'''
                # 左手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[7], hand_landmarks.landmark[8], -25,
                                                           frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    syl_x = int(intersection_sy[0])
                    syl_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))
                # 右手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[7], hand_landmarks.landmark[8], 25,
                                                           frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    syr_x = int(intersection_sy[0])
                    syr_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))
                '''关冲穴'''
                # 左手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[15], hand_landmarks.landmark[16],
                                                           25, frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    kcl_x = int(intersection_sy[0])
                    kcl_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))
                # 右手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[15], hand_landmarks.landmark[16],
                                                           -25, frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    kcr_x = int(intersection_sy[0])
                    kcr_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))

                '''少冲穴'''
                # 左手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[19], hand_landmarks.landmark[20],
                                                           -25, frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    shl_x = int(intersection_sy[0])
                    shl_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))
                # 右手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[19], hand_landmarks.landmark[20], 25,
                                                           frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    shr_x = int(intersection_sy[0])
                    shr_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))

                '''少泽穴'''
                # 左手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[19], hand_landmarks.landmark[20],
                                                           25, frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    sel_x = int(intersection_sy[0])
                    sel_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))
                # 右手
                vectors_data = calculate_direction_vectors(hand_landmarks.landmark[19], hand_landmarks.landmark[20],
                                                            -50,frame)
                # 取得两条线段的端点坐标
                line1_points = vectors_data['line_1_points']
                line2_points = vectors_data['line_2_points']
                try:
                    # 计算两条线段的交点
                    intersection_sy = line_intersection(line1_points, line2_points)
                    ser_x = int(intersection_sy[0])
                    ser_y = int(intersection_sy[1])
                except Exception as e:
                    print(str(e))

                # 手的方向
                if cy0 < cy12:
                    hand_dec = "ture"
                    print("cy0=",cy0)
                    print("cy12=",cy12)
                else:
                    hand_dec = "false"

                
                # 通过手部关键点判断手心或手背
                if hand_label == "Left":
                    if cx17 > cx2:  # 对左手来说，关键点 2 在 17 的左边表示手心朝上
                        hand_orientation = "palm"
                    else:
                        hand_orientation = "back"
                else:  # Right hand
                    if cx17 < cx2:  # 对右手来说，关键点 2 在 17 的右边表示手心朝上
                        hand_orientation = "palm"
                    else:
                        hand_orientation = "back"

                hand_orientations[hand_label] = hand_orientation






                # ============================================================新增五指张开=================================================

            # 根据选择的症状进行处理
            if selected_var.get() in ["哮喘", "降血压", "牙齿痛", "中暑", "心烦"]:
                if hand_dec == "ture":
                    if not hand_results.multi_hand_landmarks or all(
                            orientation == "back" for orientation in hand_orientations.values()):
                        frame = cv2ImgAddText(frame, "请以手心朝向镜头", x, y, (255, 0, 0), 30)
                    else:
                        if hand_orientation == "palm":
                            if selected_var.get() == "哮喘":
                                frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight,
                                                                frame, "鱼际穴", (fishmid_x, fishmid_y),
                                                                massage_threshold)
                            elif selected_var.get() == "降血压":
                                frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight,
                                                                frame, "劳宫穴", (lgmid_x, lgmid_y), massage_threshold)
                            elif selected_var.get() == "牙齿痛":
                                frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight,
                                                                frame, "少府穴", (cfmid_x, cfmid_y), massage_threshold)

                            elif selected_var.get() == "中暑":
                                if hand_position_text == 'ok':
                                    frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth,
                                                                    imgHeight, frame,
                                                                    "中冲穴", (cx12, cy12), massage_threshold)
                                elif hand_position_text != 'ok':
                                    cv2.putText(frame, "currvl hands", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (255, 255, 0),
                                                2)  # 显示手势判断结果

                            elif selected_var.get() == "心烦":
                                if hand_position_text == '4':
                                    if hand_label == "Left":
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth,
                                                                        imgHeight, frame,
                                                                        "少商穴", (sml_x, sml_y),
                                                                        massage_threshold)  # =======================左手的=======================
                                    elif hand_label == "Right":
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth,
                                                                        imgHeight,
                                                                        frame,
                                                                        "少商穴", (smr_x, smr_y), massage_threshold)
                                elif hand_position_text != '4':
                                    cv2.putText(frame, "hands 4", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (255, 255, 0),
                                                2)  # 显示手势判断结果
                

            elif selected_var.get() in ["落枕", "中风", "经痛", "头痛", "手指麻木", "结膜炎", "昏迷", "心肌炎"]:
                if hand_dec == "ture": #确认手的方向
                    if not hand_results.multi_hand_landmarks or all(
                            orientation == "palm" for orientation in hand_orientations.values()):
                        frame = cv2ImgAddText(frame, "请以手背朝向镜头", x, y, (255, 0, 0), 30)
                    else:
                        if hand_orientation == "back":
                            if selected_var.get() == "落枕":
                                frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                "中渚穴", (cfmid_x, cfmid_y), massage_threshold)
                            elif selected_var.get() == "中风":
                                frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                "三间穴", (tk_x, tk_y), massage_threshold)
                            elif selected_var.get() == "经痛":
                                frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                "合谷穴", (cg_x, cg_y), massage_threshold)
                            elif selected_var.get() == "头痛":
                                if hand_position_text == 'open':
                                    frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight,
                                                                    frame,
                                                                    "液门穴", (intersection[0], intersection[1]),
                                                                    massage_threshold)
                                elif hand_position_text != 'open':
                                    cv2.putText(frame, "open finger", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (255, 255, 0),
                                                2)  # 显示手势判断结果
                            elif selected_var.get() == "手指麻木":
                                if abs(cx12 - cx0) < 5:
                                    if hand_label == "Left":
                                        if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                            t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                            intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                            # 绘制交点
                                            intersection_x = int(intersection[0])
                                            intersection_y = int(intersection[1])
                                            # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                            distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                            # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                            other = (distance // 15) * 4  # 食指中指无名指宽度
                                            other = other / 2

                                            line_length_other1 = other
                                            point_other1 = (cx7_8, cy7_8)

                                            # 计算线段终点 无名指
                                            line_point_other = point_other1 + direction_vector * line_length_other1  # 根据方向矢量计算终点
                                            line_otherx = int(line_point_other[0])
                                            line_othery = int(line_point_other[1])
                                            frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                    "商阳穴", (line_otherx, line_othery), massage_threshold) # =======================左手的=======================
                                    elif hand_label == "Right":
                                        if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                            t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                            intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                            # 绘制交点
                                            intersection_x = int(intersection[0])
                                            intersection_y = int(intersection[1])
                                            # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                            distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                            # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                            other = (distance // 15) * 4  # 食指中指无名指宽度
                                            other = other / 2

                                            line_length_other1 = -other
                                            point_min = (cx19_20, cy19_20)
                                            point_other1 = (cx7_8, cy7_8)

                                            # 计算线段终点 无名指
                                            line_point_other = point_other1 + direction_vector * line_length_other1  # 根据方向矢量计算终点
                                            line_otherx = int(line_point_other[0])
                                            line_othery = int(line_point_other[1])
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight,
                                                                        frame,
                                                                        "商阳穴", (line_otherx, line_othery), massage_threshold)
                                else:
                                    print('cx12 != cx0')
                            elif selected_var.get() == "结膜炎":
                                if hand_label == "Left":
                                    # 检查是否有唯一解
                                    # ===========================================可统一======================
                                    if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                        t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                        intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                        # 绘制交点
                                        intersection_x = int(intersection[0])
                                        intersection_y = int(intersection[1])
                                        # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                        distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                        # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                        min = (distance // 15) * 3  # 小指宽度
                                        other = (distance // 15) * 4  # 食指中指无名指宽度
                                        min = min / 2
                                        other = other / 2

                                        line_length_min = min  # 加负号 另一边
                                        line_length_mn = -min
                                        line_length_other = -other
                                        line_length_other1 = other
                                        point_min = (cx19_20, cy19_20)
                                        point_other = (cx15_16, cy15_16)
                                        point_other1 = (cx7_8, cy7_8)
                                        # ==========================================================
                                        # 计算线段终点 无名指
                                        line_point_other = point_other + direction_vector * line_length_other  # 根据方向矢量计算终点
                                        line_otherx = int(line_point_other[0])
                                        line_othery = int(line_point_other[1])

                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth,
                                                                        imgHeight, frame,
                                                                        "关冲穴", (line_otherx, line_othery),
                                                                        massage_threshold)  # =======================左手的=======================


                                    else:
                                        print("两条线平行，没有交点。")

                                elif hand_label == "Right":
                                    if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                        t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                        intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                        # 绘制交点
                                        intersection_x = int(intersection[0])
                                        intersection_y = int(intersection[1])
                                        # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                        distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                        # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                        other = (distance // 15) * 4  # 食指中指无名指宽度
                                        other = other / 2

                                        line_length_other1 = other
                                        point_min = (cx19_20, cy19_20)
                                        point_other = (cx15_16, cy15_16)
                                        point_other1 = (cx7_8, cy7_8)

                                        # 计算线段终点 无名指
                                        line_point_other = point_other + direction_vector * line_length_other1  # 根据方向矢量计算终点
                                        line_otherx = int(line_point_other[0])
                                        line_othery = int(line_point_other[1])

                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth,
                                                                        imgHeight, frame,
                                                                        "关冲穴", (line_otherx, line_othery),
                                                                        massage_threshold)  # =======================左手的=======================

                            elif selected_var.get() == "昏迷":
                                if hand_label == "Left":
                                    if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                        t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                        intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                        # 绘制交点
                                        intersection_x = int(intersection[0])
                                        intersection_y = int(intersection[1])
                                        # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                        distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                        # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                        min = (distance//15)*3 #小指宽度
                                        min = min/2

                                        line_length_min = min  # 加负号 另一边
                                        line_length_mn = -min
                                        point_min = (cx19_20, cy19_20)

                                        # 计算线段终点 无名指
                                        line_point_mn = point_min + direction_vector * line_length_mn  # 根据方向矢量计算终点
                                        line_mnx = int(line_point_mn[0])
                                        line_mny = int(line_point_mn[1])
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                "少泽穴", (line_mnx, line_mny), massage_threshold) # =======================左手的=======================
                                elif hand_label == "Right":
                                    if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                        t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                        intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                        # 绘制交点
                                        intersection_x = int(intersection[0])
                                        intersection_y = int(intersection[1])
                                        # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                        distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                        # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                        min = (distance//15)*3 #小指宽度
                                        min = min/2

                                        line_length_mn = min
                                        point_min = (cx19_20, cy19_20)

                                        # 计算线段终点 无名指
                                        line_point_mn = point_min + direction_vector * line_length_mn  # 根据方向矢量计算终点
                                        line_mnx = int(line_point_mn[0])
                                        line_mny = int(line_point_mn[1])
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                "少泽穴", (line_mnx, line_mny), massage_threshold)

                            elif selected_var.get() == "心肌炎":
                                if hand_label == "Left":
                                    if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                        t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                        intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                        # 绘制交点
                                        intersection_x = int(intersection[0])
                                        intersection_y = int(intersection[1])
                                        # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                        distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                        # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                        min = (distance//15)*3 #小指宽度
                                        min = min/2

                                        line_length_mn = min
                                        point_min = (cx19_20, cy19_20)

                                        # 计算线段终点 无名指
                                        line_point_mn = point_min + direction_vector * line_length_mn  # 根据方向矢量计算终点
                                        line_mnx = int(line_point_mn[0])
                                        line_mny = int(line_point_mn[1])
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                                "少冲穴", (line_mnx, line_mny), massage_threshold)

                                    # =======================左手的=======================
                                elif hand_label == "Right":
                                    if np.linalg.det(A) != 0:  # 如果行列式不为零，则两条线有唯一交点
                                        t = np.linalg.solve(A, b)  # 求解线性方程组，得到 t1 和 t2
                                        intersection = point + t[0] * direction_vector1  # 计算交点坐标

                                        # 绘制交点
                                        intersection_x = int(intersection[0])
                                        intersection_y = int(intersection[1])
                                        # cv2.circle(frame, (intersection_x, intersection_y), 5, (0, 255, 0), -1)  # 用绿色绘制交点
                                        distance = np.sqrt((intersection_x - cx6) ** 2 + (intersection_y - cy6) ** 2)
                                        # print(f"交点和(cx6, cy6)之间的距离为: {distance}")
                                        min = (distance//15)*3 #小指宽度
                                        min = min/2

                                        line_length_mn = -min
                                        point_min = (cx19_20, cy19_20)

                                        # 计算线段终点 无名指
                                        line_point_mn = point_min + direction_vector * line_length_mn  # 根据方向矢量计算终点
                                        line_mnx = int(line_point_mn[0])
                                        line_mny = int(line_point_mn[1])
                                        frame = handle_acupoint_massage(hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame,
                                                               "少冲穴", (line_mnx, line_mny), massage_threshold)
                else:
                    frame = cv2ImgAddText(frame, "镜头颠倒了", x, y, (255, 0, 0), 30)

            elif selected_var.get() in ["手阳明大肠经", "手少阳三焦经", "手太阳小肠经"]:
                if hand_dec == "ture":
                    if not hand_results.multi_hand_landmarks or all(
                            orientation == "palm" for orientation in hand_orientations.values()):
                        frame = cv2ImgAddText(frame, "请以手背朝向镜头", x, y, (255, 0, 0), 30)
                    else:
                        if hand_orientation == "back":
                            if selected_var.get() == "手阳明大肠经":
                                if hand_label == "Left":
                                    cv2.circle(frame, (syl_x, syl_y), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "商阳穴", syl_x, syl_y, (255, 0, 0),
                                                        20)  # =======================左手的=======================
                                    cv2.line(frame, (syl_x, syl_y), (tk_x, tk_y), purple_color, 2)
                                elif hand_label == "Right":
                                    cv2.circle(frame, (syr_x, syr_y), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "商阳穴", syr_x, syr_y, (255, 0, 0), 20)
                                    cv2.line(frame, (syr_x, syr_y), (tk_x, tk_y), purple_color, 2)

                                cv2.circle(frame, (cg_x, cg_y), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "合谷穴", cg_x, cg_y, (255, 0, 0), 20)
                                cv2.circle(frame, (tk_x, tk_y), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "三间穴", tk_x, tk_y, (255, 0, 0), 20)

                                cv2.line(frame, (cg_x, cg_y), (tk_x, tk_y), purple_color, 2)

                            elif selected_var.get() == "手少阳三焦经":
                                if hand_label == "Left":
                                    cv2.circle(frame, (kcl_x, kcl_y), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "关冲穴", kcl_x, kcl_y, (255, 0, 0),
                                                        20)  # =======================左手的=======================
                                    cv2.line(frame, (kcl_x, kcl_y), (intersection[0], intersection[1]), purple_color, 2)
                                elif hand_label == "Right":
                                    cv2.circle(frame, (kcr_x, kcr_y), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "关冲穴", kcr_x, kcr_y, (255, 0, 0), 20)
                                    cv2.line(frame, (kcr_x, kcr_y), (intersection[0], intersection[1]), purple_color, 2)

                                cv2.circle(frame, (intersection[0], intersection[1]), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "液门穴", intersection[0], intersection[1], (255, 0, 0), 20)
                                cv2.circle(frame, (cfmid_x, cfmid_y), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "中渚穴", cfmid_x, cfmid_y, (255, 0, 0), 20)

                                cv2.line(frame, (intersection[0], intersection[1]), (cfmid_x, cfmid_y), purple_color, 2)

                            elif selected_var.get() == "手太阳小肠经":
                                if hand_label == "Left":
                                    cv2.circle(frame, (sel_x, sel_y), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "少泽穴", sel_x, sel_y, (255, 0, 0),
                                                        20)  # =======================左手的=======================
                                elif hand_label == "Right":
                                    cv2.circle(frame, (ser_x, ser_y), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "少泽穴", ser_x, ser_y, (255, 0, 0), 20)
                else:
                    frame = cv2ImgAddText(frame, "镜头颠倒了", x, y, (255, 0, 0), 30)   


            elif selected_var.get() in ["手太阴肺经", "手厥阴心包经", "手少阴心经"]:
                if hand_dec == "ture":
                    if not hand_results.multi_hand_landmarks or all(
                            orientation == "back" for orientation in hand_orientations.values()):
                        frame = cv2ImgAddText(frame, "请以手心朝向镜头", x, y, (255, 0, 0), 30)
                    else:
                        if hand_orientation == "palm":
                            if selected_var.get() == "手太阴肺经":
                                if hand_position_text == '4':
                                    if hand_label == "Left":
                                        cv2.circle(frame, (sml_x, sml_y), 5, blue_color, -1)
                                        frame = cv2ImgAddText(frame, "少商穴", sml_x, sml_y, (255, 0, 0),
                                                            20)
                                        cv2.line(frame, (sml_x, sml_y), (fishmid_x, fishmid_y), purple_color, 2)
                                    elif hand_label == "Right":
                                        cv2.circle(frame, (smr_x, smr_y), 5, blue_color, -1)
                                        frame = cv2ImgAddText(frame, "少商穴", smr_x, smr_y, (255, 0, 0), 20)
                                        cv2.line(frame, (smr_x, smr_y), (fishmid_x, fishmid_y), purple_color, 2)

                                    cv2.line(frame, (smr_x, smr_y), (fishmid_x, fishmid_y), purple_color, 2)
                                elif hand_position_text != '4':
                                    cv2.putText(frame, "currvl bigfinger", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (255, 255, 0),
                                                2)  # 显示手势判断结果

                                cv2.circle(frame, (fishmid_x, fishmid_y), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "鱼际穴", fishmid_x, fishmid_y, (255, 0, 0), 20)
                                # cv2.line(frame, (smid_x, smid_y), (fishmid_x, fishmid_y), purple_color, 2)

                            elif selected_var.get() == "手厥阴心包经":
                                if hand_position_text == '7':
                                    cv2.circle(frame, (cx12, cy12), 5, blue_color, -1)
                                    frame = cv2ImgAddText(frame, "中冲穴", cx12, cy12, (255, 0, 0),
                                                        20)
                                elif hand_position_text != '7':
                                    cv2.putText(frame, "currvl midfinger", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (255, 255, 0),
                                                2)  # 显示手势判断结果

                                cv2.circle(frame, (lgmid_x, lgmid_y), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "劳宫穴", lgmid_x, lgmid_y, (255, 0, 0), 20)
                                cv2.line(frame, (cx12, cy12), (lgmid_x, lgmid_y), purple_color, 2)

                            elif selected_var.get() == "手少阴心经":
                                if hand_position_text == '9':
                                    if hand_label == "Left":
                                        cv2.circle(frame, (shl_x, shl_y), 5, blue_color, -1)
                                        frame = cv2ImgAddText(frame, "少冲穴", shl_x, shl_y, (255, 0, 0),
                                                            20)
                                        cv2.line(frame, (shl_x, shl_y), (cfmid_x, cfmid_y), purple_color, 2)
                                    elif hand_label == "Right":
                                        cv2.circle(frame, (shr_x, shr_y), 5, blue_color, -1)
                                        frame = cv2ImgAddText(frame, "少冲穴", shr_x, shr_y, (255, 0, 0), 20)
                                        cv2.line(frame, (shr_x, shr_y), (cfmid_x, cfmid_y), purple_color, 2)

                                elif hand_position_text != '9':
                                    cv2.putText(frame, "currvl smallfinger", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (255, 255, 0),2)  # 显示手势判断结果

                                cv2.circle(frame, (cfmid_x, cfmid_y), 5, blue_color, -1)
                                frame = cv2ImgAddText(frame, "少府穴", cfmid_x, cfmid_y, (255, 0, 0), 20)
                else:
                    frame = cv2ImgAddText(frame, "镜头颠倒了", x, y, (255, 0, 0), 30)




        # 将图像从 OpenCV 格式转换为 PIL 格式以便在 Tkinter 中显示
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # 根据页面选择显示视频或时钟
        current_tab = notebook.index(notebook.select())
        if current_tab == 0:
            video_label_symptom.imgtk = imgtk
            video_label_symptom.config(image=imgtk)
        elif current_tab == 1:
            video_label_meridian.imgtk = imgtk
            video_label_meridian.config(image=imgtk)
        elif current_tab == 2:
            # 在 "此刻时辰" 页面上不显示实时影像，只显示时钟
            pass

    # 循环调用
    root.after(10, update_frame)

# 启动图像更新循环
update_frame()
# 启动 Tkinter 主循环
root.mainloop()
# 释放视频捕获设备
cap.release()

# 修改倒计时显示函数
def show_countdown(seconds, label, acupoint_name, acupoint_coords, hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame):
    if seconds > 0:
        frame = cv2ImgAddText(frame, f"{seconds}", imgWidth // 2, imgHeight // 2, COLORS['prompt_text'], 50)
        label.after(1000, lambda: show_countdown(seconds - 1, label, acupoint_name, acupoint_coords, hand_label, hand_landmarks_dict, imgWidth, imgHeight, frame))
    else:
        frame = cv2ImgAddText(frame, "按摩完成！", imgWidth // 2, imgHeight // 2, COLORS['prompt_text'], 30)
        label.after(1000, lambda: update_frame())