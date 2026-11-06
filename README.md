# 师大瑶湖 · 校园导航

基于 **C + OpenGL (freeglut)** 的三维校园导航程序，配套一份同源网页版。
覆盖校园 **76 栋建筑、677 个节点（76 个地点 + 601 个路网节点）、842 条道路**，
支持最短路径、最少换乘、最小生成树与图遍历演示。

![三维校园地图](docs/screenshots/map.png)
![路线面板](docs/screenshots/route.png)
![最少换乘（BFS）](docs/screenshots/transfer.png)
![Prim 最小生成树](docs/screenshots/algo.png)

---

## 功能

| 模块 | 说明 |
| --- | --- |
| **三维地图** | 建筑按真实轮廓多边形绘制，可鼠标旋转 / 缩放 / 平移；道路按等级分色 |
| **最短路径** | Dijkstra，按步行距离计算，支持起终点任意选择，路径高亮 |
| **最少换乘** | 在换乘代价建模上求解，用于"少走岔路、少拐弯"的路线推荐 |
| **最小生成树** | Prim，展示把全校路网连通的最小代价方案 |
| **遍历演示** | 深度优先（DFS）/ 广度优先（BFS）逐步高亮访问顺序 |
| **道路报告** | 手写快速排序按权重排序边，输出路网统计 |
| **数据面板** | 实时显示节点数、边数、选中建筑信息与算法耗时 |

## 两种版本

- **桌面版**：`main.c` 单文件，C + freeglut/OpenGL，Windows 下运行
- **网页版**：`web/index.html`，浏览器直接打开即可，无需安装（数据在 `web/campus_data.js`）

## 运行

**直接跑（免编译）**

```
campus.exe          需要同目录下的 libfreeglut.dll
```

> ⚠️ 仓库里的 `campus.exe` 构建于 **2026-10-25**，之后 `main.c` 仍有改动，
> 因此二进制可能落后于源码。想要最新行为请按下面的命令自行编译；
> 网页版 `web/index.html` 的数据是最新的（2026-11-06）。

**自己编译（MinGW-w64 示例）**

```bash
gcc main.c -o campus.exe -O2 -mwindows \
    -lfreeglut -lopengl32 -lglu32 -lwinmm
```

> 需要 freeglut 开发包（头文件 + `libfreeglut.a`）。用 MSVC 时同样需要 freeglut 的 lib，
> 并在项目属性里链接 `opengl32.lib glu32.lib winmm.lib`。

## 数据文件

| 文件 | 内容 |
| --- | --- |
| `map.txt` | `VERSION 1` / `BUILDINGS 76`，每行一栋建筑：名称、坐标、高度、RGB、顶点数与多边形顶点 |
| `road_data.txt` | `VERSION 23` / 节点数 677（76 个地点 + 601 个路网节点）、842 条边；先列节点（id、名称、坐标），再列边与权重 |
| `map_bak1.txt` / `map_bak2.txt` | 备用地图（程序内可切换） |
| `osm_export/` | 原始测绘数据与比对报告（见下方署名） |

## 测绘数据来源（重要）

`osm_export/` 与地图文件中的建筑轮廓来自 **OpenStreetMap**，遵循
**Open Database License (ODbL) 1.0**：

- 必须署名：**© OpenStreetMap contributors**（https://www.openstreetmap.org/copyright）
- 若基于该数据发布衍生数据库，需以相同许可（ODbL）开放

取数时间 2026-09-25，方式为 Overpass API。详见 `osm_export/NOTICE.txt`。

> `osm_export/` 里的三份报告（对比 / 补全 / 定位）是**当时的数据处理记录**，
> 反映的是 73 栋建筑的中期状态；此后地图已补全到 76 栋，报告内容未再更新，仅作来源凭证保留。

> 换言之：**代码**你可以自行决定许可；但**地图数据**受 ODbL 约束，转载或再分发时要保留署名。

## 目录结构

```
main.c                桌面版全部源码（地图渲染 + 图算法 + 交互）
campus.exe            预编译可执行文件（Windows x64）
libfreeglut.dll       freeglut 运行库
map.txt               建筑数据
road_data.txt         路网数据（节点 + 边）
get_buildings.py      从 OSM 导出数据生成 map.txt 的脚本
web/                  网页版（index.html + campus_data.js + 界面截图）
osm_export/           OSM 原始数据、比对报告与许可说明
docs/screenshots/     README 用截图
```
