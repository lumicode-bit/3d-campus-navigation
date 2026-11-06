# 江西师范大学瑶湖校区：OSM 实测数据 vs 现有 map.txt 对比报告

> 生成日期：2026-09-25　数据源：OpenStreetMap（Overpass API，ODbL 1.0）　对比对象：`map.txt`（VERSION 1，73 栋）
> 本报告只产出数据与分析，**未改动 main.c 或 map.txt**。

## 一、数据获取

- 校区边界：OSM way **227753265**「江西师范大学（瑶湖校区）」，`amenity=university`，闭合多边形 38 节点
- 校区面积（平面估算）：**151.1 公顷**；`get_buildings.py` 中设定的中心点位于校区几何中心**以西约 1133 m**（已在校区多边形之外）
- 取数范围：纬度 28.6735~28.6895、经度 116.0120~116.0360
- 复现用 Overpass 语句：

```overpassql
[out:json][timeout:40];
way[building](28.6735,116.0120,28.6895,116.0360);
out geom;
```

- 取回建筑 **108 处**：校区内 **32**、校区边界外 120 m 内 3、其余 73（多为隔壁江西科技学院、奥体中心、商业体）
- 校区内道路按 40 m 缓冲裁剪后 **168 段**（footway / service / residential / steps / pedestrian）

## 二、覆盖情况

| 指标 | 现有 map.txt | OSM 实测 |
|---|---|---|
| 建筑数量 | 73（含 3 处明显的编辑器残留：New Building 73、Fengyu Qiuchang2、Wangqiuchang2） | 32（校区内，其中 31 有名称） |
| 建筑形状 | 全部为矩形/简单多边形，尺寸 1.6~16 单位 | 实测轮廓，4~26 节点，面积 1 千~2.2 万 m² |
| 高度信息 | 0.2~28（示意值） | 108 处中 41 处有 building:levels，仅 1 处有 height |
| 道路 | 7 条 + 13 点环路（示意） | 168 段真实步道/支路 |
| 名称匹配 | **25 组**可同名对应，2 组仅几何相邻，**46 栋在 OSM 中无对应** | —— |

### 2.1 可对应的建筑（25 组，同名/同功能）

| 现有名称 | OSM 名称 | 现有占地估算(m²) | OSM 实测(m²) | 面积倍数 | 中心偏差(m) |
|---|---|---|---|---|---|
| Wangqiuchang | 望城篮球场 | 19,133 | 10,307 | 1.86× | 682 |
| Weiyi Lou | 惟义楼 | 116,071 | 22,079 | 5.26× | 314 |
| Xingzhi Lou | 知行楼（行政楼） | 25,510 | 3,883 | 6.57× | 265 |
| Dorm 15 | 15栋 | 9,796 | 3,140 | 3.12× | 248 |
| Yaohu Tiyuguan | 瑶湖体育馆 | 71,429 | 11,725 | 6.09× | 199 |
| Dorm 16 | 16栋 | 9,796 | 2,115 | 4.63× | 187 |
| Zhouzhuan 1 | 周转房 | 12,245 | 1,258 | 9.73× | 185 |
| Baowei Lou | 保卫楼 | 15,306 | 818 | 18.70× | 176 |
| Zhouzhuan 2 | 周转房 | 12,245 | 1,258 | 9.73× | 170 |
| Xiaoyiyuan | 江西师范大学校医院 | 15,306 | 5,210 | 2.94× | 167 |
| Dorm 1 | 1栋 | 9,796 | 2,407 | 4.07× | 165 |
| Changsheng Tiyuchang | 长胜体育馆 | 63,138 | 6,330 | 9.98× | 163 |
| Dorm 14 | 14栋 | 9,796 | 5,382 | 1.82× | 158 |
| Ershitang | 芒果青年（二食堂） | 30,612 | 3,249 | 9.42× | 153 |
| Tianlang Lou | 天浪楼·音乐学院 | 25,510 | 4,500 | 5.67× | 130 |
| Wushitang | 福泉餐厅（五食堂） | 20,408 | 1,015 | 20.10× | 112 |
| Cainiao Yizhan | 江西师范大学快递中心 | 9,184 | 860 | 10.68× | 111 |
| Dorm 2 | 2栋 | 9,796 | 2,260 | 4.33× | 104 |
| Yishitang | 一食堂 | 30,612 | 2,872 | 10.66× | 103 |
| Dorm 13 | 13栋 | 9,796 | 5,521 | 1.77× | 103 |
| San Shitang | 长胜园（三食堂） | 22,959 | 6,353 | 3.61× | 102 |
| Meishu Xueyuan | 超真楼·美术学院 | 25,510 | 4,570 | 5.58× | 91 |
| Dorm 3 | 3栋 | 9,796 | 2,008 | 4.88× | 90 |
| Dorm 4 | 4栋 | 9,796 | 2,638 | 3.71× | 72 |
| Bailu Huiguan | 白鹿会馆（国际交流中心） | 30,612 | 4,599 | 6.66× | 41 |

### 2.2 OSM 有、现有地图缺的建筑（6 处）

　百时乐（四食堂）、国旗台、(无名，OSM id 971592725)、17栋、18栋、19栋

### 2.3 现有地图有、OSM 未收录的建筑（46 栋）

　Zhengda Men、Zhengda Fang、Zhengda Plaza、Shengqi Tai、Xiaoshi Jinianbei、Taoli Ding、Xiaohui Xiaoxun Qiang、Jing Hu Xi、Jing Hu Dong、Jing Hu Bridge、Tuwen Xinxi Zhongxin、Zhonglou、Xiaoshiguan、Xueshu Baogao Ting、Meishuguan、Xiansu Lou、Mingda Lou、Fangyin Lou、Shiyan Dalou、Fengyu Qiuguan、Fushu Gaozhong、Dorm 11、Dorm 10、Dorm 9、Dorm 8、Dorm 7、Fengyu Qiuchang、Houqin Fuwu、Daxuesheng Huodong、Qingnian Guangchang、Dorm 5、Dorm 6、Dorm 12、Yanjiusheng 1、Yanjiusheng 2、Yinyue Yishu Guangchang、Youeryuan、Youyongchi、Shinei Yundong、Guoji Jiaoliu、Hongguan、Aoti Ditie Zhan、Xinnian Guangchang、Fangzhou Shetuan Guangchang、Fengyu Qiuchang2、Wangqiuchang2

> 说明：OSM 对江师大瑶湖校区的覆盖是**部分覆盖**（宿舍 1~19 栋、5 个食堂、体育馆群、白鹿会馆、知行楼、惟义楼、天浪楼、超真楼较完整），但**图文信息中心、名达楼、先骕楼、方荫楼、实验大楼、正大坊、静湖、钟楼等尚未绘制**。

## 三、坐标与比例尺误差（关键结论）

以 25 组同名建筑做最小二乘相似变换拟合，最优参数为：

- 缩放 **2.339×**（现有地图相对真实布局被放大约 2.34 倍）
- 旋转 **0.37°**（基本正北，无明显旋转）
- 平移 **(-82.4, -4.8)** 场景单位（≈ -2943 m, -173 m）
- 拟合残差 **RMS 210 m**；对应建筑中心偏差中位数 **158 m**、最大 **682 m**

即使允许整体缩放/旋转/平移，单栋建筑仍有上百米量级的偏差，**说明 map.txt 是示意性（手绘风格）布局，不是按比例尺测绘的结果**。
此外建筑尺寸也普遍偏大：现有地图建筑占地中位数是 OSM 实测的 **5.58 倍**（范围 1.77~20.10）。

另外两处需要注意（`get_buildings.py`）：
1. `CENTER_LON/LAT = 116.0148, 28.6812` 注释为「正大坊」，但该点位于 OSM 校区多边形之外约 1.1 km（西侧），用它做基准会让整个场景偏移；
2. 经度换算用了 `111000 m/度`，未乘 `cos(纬度)`，在本纬度东西向会**偏长约 13.7%**（纬度 28.68° 处 1° 经度实际约 97.7 km）。

## 四、本次产出文件

| 文件 | 内容 |
|---|---|
| `map_osm.txt` | **可直接加载的完整地图**：32 栋 OSM 实测建筑 + 168 段校内道路，米制真实比例，坐标以校区几何中心为原点（RING 0） |
| `osm_campus.json` | 校区建筑与道路的结构化数据（经纬度、面积、层数、轮廓相对坐标） |
| `osm_buildings_campus.csv` | 校区内 32 栋建筑表（含经纬度、类型、层数、面积） |
| `osm_buildings_all.csv` | 取数范围内全部 108 处建筑（含分类：校区内/校区周边/其他） |
| `building_match.csv` | 73 栋现有建筑与 OSM 的逐栋对应关系、面积倍数、中心偏差 |
| `overlay.png` | 三联图：现状 / OSM 实测 / 最佳拟合叠加 |
| `NOTICE.txt` | OSM 数据许可与署名 |

## 五、建议的下一步

1. **想得到“真实校园”**：以 `map_osm.txt` 为新底图（真实比例 + 真实道路），缺失的教学楼群用卫星/航拍影像描摹轮廓，或用高德 POI 批量补名称与坐标；
2. **想保留现有手绘地图**：至少要把比例尺统一（例如约定 1 场景单位 = 1 m 或 10 m），并把 `SCALE` 改成按真实米制换算，否则路径长度、步行时间都没有意义；
3. **数据缺口清单**（建议优先补）：图文信息中心、名达楼、先骕楼、方荫楼、实验大楼、正大坊、静湖、钟楼、校史柱、桃李鼎、音乐艺术广场、瑶湖体育场；
4. **许可**：OSM 数据为 ODbL 1.0，使用/再分发需署名“© OpenStreetMap contributors”，衍生数据需以相同许可发布（详见 `NOTICE.txt`）。

## 六、可选：如何试加载这份真实地图（不改代码）

把 `map_osm.txt` 复制到程序目录并命名为 `map.txt` 即可（建议先备份现有 `map.txt`）。
注意其坐标以校区中心为原点，与现有 map.txt 不是同一坐标框架；如只想预览，可在临时副本上操作。
