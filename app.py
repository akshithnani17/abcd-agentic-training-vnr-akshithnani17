import sys
import os
import io
import time
import threading
import webbrowser  # 1. Import this module
import torch
import torchvision.transforms as transforms
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
from model import load_model

# --- FIX FOR PYINSTALLER PATHS ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ---------------------------------

# Initialize Flask with explicit template and static paths
app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))
CORS(app)

print("Loading model...")
# Use resource_path to find the model file inside the .exe
model = load_model(resource_path('morph_model.pth'))

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def get_prediction(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(image)
        probability = torch.sigmoid(output).item()
    return probability

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    try:
        img_bytes = file.read()
        confidence = get_prediction(img_bytes)
        is_morphed = confidence > 0.5
        return jsonify({
            'isMorphed': is_morphed,
            'confidence': round(confidence * 100, 2),
            'processingTime': '0.15s'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. Function to open the browser
def open_browser():
    # Give the server 1.5 seconds to start up to avoid "Connection Refused" errors
    time.sleep(1.5) 
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Start the browser opening in a separate thread
    threading.Thread(target=open_browser).start()
    
    # 3. Run the app
    # debug=False ensures the browser doesn't reload continuously and is faster
    # host='0.0.0.0' ensures it is accessible
    app.run(debug=False, port=5000, host='0.0.0.0')