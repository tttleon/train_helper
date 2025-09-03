import onnxruntime as ort
import numpy as np
import cv2

def create_onnx_session(model_path):
    providers = [
        ('CUDAExecutionProvider', {
            'device_id': 0,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'gpu_mem_limit': 2 * 1024 * 1024 * 1024,
            'cudnn_conv_algo_search': 'EXHAUSTIVE',
            'do_copy_in_default_stream': True,
        }),
        'CPUExecutionProvider'
    ]
    return ort.InferenceSession(model_path, providers=providers)

def preprocess_frame(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    x = rgb.astype(np.float32) / 255.0
    x = np.transpose(x, (2, 0, 1))  # HWC → CHW
    x = np.expand_dims(x, axis=0)  # CHW → NCHW
    return x

def postprocess_output(output):
    x = np.squeeze(output, axis=0)
    x = np.clip(x, 0, 1)
    x = (x * 255).astype(np.uint8)
    x = np.transpose(x, (1, 2, 0))  # CHW → HWC
    return cv2.cvtColor(x, cv2.COLOR_RGB2BGR)

# 初始化模型
session = create_onnx_session("dehaze_net_dynamic.onnx")

# 视频输入 & 输出配置
input_video_path = "./video/3968565-hd_1920_1080_24fps.mp4"
output_video_path = "combined_output.mp4"

cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 上下拼接后，高度 ×2，宽度不变
combined_height = height * 2
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, combined_height))

frame_idx = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    input_tensor = preprocess_frame(frame)
    output_tensor = session.run(["output"], {"input": input_tensor})[0]
    dehazed_frame = postprocess_output(output_tensor)

    # 拼接：原图在上，去雾图在下
    combined_frame = np.vstack((frame, dehazed_frame))

    # 写入视频文件
    out_writer.write(combined_frame)

    # 实时预览
    # cv2.imshow("Original (Top) + Dehazed (Bottom)", combined_frame)
    # 实时预览缩放（例如缩小一半）
    preview_frame = cv2.resize(combined_frame, (width // 2, combined_height // 2))
    cv2.imshow("Original (Top) + Dehazed (Bottom)", preview_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_idx += 1
    if frame_idx % 10 == 0:
        print(f"处理帧数: {frame_idx}")

cap.release()
out_writer.release()
cv2.destroyAllWindows()
print("✅ 完成，视频已保存为:", output_video_path)
