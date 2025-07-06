

import os
from transformers import AutoProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import cv2
import numpy as np
from torchvision import models, transforms
from ultralytics import YOLO

# Load model once at startup
NSFW_PROCESSOR = AutoProcessor.from_pretrained("Falconsai/nsfw_image_detection")
NSFW_MODEL = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")

# Load once globally to avoid reloading on every call
APPAREL_DETECTOR_MODEL = YOLO("yolov8n-oiv7.pt")  # Change to custom model if needed

ATTRIBUTE_DETECTOR_MODEL=YOLO("runs/classify/train2/weights/best.pt")


def is_obscene(image_path, threshold=0.7):
    """
    Returns True if NSFW content is detected with high probability.
    """
    image = Image.open(image_path).convert("RGB")
    inputs = NSFW_PROCESSOR(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = NSFW_MODEL(**inputs)

    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)[0]
    predicted_class = probs.argmax().item()
    labels = NSFW_MODEL.config.id2label

    nsfw_score = probs[predicted_class].item()
    predicted_label = labels[predicted_class]

    print(f"[NSFW Detection] Label: {predicted_label}, Confidence: {nsfw_score:.3f}")

    return predicted_label.lower() == "nsfw" and nsfw_score > threshold

# Dummy class attribute lists (you can refine these later)
COLORS = ['black', 'white', 'blue', 'red', 'green', 'yellow', 'gray', 'brown']
PATTERNS = ['plain', 'striped', 'checked', 'floral', 'graphic']
STYLES = ['casual', 'formal', 'sporty']

# Load pretrained ResNet model
resnet = models.resnet18(pretrained=True)
resnet.eval()

# Preprocessing transform
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet normalization
        std=[0.229, 0.224, 0.225]
    )
])
def get_color_name(h, s, v):
    if v < 50:
        return 'black'
    elif s < 40 and v > 200:
        return 'white'
    elif s < 40:
        return 'gray'
    elif h < 10 or h > 170:
        return 'red'
    elif 10 <= h < 20:
        return 'orange'
    elif 20 <= h < 30:
        return 'yellow'
    elif 30 <= h < 80:
        return 'green'
    elif 80 <= h < 100:
        return 'cyan'
    elif 100 <= h < 130:
        return 'blue'
    elif 130 <= h < 160:
        return 'purple'
    elif 160 <= h < 170:
        return 'pink'
    else:
        return 'brown'  # fallback


def classify_attributes(image_path):
    results = ATTRIBUTE_DETECTOR_MODEL(image_path)
    probs = results[0].probs
    class_id = probs.top1
    class_name = results[0].names[class_id]
    
    try:
        # Parse the class name assuming it was color_pattern_style
        color, item = class_name.split('_')
    except:
        color, item = "unknown", "unknown"

    return {
        "color": color,
        "item":item
    }

def detect_apparel(image_path):
    print("Running multi-stage apparel detection...")

    RELEVANT_CLASSES = {
        'shirt', 't-shirt', 'trousers', 'pants', 'shorts',
        'jacket', 'hoodie', 'sweater', 'dress', 'skirt', 'jeans',
        'top', 'blazer', 'coat', 'tank top', 'suit'
    }

    CONFIDENCE_THRESHOLD = 0.25
    if not os.path.exists(image_path):
        print("ERROR: Image not found:", image_path)
        return []

    try:
        results = APPAREL_DETECTOR_MODEL(image_path)
    except Exception as e:
        print(f"[detect_apparel] Detection failed: {e}")
        return []

    full_image = Image.open(image_path).convert("RGB")
    full_image_cv = cv2.cvtColor(np.array(full_image), cv2.COLOR_RGB2BGR)
    
    labels = []
    for r in results:
        names = APPAREL_DETECTOR_MODEL.names
        for box in r.boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)
            label = names.get(class_id, "").lower()

            if label in ['human face','woman','man']:
                continue

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped_img = full_image_cv[y1:y2, x1:x2]

            # Preprocess and pass cropped image to attribute model
            attr_data = classify_attributes(cropped_img)
            print(attr_data)

            labels.append({
                "label": label,
                "confidence": round(confidence, 4),
                **attr_data  # merge color, style, etc.
            })

    print("Detected outfit labels:", labels)
    return labels