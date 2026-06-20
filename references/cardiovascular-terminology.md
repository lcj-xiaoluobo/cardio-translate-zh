# 心血管亚专业术语总索引

本索引用于心血管医学英译中、术语统一、图注与图内标签翻译。详细条目按需从分库加载，避免把完整术语库一次性写入上下文。

## 导航

- [A0最高权限与裁决顺序](#a0-最高权限来源)
- [强制检索流程](#强制检索流程)
- [A0官方分库路由](#a0-官方分库路由)
- [扩展分库路由](#扩展分库路由)
- [高频规范词与易错词](#高频-a0-规范词)
- [交付前术语核验](#交付前术语核验)

## A0 最高权限来源

`references/terminology/cnterm-2025/` 收录全国科学技术名词审定委员会《心血管病学名词（2025）》征求意见稿的 **1,434 条**中英名词，覆盖 **30 个章节分库**。用户指定该 PDF 为本 Skill 的最高术语裁决来源。

原稿存在编号复用：1,434 条名词对应 1,374 个不同编号，59 个编号分别用于不同条目。不得擅自重编号；需要追溯时同时记录“章节 + 编号 + 规范中文名”，并查阅 `terminology/cnterm-2025/code-collisions.md`。

执行规则：

1. 概念与 PDF 条目确切对应时，必须采用其“规范中文名”。
2. A0 与教材、指南、项目旧译或本 Skill 扩展库冲突时，A0 胜出。
3. 只有用户随后针对某个具体术语明确指定新译法，才能覆盖 A0；将该译法记录为项目例外，不得静默扩展到相近概念。
4. A0 规范的是中文定名。PDF 英文栏中的拼写、标点、单复数和缩写若存在原稿问题，可依据原文语境校正，但不得借此改写其中文名。
5. 不得仅因英文词形相似就套用 A0 条目；先确认疾病、结构、机制、操作、器械或指标是同一概念。
6. PDF 当前标注为“征求意见稿”。交付术语表或说明来源时如实保留该状态，不将其表述为已正式发布的终审版。

## 裁决顺序

| 权限 | 来源 | 用法 |
|---|---|---|
| A0 | 《心血管病学名词（2025）》征求意见稿 | 最高权限；概念匹配时直接采用规范中文名 |
| A1 | 用户随后明确指定的单项译法 | 仅覆盖指定术语，并记录为项目例外 |
| T | 中国大陆现行医学教材稳定用语 | 补充 A0 未收录的成熟概念 |
| N | 其他全国科学技术名词审定委员会规范名词 | 与 A0 不冲突时采用 |
| G | 国内指南、共识及专业学会稳定用语 | 用于新技术、新分型、新器械和新治疗 |
| J | 权威中文专业期刊稳定用法 | 上述来源未覆盖时参考 |
| P | 暂定译名 | 首次出现保留英文，并列入待核对项 |

旧标记 `M`、`HE`、`HC-ref` 只表示本地书证来源，不具有覆盖 A0/T/N/G 的权限。

## 强制检索流程

1. 识别英文术语的完整概念、亚专业、词性和上下文。
2. 先在 `terminology/cnterm-2025/` 全量检索英文、缩写及中文候选词。
3. 命中 A0 后核对概念和章节，采用规范中文名；不要继续用低权限来源替换。
4. A0 未命中时，加载相关扩展分库；电生理文本还需加载其主题子库。
5. 仍未命中时按 A1/T/N/G/J/P 顺序核定，并保持首次出现格式和项目一致性。

推荐检索命令：

```bash
rg -ni -F "complete English term" references/terminology/cnterm-2025
rg -ni "English variant|ABBR|中文候选" references/terminology/cnterm-2025
rg -ni "English variant|ABBR|中文候选" references/terminology
```

检索缩写时必须再查英文全称，避免把相同缩写映射到错误亚专业概念。

## A0 官方分库路由

总目录、每章条目数和编号冲突说明见 `terminology/cnterm-2025/README.md` 与 `terminology/cnterm-2025/code-collisions.md`。

| 内容 | A0 文件 |
|---|---|
| 学科、分支学科 | `terminology/cnterm-2025/01-disciplines.md`、`terminology/cnterm-2025/01-01-branches.md` |
| 流行病学、研究设计、统计指标 | `terminology/cnterm-2025/02-epidemiology.md` |
| 组织学 | `terminology/cnterm-2025/03-01-histology.md` |
| 心血管解剖学 | `terminology/cnterm-2025/03-02-anatomy.md` |
| 生理学、血流动力学 | `terminology/cnterm-2025/03-03-physiology.md` |
| 病理学 | `terminology/cnterm-2025/03-04-pathology.md` |
| 症状与体征 | `terminology/cnterm-2025/03-05-symptoms-signs.md` |
| 检验、检查、影像和设备 | `terminology/cnterm-2025/03-06-tests-devices.md` |
| 心力衰竭 | `terminology/cnterm-2025/04-01-heart-failure.md` |
| 心律失常、电生理、起搏与消融 | `terminology/cnterm-2025/04-02-arrhythmia.md` |
| 心脏骤停、心源性猝死 | `terminology/cnterm-2025/04-03-cardiac-arrest-scd.md` |
| 先天性心脏病 | `terminology/cnterm-2025/04-04-congenital-heart-disease.md` |
| 高血压 | `terminology/cnterm-2025/04-05-hypertension.md` |
| 动脉粥样硬化、冠心病及介入 | `terminology/cnterm-2025/04-06-atherosclerosis-coronary.md` |
| 心脏瓣膜病 | `terminology/cnterm-2025/04-07-valvular-heart-disease.md` |
| 感染性心内膜炎 | `terminology/cnterm-2025/04-08-infective-endocarditis.md` |
| 心肌疾病 | `terminology/cnterm-2025/04-09-myocardial-disease.md` |
| 心包疾病 | `terminology/cnterm-2025/04-10-pericardial-disease.md` |
| 主动脉和周围血管疾病 | `terminology/cnterm-2025/04-11-aortic-peripheral-vascular.md` |
| 肺血管病 | `terminology/cnterm-2025/04-12-pulmonary-vascular.md` |
| 心脏肿瘤 | `terminology/cnterm-2025/04-13-cardiac-tumor.md` |
| 合理用药基本概念 | `terminology/cnterm-2025/05-01-pharmacotherapy-concepts.md` |
| 抗高血压药物 | `terminology/cnterm-2025/05-02-antihypertensive-drugs.md` |
| 抗心律失常药 | `terminology/cnterm-2025/05-03-antiarrhythmic-drugs.md` |
| 心力衰竭治疗药物 | `terminology/cnterm-2025/05-04-heart-failure-drugs.md` |
| 抗血小板和抗凝治疗 | `terminology/cnterm-2025/05-05-antiplatelet-anticoagulation.md` |
| 调脂药 | `terminology/cnterm-2025/05-06-lipid-lowering-drugs.md` |
| 心血管康复 | `terminology/cnterm-2025/06-cardiovascular-rehabilitation.md` |
| 心血管护理 | `terminology/cnterm-2025/07-cardiovascular-nursing.md` |

## 扩展分库路由

扩展库只补充 A0 未收录的细分解剖、新技术、新器械和出版项目用语，不得覆盖 A0。

| 内容 | 扩展文件 |
|---|---|
| 解剖、生理、血流动力学、胚胎学 | `terminology/anatomy-physiology.md` |
| 心律失常、电生理、起搏、导管消融 | `terminology/electrophysiology-arrhythmia.md`，再加载 `terminology/electrophysiology/` 对应主题子库 |
| 冠心病、冠状动脉介入、腔内影像 | `terminology/coronary-intervention.md` |
| 瓣膜病、结构性心脏病、超声、CT、磁共振 | `terminology/structural-imaging.md` |
| 心力衰竭、心肌病、移植、机械循环支持 | `terminology/heart-failure-cardiomyopathy.md` |
| 高血压、血脂、预防、康复、临床研究 | `terminology/hypertension-prevention.md` |
| 血栓与抗栓、肺血管病、主动脉及外周血管病 | `terminology/vascular-thrombosis.md` |
| 先天性心脏病、心外科、心血管重症 | `terminology/congenital-surgery-critical-care.md` |

## 高频 A0 规范词

| English | A0 规范中文 | 官方编号 | 说明 |
|---|---|---|---|
| arrhythmia | 心律失常 | 04.050 | 不写“心率失常” |
| heart failure | 心力衰竭 | 04.001 | 可在已定义后简称“心衰” |
| sudden cardiac arrest | 心脏骤停 | 04.265 | SCA；普通 `cardiac arrest` 仍须结合原文和项目体例 |
| sudden cardiac death | 心源性猝死 | 04.266 | SCD；遵循 A0，不沿用旧库“心脏性猝死” |
| atrial fibrillation | 心房颤动 | 04.133 | AF |
| atrial flutter | 心房扑动 | 04.132 | — |
| ventricular fibrillation | 心室颤动 | 04.176 | VF |
| radiofrequency catheter ablation | 经导管射频消融术 | 03.366 | RFCA；泛称 `catheter ablation` 需按语境处理 |
| percutaneous coronary intervention | 经皮冠状动脉介入治疗 | 04.568 | PCI |
| ejection fraction | 射血分数 | 03.127 | EF |
| cardiac output | 心输出量 | 03.118 | 遵循 A0；不要沿用旧库“心排血量” |
| stroke volume | 每搏输出量 | 03.117 | — |
| preload | 前负荷 | 03.120 | — |
| afterload | 后负荷 | 03.121 | — |
| ventricular remodeling | 心室重塑 | 04.043 | 遵循 A0；其他 `remodeling` 组合须另行核定 |

## 易错词与语境裁决

| English | 处理规则 |
|---|---|
| lead | 心电图为“导联”；起搏系统为“电极导线” |
| capture | 起搏语境依 A0 具体条目使用“夺获”；一般数据采集或影像语境另译 |
| entrainment | A0 为“拖带现象”；行文可依名词功能写“拖带”或“拖带标测” |
| substrate | 电生理常为“基质”；代谢、药理和材料语境不得套用 |
| burden | 可为负荷、疾病负担、发作负荷或发生比例，按指标定义判断 |
| cusp / leaflet | 先确定瓣膜与官方定名，不按英文词形机械区分“瓣尖/瓣叶” |
| annulus | 通常为瓣环；影像学、外科和功能性瓣环定义须结合语境 |
| ostium | 按官方结构名译为口、开口或入口 |
| sinus | 可为窦、静脉窦或主动脉窦，先确定解剖实体 |
| ridge / crest | 已命名结构用规范名；一般形态可为嵴、隆起或缘 |
| recess / fossa | 通常分别为隐窝与窝，不得互换 |
| compliance | 生理学通常为顺应性；患者行为语境才可能是依从性 |
| shock | 循环衰竭为休克；除颤治疗动作为电击 |

## 专名、缩写与新技术

- A0 已收录的冠名术语使用其规范中文名。
- A0 未收录而国内已有公认译名的专名，首次写“中文名（英文原名）”；图内空间不足时可仅用中文标准名，并在图注或术语表保留英文。
- 缩写首次出现通常写“中文全称（英文全称，缩写）”；图内标签按可读空间简化，但不得造成歧义。
- 新器械、商品名、试验名和快速演变技术若 A0 未收录，优先采用国内指南或共识用语；仍不稳定时标记 `P` 并保留英文。

## 交付前术语核验

- A0 命中项是否严格采用规范中文名。
- 是否把 A0 英文栏的原稿拼写问题误当成中文定名依据。
- 是否出现同一概念多译、同一缩写误配或亚专业串义。
- 是否把扩展库、英文网页或机器翻译结果放在 A0 之前。
- 是否逐项复核侧别、方位、数字、单位、药物通用名和图表对应关系。
