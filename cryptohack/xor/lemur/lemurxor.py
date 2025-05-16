from PIL import Image
import numpy as np

def xor_images(image_path1, image_path2, output_path):
    # Open both images and convert to RGB
    img1 = Image.open(image_path1).convert('RGB')
    img2 = Image.open(image_path2).convert('RGB')

    # Ensure both images are the same size
    if img1.size != img2.size:
        raise ValueError("Images must be the same size to XOR them.")

    # Convert images to NumPy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # XOR the arrays
    xor_result = np.bitwise_xor(arr1, arr2)

    # Convert back to image and save
    result_img = Image.fromarray(xor_result.astype(np.uint8))
    result_img.save(output_path)

# Example usage:
xor_images("flag.png", "lemur.png", "output_xor.png")
