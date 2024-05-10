from flask import Flask, render_template, request
import cv2
import numpy as np
import base64

app = Flask(__name__)

# def crop_image(image, x, y, width, height):
#     cropped_img = image[y:y+height, x:x+width]
#     return cropped_img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file is present in the request
        if 'image' not in request.files:
            return render_template('index.html', error='No image file uploaded.')
        
        # Read the uploaded image
        image = request.files['image'].read()
        
        # Convert the image data to numpy array
        nparr = np.frombuffer(image, np.uint8)
        
        # Decode the image array
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Check if crop parameters are provided
        if 'crop' in request.form:
            x = int(request.form['x'])
            y = int(request.form['y'])
            width = int(request.form['width'])
            height = int(request.form['height'])
            print(x)
            print(y)
            print(width)
            print(height)

            
            
            # Crop the image
            img_cv = img_cv[y:y+height, x:x+width]
        
        # Check if rotate angle is provided
        if 'rotate' in request.form:
            angle = int(request.form['angle'])
            print(angle)
            
            # Rotate the image
            (h, w) = img_cv.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            img_cv = cv2.warpAffine(img_cv, M, (w, h))
        
        # Check if grayscale conversion is requested
        if 'grayscale' in request.form:
            # Convert the image to grayscale
            print("YEss")
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Encode the modified image to base64
        _, img_encoded = cv2.imencode('.png', img_cv)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        
        return render_template('result.html', processed_image=img_base64)
    
    # Render the index.html template
    return render_template('index.html', error='')

if __name__ == '__main__':
    app.run()
