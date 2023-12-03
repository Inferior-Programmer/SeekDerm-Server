import torch
import torchvision.models as models
import torch.nn as nn
from io import BytesIO
from PIL import Image
from torchvision import transforms

import torch.nn.functional as F
import random
import base64
ngpu = 1
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")



def load_checkpoint(checkpoint_path, model, optimizer=None):
    checkpoint = torch.load(checkpoint_path,  map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['network'])
    if optimizer:
        optimizer.load_state_dict(checkpoint['optimizer'])
    return model

index_to_label = {0: 'Acne and Rosacea Photos', 1: 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 2: 'Atopic Dermatitis Photos', 3: 'Bullous Disease Photos', 4: 'Cellulitis Impetigo and other Bacterial Infections', 5: 'Eczema Photos', 6: 'Exanthems and Drug Eruptions', 7: 'Hair Loss Photos Alopecia and other Hair Diseases', 8: 'Herpes HPV and other STDs Photos', 9: 'Light Diseases and Disorders of Pigmentation', 10: 'Lupus and other Connective Tissue diseases', 11: 'Melanoma Skin Cancer Nevi and Moles', 12: 'Nail Fungus and other Nail Disease', 13: 'Poison Ivy Photos and other Contact Dermatitis', 14: 'Psoriasis pictures Lichen Planus and related diseases', 15: 'Scabies Lyme Disease and other Infestations and Bites', 16: 'Seborrheic Keratoses and other Benign Tumors', 17: 'Systemic Disease', 18: 'Tinea Ringworm Candidiasis and other Fungal Infections', 19: 'Urticaria Hives', 20: 'Vascular Tumors', 21: 'Vasculitis Photos', 22: 'Warts Molluscum and other Viral Infections'}


class Discriminator(nn.Module):
  def __init__(self):
    super(Discriminator, self).__init__()
    self.model = models.resnext50_32x4d(pretrained=False)

    for params in self.model.parameters():
      params.requires_grad = True
    self.model.fc = nn.Linear(2048, 23)

  def forward(self,x):
    y = self.model(x)
    return y

def __init__weights(m):
  if isinstance(m, (nn.Linear, nn.Conv2d)):
    nn.init.kaiming_normal_(m.weight, a=0., mode="fan_in", nonlinearity="leaky_relu")


def __weights__init(m):
    if isinstance(m, (nn.Conv2d, nn.Linear)):
        nn.init.normal_(m.weight.data, 0.0, 0.02)


jerModel = Discriminator().to(device)

jerModel = load_checkpoint("models/resNetXt.pt", jerModel)
jerModel.eval()


prediction_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])



def make_prediction_from_base64(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_bytes))
    input_tensor = prediction_transform(image).unsqueeze(0)
    input_tensor = input_tensor.to(device)
    with torch.no_grad():
        output = jerModel(input_tensor)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    predicted_class = torch.argmax(probabilities).item()
    predicted_label = index_to_label[predicted_class]
    return str(predicted_label)





