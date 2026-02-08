import torch
import torch.nn as nn
import torchvision.models as models

class MorphDetector(nn.Module):
    def __init__(self):
        super(MorphDetector, self).__init__()
        # Load a pre-trained ResNet18 model
        self.resnet = models.resnet18(pretrained=True)
        
        # Replace the final layer to output 1 value (Real vs Morphed)
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_features, 1)

    def forward(self, x):
        return self.resnet(x)

def load_model(path='morph_model.pth'):
    model = MorphDetector()
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()
    return model