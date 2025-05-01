from PIL import Image
import os

input_folder = "assets/old"
output_folder = "assets/processed"
os.makedirs(output_folder, exist_ok=True)

target_size = (120, 120)  # You can use 120x120 if needed

for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Make square by padding with transparent or white background
        width, height = img.size
        new_size = max(width, height)
        background = Image.new("RGBA", (new_size, new_size), (255, 255, 255, 0))  # Transparent
        offset = ((new_size - width) // 2, (new_size - height) // 2)
        background.paste(img, offset)

        # Resize to target
        square_img = background.resize(target_size)

        # Save processed version
        output_path = os.path.join(output_folder, filename)
        square_img.save(output_path)

print("✅ All avatars resized and centered in:", output_folder)
