from pathlib import Path

import cv2 as cv
import numpy as np

import config

def preprocess_image(image):
    """
    转换成统一尺寸的二值图。
    """
    if image is None or image.size == 0:
        return None

    if image.ndim == 3:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    gray = cv.GaussianBlur(gray, (3, 3), 0)
    gray = cv.resize(gray, config.TEMPLATE_SIZE)

    _, binary = cv.threshold(
        gray,
        0,
        255,
        cv.THRESH_BINARY_INV + cv.THRESH_OTSU
    )

    return binary


def load_templates(template_dir=None):
    """
    加载模板。

    返回格式：
    {
        "red": {"车": 模板图},
        "green": {"将": 模板图}
    }
    """
    root = Path(template_dir or config.TEMPLATES_DIR)
    templates = {
        "red": {},
        "green": {},
    }

    for color in templates:
        color_dir = root / color

        if not color_dir.is_dir():
            print(f"模板目录不存在：{color_dir}")
            continue

        for path in sorted(color_dir.iterdir()):
            if path.suffix.lower() not in config.IMAGE_EXTENSIONS:
                continue
            type_name = config.TYPE_NAME_MAP[color].get(path.stem.lower())

            if type_name is None:
                print(f"无法识别模板文件名，已跳过：{path.name}")
                continue

            image = cv.imread(str(path))

            if image is None:
                print(f"模板读取失败：{path}")
                continue

            templates[color][type_name] = preprocess_image(image)

    return templates


def crop_piece(image, center, radius):
    """
    截取棋子中间区域。
    """
    x, y = center
    half_size = max(2, int(radius * 0.65))

    x1 = max(0, x - half_size)
    y1 = max(0, y - half_size)
    x2 = min(image.shape[1], x + half_size)
    y2 = min(image.shape[0], y + half_size)

    return image[y1:y2, x1:x2]


def compare_images(query, template):
    """
    使用模板匹配计算相似度
    """
    if query is None or template is None:
        return 0.0

    result = cv.matchTemplate(
        query,
        template,
        cv.TM_CCOEFF_NORMED
    )

    score = float(result[0, 0])

    if not np.isfinite(score):
        return 0.0

    return max(0.0, min(1.0, score))


def classify_type(image, piece, templates):
    """
    识别单个棋子的类别。

    返回：
        类别名称、匹配置信度
    """
    color = piece.get("color", "unknown")
    color_templates = templates.get(color, {})

    if not color_templates:
        return "unknown", 0.0

    center = piece["center"]
    crop = crop_piece(
        image,
        (center["x"], center["y"]),
        piece["radius"]
    )

    query = preprocess_image(crop)

    if query is None:
        return "unknown", 0.0

    best_type = "unknown"
    best_score = 0.0

    for type_name, template in color_templates.items():
        score = compare_images(query, template)

        if score > best_score:
            best_type = type_name
            best_score = score

    if best_score < config.TYPE_THRESHOLD:
        return "unknown", best_score

    return best_type, best_score


def classify_pieces(image, pieces, templates):
    """
    为每个棋子补充 种类 和 置信度
    """
    for piece in pieces:
        type_name, confidence = classify_type(
            image,
            piece,
            templates
        )

        piece["type"] = type_name
        piece["confidence"] = round(confidence, 4)

    return pieces



