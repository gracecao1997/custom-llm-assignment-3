"""Render the unchanged asciicast text into a readable-speed GIF (requires Pillow).
This is a recording visualization, not a screenshot of a Terminal window.
"""
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
lines = (ROOT / 'evidence/chat.cast').read_text().splitlines()
events = [json.loads(line) for line in lines[1:]]
text = ''.join(event[2] for event in events if event[1] == 'o').replace('\r', '')
try:
    font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 22)
    title_font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 26)
except OSError:
    font = ImageFont.truetype('DejaVuSansMono.ttf', 22)
    title_font = ImageFont.truetype('DejaVuSansMono.ttf', 26)
markers = ['You: the customer', 'You: a cat', 'You: explain quantum teleportation', 'You: /quit']
fragments = [text[:text.index(marker)] for marker in markers[1:]] + [text]
frames = []
for index, fragment in enumerate(fragments):
    image = Image.new('RGB', (1440, 810), '#111c27')
    draw = ImageDraw.Draw(image)
    draw.text((40, 30), 'Actual nanoGPT chat recording', font=title_font, fill='#edf5ff')
    draw.text((40, 78), 'expanded | 3,000 updates | 48-token context | fresh prompt each turn', font=font, fill='#9ec9e8')
    draw.text((40, 116), 'Readable-speed replay of captured terminal I/O; original chat.cast retained.', font=font, fill='#9ec9e8')
    y = 177
    for line in fragment.rstrip().split('\n'):
        for wrapped in textwrap.wrap(line, width=98, replace_whitespace=False) or ['']:
            color = '#ffd58a' if wrapped.startswith('Unknown words:') else '#e9f1ec'
            draw.text((40, y), wrapped, font=font, fill=color)
            y += 32
    draw.text((40, 754), f'Recording frame {index + 1}/{len(fragments)} | text and replies unedited', font=font, fill='#9ec9e8')
    frames.append(image)
frames[-1].save(ROOT / 'evidence/chat_recording_still.png')
frames[0].save(ROOT / 'evidence/chat_recording.gif', save_all=True,
               append_images=frames[1:], duration=[2200, 2800, 3500, 5000], loop=0)
print('Rendered original recording as GIF and final-frame PNG.')
