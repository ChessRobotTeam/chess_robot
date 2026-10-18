from pathlib import Path

import cv2 as cv

import config
from classifier import (
    classify_pieces,
    load_templates,
)
from detector import (
    build_color_masks,
    classify_piece_colors,
    detect_pieces,
)
from io_utils import save_results
from priority import (
    assign_scores,
    build_grab_queue,
)
from visualize import annotate_image


def process_frame(frame, templates):
    """
    返回：
        result：标注后的图片
        pieces：按抓取优先级排序的棋子列表
    """
    #检测棋子
    pieces = detect_pieces(frame)

    if not pieces:
        return frame.copy(), []

    #掩膜
    color_masks = build_color_masks(frame)

    #判断颜色
    classify_piece_colors(
        pieces,
        color_masks
    )

    #识别棋子类别
    classify_pieces(
        frame,
        pieces,
        templates
    )

    #映射棋子分数
    assign_scores(pieces)

    #计算距离并生成抓取队列
    pieces = build_grab_queue(
        pieces,
        image_size=(
            frame.shape[1],
            frame.shape[0]
        ),
        grab_point=config.GRAB_POINT
    )

    #在图片上绘制结果
    result = annotate_image(
        frame,
        pieces
    )

    return result, pieces


def print_grab_queue(pieces):
    """
    在终端打印抓取队列。
    """
    if not pieces:
        print("没有检测到棋子")
        return

    print("\n抓取队列：")

    for piece in pieces:
        center = piece["center"]

        print(
            f"P{piece['priority']} "
            f"ID={piece['id']} "
            f"颜色={piece['color']} "
            f"类别={piece['type']} "
            f"分数={piece['score']} "
            f"置信度={piece['confidence']:.3f} "
            f"距离={piece['distance']:.2f} "
            f"中心=({center['x']}, {center['y']})"
        )


def print_saved_paths(saved_paths):
    """
    打印文件保存位置。
    """
    print("\n处理结果已保存：")
    print("结果图片：", saved_paths["image"])
    print("JSON：", saved_paths["json"])
    print("CSV：", saved_paths["csv"])


def run_image():
    """
    处理单张图片。
    """
    image = cv.imread(
        str(config.IMAGE_PATH)
    )

    if image is None:
        print(
            "图片读取失败，请检查路径：",
            config.IMAGE_PATH
        )
        return

    templates = load_templates()

    result, pieces = process_frame(
        image,
        templates
    )

    print("检测到棋子数量：", len(pieces))
    print_grab_queue(pieces)

    if config.SAVE_RESULT:
        saved_paths = save_results(
            result,
            pieces
        )

        print_saved_paths(saved_paths)

    if config.SHOW_WINDOW:
        window_name = "结果显示"
        cv.namedWindow(
            window_name,
            cv.WINDOW_NORMAL
        )
        cv.resizeWindow(
            window_name,
            1000,
            700
        )

        cv.imshow(
            window_name,
            result
        )

        cv.waitKey(0)
        cv.destroyAllWindows()




def main():
    """
    根据 config.MODE 选择运行模式。
    """
    mode = config.MODE.lower()

    if mode == "image":
        run_image()

#暂时仅实现照片
    else:
        print("不支持的运行模式：", config.MODE)
        print("可选模式：image、video、camera")


if __name__ == "__main__":
    main()