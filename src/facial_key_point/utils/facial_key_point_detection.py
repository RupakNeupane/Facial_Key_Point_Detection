import numpy as np
import torch
from torchvision import transforms

class FacialKeyPointDetection:
    def __init__(self) -> None:
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load('dump/version_1/model.pth',map_location=self.device)
        self.normalize = transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )

    def predict(self, image):
        img, img_disp = self.preprocess(image)
        kps = self.model (img[None]).flatten().detach().cpu()
        kp = self.postprocess(image, kps)
        return img_disp, kp

    def preprocess(self, img):
        img = img.resize((224, 224))
        img = img_disp = np.asarray(img) / 255
        img = torch.tensor(img).permute(2, 0 ,1)
        img = self.normalize(img)
        img = img.float()
        return img.to(self.device), img_disp

    def postprocess(self, image, kps):
        width, height = image. size
        kp_x, kp_y = kps[:68] * width, kps [68:] * height
        return kp_x, kp_y
