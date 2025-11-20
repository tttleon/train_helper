from paddleocr import TextDetection
import cv2
import numpy as np
import os


def point_in_roi(point, roi_polygon):
    """判断点是否在 ROI 区域内"""
    return cv2.pointPolygonTest(roi_polygon, (point[0], point[1]), False) >= 0

def polys_in_roi(dt_polys, roi_polygon):
    """判断一组点是否全部在 ROI 内"""
    return all(point_in_roi(pt, roi_polygon) for pt in dt_polys)

def process_output(output, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    for res in output:
        # print(f'res={res}')
        input_path = res["input_path"]
        dt_polys = res["dt_polys"]  # 多组点

        # 过滤：如果某组有点不在ROI，则剔除
        valid_polys = [poly for poly in dt_polys if polys_in_roi(poly, ROI) or polys_in_roi(poly, ROI_2)]

        if not valid_polys:
            print(f'{input_path}没有符合ROI的点，跳过')
            continue  #

        # 计算剩余所有点的最大外接矩形
        all_points = np.vstack(valid_polys)
        # print(f'all_points={all_points}')
        all_points = np.array(all_points, dtype=np.int32)
        x, y, w, h = cv2.boundingRect(all_points)

        # 中心点
        cx, cy = x + w // 2, y + h // 2


        half = crop_size // 2

        # 读取原图
        img = cv2.imread(input_path)
        if img is None:
            continue

        H, W = img.shape[:2]

        # 确保裁剪区域不越界
        x1 = max(0, cx - half)
        y1 = max(0, cy - half)
        x2 = min(W, cx + half)
        y2 = min(H, cy + half)

        crop = img[y1:y2, x1:x2]

        # 如果不够 640*640，可以考虑 padding
        if crop.shape[0] != crop_size or crop.shape[1] != crop_size:
            padded = np.zeros((crop_size, crop_size, 3), dtype=np.uint8)
            padded[:crop.shape[0], :crop.shape[1]] = crop
            crop = padded

        # 保存
        filename = os.path.basename(input_path)
        save_path = os.path.join(save_dir, filename)
        cv2.imwrite(save_path, crop)

if __name__ == "__main__":
    # os.chdir(r'E:\myJobTwo\project\PaddleOCR-3.2.0')

    model = TextDetection(model_name="PP-OCRv5_server_det",
                          model_dir='E:\myJobTwo\project\PaddleOCR\PP-OCRv5_server_det_infer')
    output = model.predict(r"E:\myJobTwo\project\train-helper\video\output_images",
                           batch_size=1,
                           limit_side_len=640,
                           limit_type='min'
                           )
    for res in output:
        res.save_to_img(save_path="./server_TextDetection_output/")



    # ROI 多边形
    ROI = np.array([[63, 129], [1913, 397], [1857, 810], [4, 542]])
    ROI_2 = np.array([[7,616],[1730,4],[1914,161],[11,1064]])
    # 裁剪区域大小
    crop_size = 320
    # 删除旧目录
    if os.path.exists("crop_320_save_dir"):
        import shutil
        shutil.rmtree("crop_320_save_dir")

    process_output(output, "crop_320_save_dir")

    # 打印crop_320_save_dir中文件数量
    print(f'crop_320_save_dir中文件数量={len(os.listdir("crop_320_save_dir"))}')