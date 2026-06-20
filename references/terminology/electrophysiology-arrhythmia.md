# 心脏电生理与心律失常术语路由

本文件只负责选择分库，不再承载全部电生理术语。根据段落主题读取最少的相关文件。

## 本地三书的证据用途

- **M**：《梅奥心脏电生理学》中文版，用于核对中国心脏电生理教材中的稳定术语。
- **HE**：*Huang's Catheter Ablation of Cardiac Arrhythmias* 英文原版，用于确定英文概念、技术边界和第五版新增术语。
- **HC-ref**：该书简体中文 PDF，仅作译法候选、检索线索和误译样本，不单独决定首选中文。

本地书证标记不能替代总索引中的 `T/N/G/P` 规范等级。`HE` 或 `HC-ref` 单独出现时，不得把译名标为教材规范。

## 按主题加载

| 识别到的内容或关键词 | 加载文件 |
|---|---|
| 电生理机制、心内电图、程序刺激、激动/电压/起搏/拖带标测、三维标测 | `electrophysiology/fundamentals-mapping.md` |
| 射频、冷冻、脉冲电场、激光、损伤形成、食管保护、心腔内超声、房间隔穿刺 | `electrophysiology/ablation-energy-imaging.md` |
| 房室结折返、房室折返、旁路、房速、房扑、室上性心动过速 | `electrophysiology/supraventricular-arrhythmias.md` |
| 房颤、肺静脉隔离、非肺静脉触发灶、左心房线性消融、Marshall静脉 | `electrophysiology/atrial-fibrillation.md` |
| 室早、室速、室颤、流出道、乳头肌、左心室顶部、分支性或瘢痕相关室速 | `electrophysiology/ventricular-arrhythmias.md` |
| 起搏器、ICD、CRT、电极导线、夺获/感知、围术期并发症 | `electrophysiology/pacing-devices-complications.md` |

## 组合加载规则

- “某种心律失常的标测与消融”通常加载对应心律失常分库，并补充 `fundamentals-mapping.md`；只有原文讨论能量、损伤或影像时才加载 `ablation-energy-imaging.md`。
- 房颤章节不要自动加载全部室上性心律失常术语；室性心律失常章节也不要自动加载起搏器术语。
- 解剖图注另加载 `../anatomy-physiology.md`；先天性心脏病术后心律失常另加载 `../congenital-surgery-critical-care.md`。
- 同一术语存在不同书内译法时，按总索引优先级定稿，并将 HC-ref 的译法视为可否决证据而非确认依据。
