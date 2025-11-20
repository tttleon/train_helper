import onnx

def print_onnx_node_types(model_path):
    """
    加载ONNX模型并打印每一层（节点）的输入和输出数据类型，包括initializer（权重/偏置）。
    """
    try:
        model = onnx.load(model_path)
        graph = model.graph

        # 构建 initializer 字典，方便快速查 dtype
        initializer_dict = {init.name: init for init in graph.initializer}

        print(f"ONNX模型: {model_path}")
        print("-" * 60)

        # 打印模型输入
        print("模型输入 (Model Inputs):")
        for input_tensor in graph.input:
            name = input_tensor.name
            if name in initializer_dict:
                dtype = onnx.helper.tensor_dtype_to_string(initializer_dict[name].data_type)
                print(f"  - 名称: {name}, 数据类型: {dtype} (Initializer)")
            else:
                dtype = onnx.helper.tensor_dtype_to_string(input_tensor.type.tensor_type.elem_type)
                print(f"  - 名称: {name}, 数据类型: {dtype}")
        print("-" * 60)

        # 遍历每个节点
        print("模型节点 (Nodes):")
        for i, node in enumerate(graph.node):
            print(f"节点 {i}: {node.name} (Op: {node.op_type})")

            # 输入
            print("  输入:")
            for input_name in node.input:
                if input_name in initializer_dict:
                    dtype = onnx.helper.tensor_dtype_to_string(initializer_dict[input_name].data_type)
                    print(f"    - 名称: {input_name}, 数据类型: {dtype} (Initializer)")
                else:
                    # 从 value_info 查找
                    type_info = next((vi.type.tensor_type for vi in graph.value_info if vi.name == input_name), None)
                    if type_info:
                        dtype = onnx.helper.tensor_dtype_to_string(type_info.elem_type)
                        print(f"    - 名称: {input_name}, 数据类型: {dtype}")
                    else:
                        print(f"    - 名称: {input_name}, 数据类型: 无法确定")

            # 输出
            print("  输出:")
            for output_name in node.output:
                type_info = next((vi.type.tensor_type for vi in graph.value_info if vi.name == output_name), None)
                if not type_info:
                    # 输出可能在 graph.output 中
                    type_info = next((go.type.tensor_type for go in graph.output if go.name == output_name), None)
                if type_info:
                    dtype = onnx.helper.tensor_dtype_to_string(type_info.elem_type)
                    print(f"    - 名称: {output_name}, 数据类型: {dtype}")
                else:
                    print(f"    - 名称: {output_name}, 数据类型: 无法确定")
            print()

        print("-" * 60)
        # 打印模型输出
        print("模型输出 (Model Outputs):")
        for output_tensor in graph.output:
            dtype = onnx.helper.tensor_dtype_to_string(output_tensor.type.tensor_type.elem_type)
            print(f"  - 名称: {output_tensor.name}, 数据类型: {dtype}")

    except Exception as e:
        print(f"加载或解析模型时出错: {e}")


if __name__ == "__main__":
    # 替换为你的模型路径
    print_onnx_node_types(r'E:\myJobTwo\project\yolov5-master\yolov5s.onnx')
