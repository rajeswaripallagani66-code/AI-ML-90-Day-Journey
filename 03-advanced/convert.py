import torch
import torchvision
model=torchvision.models.resnet18(weights="IMAGENET1K_V1")
model.eval()
dummy_input=torch.randn(1,3,224,224)
torch.onnx.export(model,dummy_input,"resnet18.onnx",input_names=["input"],output_names=["output"])
print("Saved resnet18>onnx FP32-4MB")