import onnxruntime as ort

print("ONNX Runtime version:", ort.__version__)
print("Available Providers:", ort.get_available_providers())

sess = ort.InferenceSession("./onnx_model/glove-hand-person-yolov5x.onnx", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
print("Using Providers:", sess.get_providers())
