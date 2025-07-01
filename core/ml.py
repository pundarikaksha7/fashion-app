# detect_apparel.py

import os

def detect_apparel(image_path, model):
    print("Running apparel detection...")

    # Relevant clothing classes from OpenImages / fashion datasets
    RELEVANT_CLASSES = {
        'shirt', 't-shirt', 'trousers', 'pants', 'shorts',
        'jacket', 'hoodie', 'sweater', 'dress', 'skirt', 'jeans',
        'top', 'blazer', 'coat', 'tank top', 'suit','SHIRT','HOODIE',
        'Trousers'
    }

    CONFIDENCE_THRESHOLD = 0.35

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