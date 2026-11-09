from torchvision import transforms

PREPROCESSING_VERSION = 'retfound-rgb-resize256-crop224-imagenet-v1'


def build_transform():
    return transforms.Compose([
        transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.CenterCrop(224), transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
