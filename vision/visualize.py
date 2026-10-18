import cv2 as cv
import config
#绘制文字
def draw_text_with_background(
        image,
        text,
        position,
        text_color=(255, 255, 255),
        background_color=(30, 30, 30),
):
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    thickness = 1

    text_size,baseline = cv.getTextSize(
        text,
        font,
        font_scale,
        thickness,
    )

    text_width, text_height = text_size
    x,y = position

    x=max(3,x)
    x = min(
        x,
        max(3,image.shape[1]-text_width-6),
    )
    y = max(text_height + 6, y)
    y = min(
        y,
        image.shape[0] - baseline - 4
    )

    cv.rectangle(
        image,
        (x-3,y-text_height-4),
        (x+text_width+3,y+baseline+3),
        background_color,
        -1
    )

    cv.putText(
        image,
        text,
        (x,y),
        font,
        font_scale,
        text_color,
        thickness,
        cv.LINE_AA,
    )
def annotate_image(image, pieces):
    result = image.copy()
    for piece in pieces:
        center = piece["center"]
        x = int(center["x"])
        y = int(center["y"])
        radius = int(piece["radius"])
        color = piece.get("color", "unknown")
        type_name = piece.get("type", "unknown")
        score = piece.get("score", 0)
        priority = piece.get("priority", 0)
        piece_id = piece.get("id", 0)

        draw_color = config.DRAW_COLORS.get(
            color,
            config.DRAW_COLORS["unknown"]
        )

        color_label = config.COLOR_LABELS.get(color, "U")
        type_label = config.TYPE_LABELS.get(type_name, "Unknown")

        cv.circle(
            result,
            (x,y),
            radius,
            draw_color,
            2
        )

        cv.rectangle(
            result,
            (x - radius, y - radius),
            (x + radius, y + radius),
            draw_color,
            1
        )

        cv.circle(
            result,
            (x, y),
            4,
            draw_color,
            -1
        )

        main_label = (
            f"P{priority}"
            f"{color_label}-{type_label}"
            f"S{score}"
        )

        draw_text_with_background(
            result,
            main_label,
            (
                x - radius,
                y - radius-8,
            )
        )

        coordinate_label = (
            f"ID{piece_id}"
            f"({x},{y})"
        )
        draw_text_with_background(
            result,
            coordinate_label,
            (
                x - radius,
                y + radius +20,
            )
        )
    return result

