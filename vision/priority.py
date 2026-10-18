import config
import math
"""
    根据类别返回对应分数
    未识别返回0
"""
def assign_score(type_name):
    return config.SCORE_TABLE.get(type_name, 0)
"""
给棋子添加score字段
"""
def assign_scores(pieces):
    for piece in pieces:
        type_name = piece.get("type","unknown")
        piece["score"] = assign_score(type_name)
    return pieces
"""
    测算中信到参考点的距离
"""
def calculate_distance(piece,grab_point):
    center = piece["center"]
    x= center["x"]
    y= center["y"]

    grab_x,grab_y = grab_point
    distance = math.hypot(x - grab_x,y - grab_y)
    return distance
#按照分数——置信度——距离排序
def build_grab_queue(pieces,image_size,grab_point = None):
    width,height = image_size
    #默认图像中心
    if grab_point is None:
        grab_point = (
            width//2,
            height//2
        )
    for piece in pieces:
        distance = calculate_distance(piece,grab_point)
        piece["distance"] = round(distance,2)
    #排序
    pieces.sort(
        key=lambda piece:(
            -piece.get("score",0),
            -piece.get("confidence",0.0),
            piece["distance"]))
    for priority,piece in enumerate(pieces,start=1):
        piece["priority"] = priority
    return pieces