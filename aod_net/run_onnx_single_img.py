import onnxruntime as ort
import numpy as np
import cv2

def create_onnx_session(model_path):
    providers = [
        ('CUDAExecutionProvider', {
            'device_id': 0,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'gpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB
            'cudnn_conv_algo_search': 'EXHAUSTIVE',
            'do_copy_in_default_stream': True,
        }),
        'CPUExecutionProvider'
    ]
    session = ort.InferenceSession(model_path, providers=providers)
    return session

# 1. 加载 ONNX 模型
# session = ort.InferenceSession("dehaze_net_dynamic.onnx", providers=["CPUExecutionProvider"])

session = create_onnx_session("dehaze_net_dynamic.onnx")


# 2. 读取并预处理图像
img_path = "./img.png"  # 替换为你的图片路径
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR 转 RGB
img_input = img.astype(np.float32) / 255.0  # 归一化到 [0,1]

# 3. 转为 NCHW 格式 (1, 3, H, W)
img_input = np.transpose(img_input, (2, 0, 1))  # HWC → CHW
img_input = np.expand_dims(img_input, axis=0)  # CHW → NCHW

# 4. 运行 ONNX 推理
outputs = session.run(
    output_names=["output"],
    input_feed={"input": img_input}
)
output = outputs[0]  # (1, 3, H, W)

# 5. 后处理并保存
output = np.squeeze(output, axis=0)  # 去掉 batch 维度
output = np.clip(output, 0, 1)
output = (output * 255).astype(np.uint8)
output = np.transpose(output, (1, 2, 0))  # CHW → HWC
output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
cv2.imwrite("output.jpg", output)

print("✅ 输出图像已保存为 output.jpg")
