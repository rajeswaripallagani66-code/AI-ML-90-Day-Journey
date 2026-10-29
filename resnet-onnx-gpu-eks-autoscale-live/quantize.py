import os
from onnxruntime.quantization import quantize_dynamic, QuantType

input_model = "app/resnet18.onnx"
output_model = "app/resnet18_int8.onnx"

print(f"Input: {os.path.getsize(input_model)/1024/1024:.2f} MB")

quantize_dynamic(
    model_input=input_model,
    model_output=output_model,
    weight_type=QuantType.QInt8
)

print(f"Output: {os.path.getsize(output_model)/1024/1024:.2f} MB")
print("Done!")