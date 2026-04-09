# 明穴智疗
Using mediapipe for acupoint AR and related health care applications

# 成果展现:
https://private-user-images.githubusercontent.com/208995280/575730902-b35b59e0-58df-4a48-913c-9871a14b3521.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU3MTQyNDYsIm5iZiI6MTc3NTcxMzk0NiwicGF0aCI6Ii8yMDg5OTUyODAvNTc1NzMwOTAyLWIzNWI1OWUwLTU4ZGYtNGE0OC05MTNjLTk4NzFhMTRiMzUyMS5tcDQ_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNDA5JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDQwOVQwNTUyMjZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05OTgwZjgzNDQxOGQzZGU3Mzc0YjI0N2ZhYzhhNTBhNjcwMWVlYjVjNDZiYzc2NzhhMmFmMDdlZDNiMGY4NjA3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.N2G6ExvcBamUjgFKEyKvw7o2Ft5YZzjlHSfZE58M3pw


画面上方分别有三个按钮


**• 症状按摩舒缓:**

使用者可从下拉选单中选择特定症状，程序将自动显示与该症状相关的穴位位置。这种设计让使用者能快速找到对应的穴位，简化中医穴位查找的过程，提升应用的效率与便利性。

**• 经络学习:**

使用者可通过下拉选单选择所需的经络，系统将自动显示该经络上所有相应的穴位，并以连线的方式呈现经络路径。这种互动式设计，让使用者能直观了解每条经络的分布与穴位位置，大幅提升经络学习与应用的便利性。

**• 当前时辰**

# 设备:

• 外接摄像头

• Python

• 需在Python中下载mediapipe、tkinter、PIL和numpy等套件

# 摘要:
&nbsp;&nbsp;&nbsp;&nbsp;穴位查找一直是许多希望进行身体保健的民众所面临的一大难题。网络上关于穴位定位的信息常伴随大量专业医学术语，对一般民众而言既难以理解又缺乏实用性。因此，本专题旨在结合科技与中医智慧，将传统的穴位查找方法数字化。通过 Mediapipe Hands 技术，准确输出穴位位置，并通过即时影像将这些穴位清晰地标示在使用者的手上。这种直观的方式，不仅省去了民众学习复杂穴位知识的麻烦，更大幅提升了进行穴位按摩的便利性与效率。

&nbsp;&nbsp;&nbsp;&nbsp;如果民众能在日常小病小痛时，优先通过穴位按摩进行缓解，或养成日常保健的良好习惯，将有助于促进全民健康。同时，也能有效减轻医疗资源的负担，为我国医疗体系创造长远的助益。此创新解决方案融合了科技与中医，期望以更简单、更高效的方式，推动穴位疗法的普及与应用，让健康管理变得更轻松、更贴近生活。

关键词：Mediapipe Hands、AR、穴位辨识

# 前言:
&nbsp;&nbsp;&nbsp;&nbsp;在当今社会，随着健康意识的提升，越来越多的人开始重视身体保健。穴位疗法作为中医的重要组成部分，因其简便且有效而受到广泛关注。然而，对于普通民众而言，准确查询及应用穴位常常是一个挑战。许多网上资源充斥着专业的医学术语，导致普通人难以理解其精髓及实用性。因此，为了解决这一问题，本专题旨在结合新兴科技与中医智慧，将传统的穴位查询方法数字化，提供一个更直观且易于操作的工具。通过使用 Mediapipe Hands 技术，我们将能够实现更加准确和便捷的穴位定位，让每个人都能轻松地进行自我保健，提升生活品质。希望本研究能为广大追求健康的人士带来实质性的帮助，并推动中医文化的普及与现代化。

# Mediapipe hands 简介:
Mediapipe Hands 是 Google 提供的 Mediapipe 框架中的一个模块，专注于 手部追踪与姿势估计。它能够通过影像或影片实时检测手部，并预测每只手 21 个关键点的三维位置。

**主要功能:**

	• 手部检测 (Hand Detection)：侦测影像中是否存在手部，并绘制边界框。
	• 手势追踪 (Hand Landmark Tracking)：识别并追踪手部关键点，包含手指关节及掌心。
	• 多手支持 (Multi-hand Support)：能同时检测与追踪多只手，最多可支持双手。

**技术特点**
	
	• 高效能：运行速度快，可在移动装置或嵌入式设备上实时处理。
	• 准确性：通过深度学习模型，准确预测手部姿势和关键点位置。
	• 跨平台支持：可在 Android、iOS、Windows、macOS、Linux 等多个平台使用。

**应用范例**

	• 手势控制：用于人机界面中，手势控制应用如虚拟鼠标、媒体播放器控制等。
	• AR/VR 应用：支持虚拟现实中的手势交互。
	• 健康与运动监测：用于手部复健训练监测或运动姿势分析。

**优势**

	• 开源：免费开放，社群活跃且持续更新。
	• 实时性强：适合需要即时反应的应用场景。
	• 易于整合：可与 OpenCV、TensorFlow 等常见框架搭配使用。

Mediapipe Hands 是影像处理领域中极具潜力的工具，适合用于开发多种手势识别与人机互动应用。
	
**官网链接**
https://chuoling.github.io/mediapipe/solutions/hands.html

# 未来应用 : 
1.软件：开发专属的App，方便使用者随时掌握穴位定位信息并进行自我保健。

2.硬件：使用机械手臂替代手动按摩，提供更加精准且便捷的自动化按摩解决方案，提升使用者的舒适度与疗效。

2.深度学习：在现有基础上，积累数据库并训练模型，以克服目前使用mediapipe受到的限制，实现更灵活的功能。

# 翻译方式:
依照中医穴位定位的说明，自行推论出用mediapipe hands 如何找到穴位，再到网络上查找中医师所拍摄的穴位照片，以验证穴位是否正确。

自行推论详见:[穴位.xlsx](h[ttps://github.com/jaipei1030/Use-mediapipe-to-find-acupuncture-points-in-the-human-body/blob/main/%E7%A9%B4%E4%BD%8D.xlsx](https://github.com/Dieu-12138/mediapipe-hands/blob/main/%E7%A9%B4%E4%BD%8D.xlsx))

验证穴位详见:[检测穴位.docx]([https://github.com/jaipei1030/Use-mediapipe-to-find-acupuncture-points-in-the-human-body/blob/main/%E6%AA%A2%E6%B8%AC%E7%A9%B4%E4%BD%8D.pdf](https://github.com/Dieu-12138/mediapipe-hands/blob/main/%E6%A3%80%E6%B5%8B%E7%A9%B4%E4%BD%8D.docx))

# 结论 : 
&nbsp;&nbsp;&nbsp;&nbsp;从照片验证的结果来看，Mediapipe Hands 技术在定位穴位方面确实展现了其准确性与可行性。然而，鉴于穴位具有重要的医疗用途，涉及人体健康与治疗效果，若要进一步将此应用推广至实际临床或保健领域，仍需要专业医师的检测与验证，确保定位准确度与实际应用的安全性。因此，本专题目前定位于教育用途，旨在帮助普通用户理解并学习穴位疗法的基本知识，降低中医保健的入门门槛，并推广中医文化的基础概念。

&nbsp;&nbsp;&nbsp;&nbsp;本研究具备巨大的发展潜力与应用前景。未来，若经由专业医师的充分验证和调整，我们计划将此技术应用于更广泛的领域，并朝着硬件整合与深度学习的方向进一步发展。例如，可开发便携式健康监测设备，结合穴位定位与即时健康数据分析，为用户提供个性化的健康建议。同时，通过深度学习模型的引入，进一步优化穴位定位的准确度，并探索不同身体部位的自动化穴位检测功能，使其应用范围不仅限于手部。

&nbsp;&nbsp;&nbsp;&nbsp;此外，我们还可以考虑将此技术与其他现代医疗设备结合，例如加入影像诊断功能或生物指标监测技术，以提供更全面的健康管理方案。未来，该系统也可与智慧医疗平台整合，建立云端数据库，收集更多人体穴位与健康状况的相关数据，从而进一步完善技术模型。这不仅能提升穴位疗法的应用效率，还能为中医现代化提供新的发展方向，助力中医疗法在全球范围内的普及与推广。最终，我们期望这项技术能成为连结传统医疗智慧与现代科技的桥梁，为人类健康事业带来更多可能性与创新价值。

root = tk.Tk()
root.title("明穴智疗")

