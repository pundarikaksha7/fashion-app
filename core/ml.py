# detect_apparel.py

import os
from transformers import AutoProcessor, AutoModelForImageClassification
from PIL import Image
import torch

# Load model once at startup
processor = AutoProcessor.from_pretrained("Falconsai/nsfw_image_detection")
model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")

def is_obscene(image_path, threshold=0.7):
    """
    Returns True if NSFW content is detected with high probability.
    """
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)[0]
    predicted_class = probs.argmax().item()
    labels = model.config.id2label

    nsfw_score = probs[predicted_class].item()
    predicted_label = labels[predicted_class]

    print(f"[NSFW Detection] Label: {predicted_label}, Confidence: {nsfw_score:.3f}")

    return predicted_label.lower() == "nsfw" and nsfw_score > threshold

def detect_apparel(image_path, model):
    print("Running apparel detection...")

    # Relevant clothing classes from OpenImages / fashion datasets
    RELEVANT_CLASSES = {
        'shirt', 't-shirt', 'trousers', 'pants', 'shorts',
        'jacket', 'hoodie', 'sweater', 'dress', 'skirt', 'jeans',
        'top', 'blazer', 'coat', 'tank top', 'suit','SHIRT','HOODIE',
        'Trousers'
    }

    CONFIDENCE_THRESHOLD = 0.25

    if not os.path.exists(image_path):
        print("ERROR: Image not found:", image_path)
        return []

    try:
        results = model(image_path)
    except Exception as e:
        print(f"[detect_apparel] Detection failed: {e}")
        return []

    labels = []
    for r in results:
        names = model.names  # Make sure to use the global model names, not r.names
        for box in r.boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)
            label = names.get(class_id, "").lower()

            if confidence >= CONFIDENCE_THRESHOLD:
                labels.append({
                    'label': label,
                    'confidence': round(confidence, 4)
                })

    print("Detected labels:", labels)
    return labels