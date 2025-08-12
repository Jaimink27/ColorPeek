🎨 ColorPeek
Extract, explore, and elevate your color palettes — effortlessly.

ColorPeek is a simple yet powerful Python-based tool designed to extract dominant colors from images. Whether you’re a designer, developer, or just a curious pixel enthusiast, this tool helps you peek behind the scenes and grab the colors that matter most.

📜 Features
Dominant Color Extraction – Identify key colors from any image.

Simple CLI Usage – No clunky interfaces; run and get results instantly.

Customizable Output – Tweak the number of colors, formats, and more.

Open Source & Lightweight – Because bloated software is so last decade.

🛠️ Installation
Make sure you have Python 3.8+ installed.

# Clone the repository
git clone https://github.com/Jaiminkansagara1327/ColorPeek.git

# Navigate into the project folder
cd ColorPeek

# Install dependencies
pip install -r requirements.txt

🚀 Usage
# Basic usage
python colorpeek.py path/to/image.jpg

# Example: Extract top 5 colors
python colorpeek.py path/to/image.jpg --colors 5
By default, the script will print RGB values and HEX codes for each extracted color. Because we know you like choices, you can export them to a file too.

⚙️ Arguments
Argument	Description	Default
--colors	Number of colors to extract	3
--output	Save results to a file	None
--show	Display extracted colors visually	False

🖼️ Example Output
Input Image:
(imagine your favorite image here)

Extracted Colors:
1. #1E3A5F  →  RGB(30, 58, 95)
2. #F9A825  →  RGB(249, 168, 37)
3. #D84315  →  RGB(216, 67, 21)

🤓 Why ColorPeek?

Because sometimes, you just need the exact shade of blue from that one JPEG your client sent you at 3AM — and you deserve a tool that delivers it without fuss.

Also, it’s lightweight, open-source, and doesn’t try to sell you “ColorPeek Premium” for $9.99/month. You’re welcome.

📄 License
MIT License — you’re free to use, modify, and distribute, just don’t claim you built it from scratch at 2AM without coffee.

🧑‍💻 Contributing
Fork it. Create a branch. Add your magic. Open a pull request.
If your contribution fixes a bug we didn’t notice because we were too busy obsessing over color gradients, we’ll thank you eternally.
