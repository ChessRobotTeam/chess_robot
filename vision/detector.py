import cv2
import numpy as np
import config


"""
棋子检测，霍夫圆变换
   返回：
   [
       {
           "id": 1,
           "center": {"x": 320, "y": 180},
           "radius": 34
       }
   ]
   """
def detect_pieces(image):
    if image is None:
        return []


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    blue_size = config.BLUR_KERNEL
    if blue_size %2 == 0:
        blue_size += 1

    gray = cv2.GaussianBlur(
        gray,
        (blue_size, blue_size),
        0)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp= config.HOUGH_DP,
        minDist = config.MIN_DISTANCE,
        param1=config.HOUGH_PARAM1,
        param2=config.HOUGH_PARAM2,
        minRadius=config.MIN_RADIUS,
        maxRadius=config.MAX_RADIUS,
    )

    if circles is None:
        return []

    circles = np.round(circles[0]).astype(int)
    circles = sorted(circles, key = lambda item:(item[1],item[0])
                     )
    pieces = []

    for index,circle in enumerate(circles,start=1):
        x,y,radius = circle

        piece = \
        {
            "id": index,
            "center":
                {
                    "x": x, "y": y
                },
            "radius":int(radius)

        }

        pieces.append(piece)
    return pieces



"""
    按 HSV 范围生成颜色掩膜。

    返回：
    {
        "red": 红色掩膜,
        "green": 绿色掩膜
    }
    考虑补充一个去噪
 """
def build_color_masks(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    masks = {}
    for color,ranges in config.COLOR_RANGES.items():
        mask = np.zeros(
            hsv.shape[:2],
            dtype=np.uint8,
        )

        for low,high in ranges:
            current_mask = cv2.inRange(
                hsv,
                np.array(low,dtype =np.uint8),
                np.array(high,dtype =np.uint8),
            )
            mask = cv2.bitwise_or(mask,current_mask)

        masks[color] = mask
    return masks


"""
返回：
    color, red_ratio, green_ratio
"""
def classify_color(color_masks,center,radius):
    if "red" not in color_masks or "green" not in color_masks:
        return "unknown",0.0,0.0

    red_mask = color_masks["red"]
    green_mask = color_masks["green"]

    x,y = center

    inner_mask = np.zeros(
        red_mask.shape,
        dtype=np.uint8,
    )
    inner_radius = max(2,int(radius *config.INNER_RADIUS_RATIO))

    cv2.circle(
        inner_mask,
        (x,y),
        inner_radius,
        255,
        -1
    )

    valid_pixels = inner_mask >0
    total_pixels = int (np.count_nonzero(valid_pixels))

    if total_pixels == 0:
        return "unknown",0.0,0.0

    red_pixels = int(
        np.count_nonzero(red_mask[valid_pixels])
    )
    green_pixels = int(
        np.count_nonzero(green_mask[valid_pixels])
    )

    red_ratio = red_pixels / total_pixels
    green_ratio = green_pixels / total_pixels

    if max(red_ratio,green_ratio) < config.MIN_COLOR_RATIO:
        color = "unknown"
    elif red_ratio >= green_ratio:
        color = "red"
    else:
        color = "green"
    return color,red_ratio,green_ratio


"""
   补充颜色信息
"""
def classify_piece_colors(pieces,color_masks):
    for piece in pieces:
        center = piece["center"]
        x = center["x"]
        y = center["y"]

        color,red_ratio,green_ratio = classify_color(
            color_masks,
            (x,y),
            piece["radius"]
        )

        piece["color"] = color
        piece["red_ratio"] = red_ratio
        piece["green_ratio"] = green_ratio
    return pieces



