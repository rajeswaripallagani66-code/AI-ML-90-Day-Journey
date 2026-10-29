import torch
import torchvision
model=torchvision.models.resnet18(weights="IMAGENET1K_V1")
model.eval()
dummy_input=torch.randn(1,3,224,224)
torch.onnx.export(model, dummy_input, "app/resnet18.onnx", input_names=["input"], output_names=["output"], dynamo=False)
print("Saved to app/resnet18.onnx")