from pathlib import Path

####文件路径
BASE_DIR = Path(__file__).resolve().parent

IMAGE_PATH = BASE_DIR / "exap" / "02.png"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templetes"



#识别模式，视频模式未写
MODE = "image"
CAMERA_INDEX = 0


#基本操作参数
MIN_DISTANCE = 95
MIN_RADIUS = 15
MAX_RADIUS = 80
HOUGH_DP = 1.2
HOUGH_PARAM1 = 100
HOUGH_PARAM2 = 60
BLUR_KERNEL = 3

COLOR_RANGES =\
    {
    "red":
        [
        ((0, 80, 40), (12, 255, 255)),
        ((170, 80, 40), (179, 255, 255)),
        ],
    "green":
        [
        ((35, 50, 30), (95, 255, 255)),
        ],
    }

MIN_COLOR_RATIO = 0.10
INNER_RADIUS_RATIO = 0.65

TYPE_THRESHOLD = 0.04
TEMPLATE_SIZE =(80,80)


####优先级
SCORE_TABLE = \
    {
    "帅": 10,
    "将": 10,
    "车": 8,
    "炮": 7,
    "马": 6,
    "士": 4,
    "仕": 4,
    "象": 4,
    "相": 4,
    "兵": 1,
    "卒": 1,
    "unknown": 0,
    }

GRAB_POINT = None
SHOW_WINDOW = True
SAVE_RESULT = False


# 对应关系
TYPE_NAME_MAP = {
    "red": {
        "shuai": "帅",
        "che": "车",
        "pao": "炮",
        "ma": "马",
        "shi": "仕",
        "xiang": "相",
        "bing": "兵",
    },
    "green": {
        "jiang": "将",
        "che": "车",
        "pao": "炮",
        "ma": "马",
        "shi": "士",
        "xiang": "象",
        "zu": "卒",
    },
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

DRAW_COLORS = {
    "red": (0, 0, 255),
    "green": (0, 200, 0),
    "unknown": (0, 180, 255),
}

TYPE_LABELS = {
    "帅": "Shuai",
    "将": "Jiang",
    "车": "Che",
    "炮": "Pao",
    "马": "Ma",
    "士": "Shi",
    "仕": "Shi",
    "象": "Xiang",
    "相": "Xiang",
    "兵": "Bing",
    "卒": "Zu",
    "unknown": "Unknown",
}


COLOR_LABELS = {
    "red": "R",
    "green": "G",
    "unknown": "U",
}
