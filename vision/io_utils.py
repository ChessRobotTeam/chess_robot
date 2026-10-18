from pathlib import Path
import csv
import json

import cv2 as cv
import config
#创建目录
def create_output_dir(output_dir=None):
    if output_dir is None:
        output_dir = config.OUTPUT_DIR
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


""""
    将 NumPy 数据类型转换为 Python 原生类型。

    JSON 不能直接保存 np.int32、np.int64 等类型，
    因此保存前需要转换。
"""
def convert_to_builtin(value):
    if isinstance(value,dict):
        return{
            key: convert_to_builtin(item)
            for key,item in value.items()
        }
    if isinstance(value,(list,tuple)):
        return[
            convert_to_builtin(item)
            for item in value
        ]
    if hasattr(value,"item"):
        return value.item()
    return value

def save_image(image,path=None):
    if image is None:
        raise ValueError("要保存的照片不能为空")
    if path is None:
        output_dir = create_output_dir()
        path = output_dir / "result.png"
    else:
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    success = cv.imwrite(
        str(path),
        image
    )

    if not success:
        raise IOError(f"图片保存失败：{path}")

    return path


def save_json(pieces,path=None):
    if path is None:
        output_dir = create_output_dir()
        path = output_dir / "grab_queue.json"
    else:
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
    data = convert_to_builtin(pieces)

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(data,
                  file,
                  ensure_ascii=False,
                  indent = 2
                  )
    return path

def save_csv(pieces,path=None):
    if path is None:
        output_dir = create_output_dir()
        path = output_dir / "grab_queue.csv"
    else:
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
    fields = [
        "priority",
        "id",
        "color",
        "type",
        "cx",
        "cy",
        "radius",
        "confidence",
        "score",
        "distance",
    ]

    with path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )
        writer.writeheader()

        for piece in pieces:
            center = piece.get(
                "center",
                {}
            )

            row = {
                "priority": piece.get("priority",0),
                "id": piece.get("id",0),
                "color": piece.get("color", "unknown"),
                "type": piece.get("type", "unknown"),
                "cx": center.get("x", 0),
                "cy": center.get("y", 0),
                "radius": piece.get("radius", 0),
                "confidence": piece.get("confidence", 0.0),
                "score": piece.get("score", 0),
                "distance": piece.get("distance", 0.0),
            }
            writer.writerow(
                convert_to_builtin(row)
            )
    return path

def save_results(image, pieces, output_dir=None):
    output_dir = create_output_dir(output_dir)

    image_path = save_image(
        image,
        output_dir / "result.png"
    )

    json_path = save_json(
        pieces,
        output_dir / "grab_queue.json"
    )

    csv_path = save_csv(
        pieces,
        output_dir / "grab_queue.csv"
    )

    return {
        "image": image_path,
        "json": json_path,
        "csv": csv_path,
    }