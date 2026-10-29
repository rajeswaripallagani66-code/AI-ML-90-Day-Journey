import os
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    model_input="app/resnet18.onnx",
    model_output="app/resnet18_int8_uint8.onnx",
    weight_type=QuantType.QUInt8
)
print("Created QUInt8")
