#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江西师范大学瑶湖校区 3D校园地图 - 建筑坐标采集脚本
使用高德地图API批量获取建筑经纬度，并转换为3D场景坐标
"""

import requests
import json
import time
import math
import random

# ============================================================
# 配置区域（请修改）
# ============================================================

# 请在这里填入您的高德API Key
AMAP_KEY = "YOUR_AMAP_KEY"  # 👈 替换成你的高德 Key

# 校区中心基准点（正大坊的经纬度）
# 如果不确定，运行脚本后查看输出，根据实际情况调整
CENTER_LON = 116.0148   # 正大坊经度
CENTER_LAT = 28.6812    # 正大坊纬度

# 3D场景缩放系数
# 值越大，地图范围越大。建议范围 0.02 ~ 0.04
SCALE = 0.028


# ============================================================
# 建筑清单（共40+个，包含全部15栋学生宿舍）
# ============================================================

buildings = [
    # ===== 核心地标 =====
    "江西师范大学瑶湖校区正大坊",
    "江西师范大学瑶湖校区正大广场",
    "江西师范大学瑶湖校区校史柱",
    "江西师范大学瑶湖校区桃李鼎",
    "江西师范大学瑶湖校区校训墙",
    
    # ===== 教学楼群（5个） =====
    "江西师范大学瑶湖校区惟义楼",
    "江西师范大学瑶湖校区名达楼",
    "江西师范大学瑶湖校区先骕楼",
    "江西师范大学瑶湖校区方荫楼",
    "江西师范大学瑶湖校区实验大楼",
    
    # ===== 学院楼（3个） =====
    "江西师范大学瑶湖校区天浪楼",
    "江西师范大学瑶湖校区超真楼",
    "江西师范大学瑶湖校区洁琼楼",
    
    # ===== 生活服务 =====
    "江西师范大学瑶湖校区图书馆",
    "江西师范大学瑶湖校区白鹿会馆",
    "江西师范大学瑶湖校区学生食堂",
    "江西师范大学瑶湖校区青年文化广场",
    
    # ===== 运动场馆 =====
    "江西师范大学瑶湖校区体育场",
    "江西师范大学瑶湖校区体育馆",
    "江西师范大学瑶湖校区风雨球场",
    "江西师范大学瑶湖校区运动馆",
    
    # ===== 学生宿舍（15栋，全部列出） =====
    "江西师范大学瑶湖校区学生公寓1栋",
    "江西师范大学瑶湖校区学生公寓2栋",
    "江西师范大学瑶湖校区学生公寓3栋",
    "江西师范大学瑶湖校区学生公寓4栋",
    "江西师范大学瑶湖校区学生公寓5栋",
    "江西师范大学瑶湖校区学生公寓6栋",
    "江西师范大学瑶湖校区学生公寓7栋",
    "江西师范大学瑶湖校区学生公寓8栋",
    "江西师范大学瑶湖校区学生公寓9栋",
    "江西师范大学瑶湖校区学生公寓10栋",
    "江西师范大学瑶湖校区学生公寓11栋",
    "江西师范大学瑶湖校区学生公寓12栋",
    "江西师范大学瑶湖校区学生公寓13栋",
    "江西师范大学瑶湖校区学生公寓14栋",
    "江西师范大学瑶湖校区学生公寓15栋",
]

# ============================================================
# 手动补充的建筑（高德API查不到的）
# ============================================================

# 静湖：API无法精确返回湖泊坐标，需要手动标注
# 格式: (名称, 场景x, 场景z, 宽度, 高度, 深度, R, G, B)
manual_buildings = [
    # 名称,       x,    z,   w,   h,   d,   R,    G,    B
    ("静湖",      2.0,  1.5,  5.0, 0.2, 5.0, 0.0,  0.5,  0.8),
]


# ============================================================
# 高德API地理编码
# ============================================================

def get_location(name):
    """调用高德API获取地址的经纬度"""
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": name,
        "key": AMAP_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data["status"] == "1" and data["geocodes"]:
            loc = data["geocodes"][0]["location"]
            lon, lat = map(float, loc.split(","))
            return lon, lat
        else:
            return None, None
    except Exception as e:
        return None, None


def to_scene_coord(lon, lat):
    """经纬度 → 3D场景坐标"""
    dx = (lon - CENTER_LON) * 111000 * SCALE
    dz = (lat - CENTER_LAT) * 111000 * SCALE
    return dx, dz


# ============================================================
# 生成C语言数组
# ============================================================

def generate_c_array(building_data, manual_data):
    """生成C语言的campusData数组"""
    lines = []
    lines.append("Landmark campusData[] = {")
    
    id_counter = 1
    
    # 处理API获取的建筑
    for name, lon, lat, dx, dz in building_data:
        # 根据名称设置不同大小和颜色
        if "图书馆" in name:
            w, h, d = 8, 6, 5
            r, g, b = 0.9, 0.2, 0.2
        elif "体育场" in name or "运动馆" in name:
            w, h, d = 7, 1, 5
            r, g, b = 0.2, 0.8, 0.3
        elif "学生食堂" in name:
            w, h, d = 5, 3, 4
            r, g, b = 0.9, 0.6, 0.1
        elif "学生公寓" in name or "宿舍" in name:
            w, h, d = 4, 3, 6
            r, g, b = 0.6, 0.7, 0.8
        elif "正大坊" in name:
            w, h, d = 3, 2, 3
            r, g, b = 1.0, 0.8, 0.2
        elif "实验大楼" in name:
            w, h, d = 5, 5, 4
            r, g, b = 0.8, 0.6, 0.2
        elif "图书馆" in name:
            w, h, d = 8, 6, 5
            r, g, b = 0.9, 0.2, 0.2
        elif "惟义楼" in name or "名达楼" in name or "先骕楼" in name or "方荫楼" in name:
            w, h, d = 6, 4, 4
            # 不同教学楼不同颜色
            if "惟义楼" in name:
                r, g, b = 0.2, 0.6, 0.9
            elif "名达楼" in name:
                r, g, b = 0.1, 0.8, 0.4
            elif "先骕楼" in name:
                r, g, b = 0.8, 0.4, 0.1
            elif "方荫楼" in name:
                r, g, b = 0.4, 0.3, 0.8
            else:
                r, g, b = 0.3, 0.6, 0.9
        elif "天浪楼" in name or "超真楼" in name or "洁琼楼" in name:
            w, h, d = 4, 4, 4
            if "天浪楼" in name:
                r, g, b = 0.9, 0.5, 0.5
            elif "超真楼" in name:
                r, g, b = 0.5, 0.3, 0.7
            else:
                r, g, b = 0.3, 0.7, 0.6
        else:
            w, h, d = 5, 4, 4
            r, g, b = random.uniform(0.4, 0.9), random.uniform(0.4, 0.9), random.uniform(0.4, 0.9)
        
        line = f'    {{"{name}", {id_counter}, {{{dx:.1f}, 0, {dz:.1f}}}, {{{r:.2f}, {g:.2f}, {b:.2f}}}, {w}, {h}, {d}}},'
        lines.append(line)
        id_counter += 1
    
    # 处理手动补充的建筑（静湖等）
    for name, dx, dz, w, h, d, r, g, b in manual_data:
        line = f'    {{"{name}", {id_counter}, {{{dx:.1f}, 0, {dz:.1f}}}, {{{r:.2f}, {g:.2f}, {b:.2f}}}, {w}, {h}, {d}}},'
        lines.append(line)
        id_counter += 1
    
    lines.append("};")
    lines.append(f"#define LANDMARK_COUNT {len(building_data) + len(manual_data)}")
    
    return "\n".join(lines)


# ============================================================
# 主程序
# ============================================================

def main():
    print("=" * 70)
    print("江西师范大学瑶湖校区 - 建筑坐标批量采集")
    print("=" * 70)
    print(f"基准点: 正大坊 ({CENTER_LON}, {CENTER_LAT})")
    print(f"缩放系数: {SCALE}")
    print(f"建筑总数: {len(buildings)} 个 (API获取) + {len(manual_buildings)} 个 (手动补充)")
    print("=" * 70)
    print()
    
    results = []
    failed = []
    
    print("📡 正在调用高德API获取建筑坐标...\n")
    
    for idx, name in enumerate(buildings, 1):
        print(f"[{idx:>2}/{len(buildings)}] {name}", end=" ... ")
        lon, lat = get_location(name)
        
        if lon is not None:
            dx, dz = to_scene_coord(lon, lat)
            results.append((name, lon, lat, dx, dz))
            print(f"✅ ({lon:.6f}, {lat:.6f}) → ({dx:.1f}, 0, {dz:.1f})")
        else:
            failed.append(name)
            print(f"❌ 未找到")
        
        time.sleep(0.15)
    
    print()
    print("=" * 70)
    print(f"📊 统计: 成功 {len(results)} 个, 失败 {len(failed)} 个")
    
    if failed:
        print("\n⚠️ 以下建筑未找到，建议手动补充:")
        for name in failed:
            print(f"  - {name}")
    
    print()
    print("=" * 70)
    print("📋 生成的 C 语言 campusData 数组:")
    print("=" * 70)
    print()
    
    c_array = generate_c_array(results, manual_buildings)
    print(c_array)
    
    print()
    print("=" * 70)
    print("✅ 完成！复制上面的数组替换 main.c 中的 campusData 即可。")
    print("=" * 70)
    
    # 输出失败列表到文件
    if failed:
        with open("failed_buildings.txt", "w", encoding="utf-8") as f:
            f.write("以下建筑高德API未找到，需要手动补充坐标:\n")
            for name in failed:
                f.write(f"{name}\n")
        print(f"\n💡 失败列表已保存到 failed_buildings.txt")


if __name__ == "__main__":
    main()