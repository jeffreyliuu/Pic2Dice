from flask import Flask, request
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        image_path = os.path.join("uploads", uploaded_file.filename)
        uploaded_file.save(image_path)

        # Your OpenCV logic here
        # Read the input image
        image = cv2.imread('input.jpg', cv2.IMREAD_GRAYSCALE)

        # Define the images for the dice faces and resize them to 12x12
        dice_faces = [cv2.resize(cv2.imread(f'dice_{i}.png', cv2.IMREAD_GRAYSCALE), (12, 12)) for i in range(1, 7)]

        # Size of each block of pixels that corresponds to a dice face
        block_size = 12

        # Create the output image
        output_image = np.zeros_like(image, dtype=np.uint8)

        # Create a text file to store the dice face numbers
        with open('dice_faces.txt', 'w') as file:
            # Map each 12x12 block of pixels to a dice face
            for i in range(0, image.shape[0] - block_size + 1, block_size):
                row_numbers = [] # to store the dice numbers for the current row
                for j in range(0, image.shape[1] - block_size + 1, block_size):
                    block_brightness = np.mean(image[i:i+block_size, j:j+block_size])
                    dice_face_idx = 5 - int(block_brightness // 43) # Reverse the mapping
                    dice_face_number = dice_face_idx + 1 # Convert index to dice number
                    dice_face_image = dice_faces[dice_face_idx]
                    row_numbers.append(str(dice_face_number)) # append the number to the row

                    # Place the dice face image in the corresponding position
                    output_image[i:i+block_size, j:j+block_size] = dice_face_image

                # Write the row of dice numbers to the text file
                file.write(' '.join(row_numbers) + '\n')

        # Save the output image
        output_path = os.path.join("outputs", "processed_" + uploaded_file.filename)
        cv2.imwrite(output_path, output_image)

        return {'url': output_path}

if __name__ == '__main__':
    app.run(debug=True)
