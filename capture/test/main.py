import torch
import torch.nn as nn
import numpy as np
import cv2
from torchvision.transforms.functional import to_tensor, to_pil_image
from tqdm import tqdm


# Định nghĩa kiến trúc DnCNN
class DnCNN(nn.Module):
    def __init__(self, channels=3, num_of_layers=17):
        super(DnCNN, self).__init__()
        layers = [nn.Conv2d(channels, 64, kernel_size=3, padding=1), nn.ReLU(inplace=True)]
        for _ in range(num_of_layers - 2):
            layers.append(nn.Conv2d(64, 64, kernel_size=3, padding=1))
            layers.append(nn.BatchNorm2d(64))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Conv2d(64, channels, kernel_size=3, padding=1))
        self.dncnn = nn.Sequential(*layers)

    def forward(self, x):
        return x - self.dncnn(x)

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DnCNN()
model.load_state_dict(torch.load("dncnn.pth", map_location=device))
model.to(device)
model.eval()

# Mở video
cap = cv2.VideoCapture("video_20250505_214118.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(3))
height = int(cap.get(4))
out = cv2.VideoWriter("video_denoised.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

print("Đang xử lý video...")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển frame sang tensor
    input_tensor = to_tensor(frame).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)

    output_np = output.squeeze().clamp(0, 1).cpu().numpy().transpose(1, 2, 0) * 255
    output_np = output_np.astype(np.uint8)

    out.write(output_np)

cap.release()
out.release()
print("✅ Hoàn tất! Video đã được giảm nhiễu: video_denoised.mp4")
