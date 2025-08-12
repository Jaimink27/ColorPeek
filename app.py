from flask import Flask, render_template, request  # Flask web framework modules
from PIL import Image, UnidentifiedImageError     # Pillow for image processing
import io                                         # For in-memory binary streams
import base64                                     # For encoding image data to display on HTML

# --------------------------
# FLASK APP CONFIGURATION
# --------------------------

app = Flask(__name__)

# Limit uploaded file size to 8 MB
# This helps prevent users from uploading huge files that can crash the server
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 * 1024 KB * 1024 bytes = 8 MB

# Define which image file extensions are allowed for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# --------------------------
# HELPER FUNCTION: allowed_file
# --------------------------
def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    :param filename: The name of the uploaded file
    :return: True if the extension is allowed, otherwise False
    """
    # '.' in filename → ensures file has an extension
    # filename.rsplit('.', 1)[1] → gets the extension after the last dot
    # .lower() → makes it case-insensitive
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --------------------------
# HELPER FUNCTION: extract_palette_pillow
# --------------------------
def extract_palette_pillow(pil_image, num_colors=6, resize_for_speed=800):
    """
    Extracts the most dominant colors from an image using Pillow.

    Steps:
    1. Resize image for faster processing
    2. Handle transparency (convert transparent areas to white)
    3. Convert image to a palette-based format (adaptive color reduction)
    4. Get color frequency and percentage usage
    5. Return the colors in HEX, RGB, pixel count, and percentage

    :param pil_image: The Pillow Image object to process
    :param num_colors: Number of top colors to extract
    :param resize_for_speed: Maximum dimension (width/height) to resize for speed
    :return: List of color dictionaries
    """

    # Work on a copy so the original image is not modified
    image = pil_image.copy()

    # Step 1: Resize image while keeping aspect ratio
    image.thumbnail((resize_for_speed, resize_for_speed))

    # Step 2: Handle transparency
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and 'transparency' in image.info):
        # Create a white background
        background = Image.new("RGB", image.size, (255, 255, 255))
        # Extract the alpha channel (transparency mask)
        alpha = image.convert("RGBA").split()[-1]
        # Paste the original image over the background using alpha mask
        background.paste(image, mask=alpha)
        image = background
    else:
        # Ensure the image is in RGB mode (no alpha channel)
        image = image.convert('RGB')

    # Step 3: Convert to paletted image with an adaptive palette,by using adaptive means choosing, it gives most frequent color.
    paletted = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)

    # Get palette data → a flat list [r0, g0, b0, r1, g1, b1, ...]
    palette = paletted.getpalette()

    # Get color counts: list of tuples (pixel_count, palette_index)
    color_counts = paletted.getcolors()
    if not color_counts:
        return []  # No colors found → return empty list

    # Step 4: Sort colors by count (most used first)
    color_counts.sort(reverse=True)

    # Calculate total pixels to later find percentages
    total = sum(count for count, idx in color_counts)

    results = []

    # Step 5: Get top `num_colors` and extract their details
    for i in range(num_colors):
        count, idx = color_counts[i]

        # Extract RGB values from the palette
        r = palette[idx * 3]
        g = palette[idx * 3 + 1]
        b = palette[idx * 3 + 2]

        # Convert RGB to HEX (e.g., "#ff00aa")
        hexcode = '#%02x%02x%02x' % (r, g, b)

        # Find percentage of the image occupied by this color
        percent = round((count / total) * 100, 2)

        # Store results in dictionary format
        results.append({
            'hex': hexcode,        # HEX color code
            'rgb': (r, g, b),      # RGB tuple
            'count': int(count),   # Number of pixels with this color
            'percent': percent     # Percentage of total image
        })

    return results


# --------------------------
# MAIN ROUTE: index
# --------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main page route:
    - GET → Show upload form
    - POST → Process uploaded image, extract color palette, and display results
    """
    if request.method == 'POST':
        # Get uploaded file from the form
        file = request.files.get('image')

        # Validate file existence and extension
        if not file or file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error='Please upload a valid image file (png/jpg/jpeg/gif).')

        try:
            # Open image using Pillow
            image = Image.open(file.stream)
        except UnidentifiedImageError:
            # Pillow couldn't identify file as a valid image
            return render_template('index.html', error='Cannot identify image file. Try a different file.')

        # Get number of colors from form, with default value = 6
        try:
            num_colors = int(request.form.get('num_colors', 6))
            # Restrict between 1 and 20 for practicality
            num_colors = max(1, min(20, num_colors))
        except ValueError:
            num_colors = 6

        # Extract the palette from the image
        palette = extract_palette_pillow(image, num_colors=num_colors)

        # Prepare a smaller preview of the image for the result page
        preview = image.copy()
        preview.thumbnail((600, 600))
        buf = io.BytesIO()
        preview.save(buf, format='JPEG')

        # Convert preview to Base64 so it can be embedded in HTML without saving to disk
        data = base64.b64encode(buf.getvalue()).decode('utf-8')
        data_uri = 'data:image/jpeg;base64,' + data

        # Render HTML with palette and preview image
        return render_template('index.html', palette=palette, image_data=data_uri, num_colors=num_colors)

    # If GET request → just show the upload form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  # debug=True → auto-reloads server on code change
