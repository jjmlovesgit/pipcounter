#NOTE:  ENV is set to 'pip'
import cv2
from matplotlib.pyplot import hsv
from PIL import ImageOps
import numpy as np
import gradio as gr
import warnings

# Filter out user warnings to avoid any unnecessary clutter in the output
warnings.filterwarnings("ignore", category=UserWarning)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color_search = np.zeros((200, 200, 3), np.uint8)
color_selected = np.zeros((200, 200, 3), np.uint8)
hue = 0

def search_contours(mask, frame, source):
    contours_count = 0
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pip_count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if 200 < area < 10000:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            contours_count += 1
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            cv2.circle(frame, (cX, cY), 3, (255, 255, 255), -1)
            pip_count += 1
            cv2.putText(frame, str(pip_count), (cX - 16, cY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    return pip_count, frame

def center_crop_with_padding(image):
    im = Image.fromarray(image)
    width, height = im.size
    new_size = min(width, height)
    im = im.crop(((width - new_size) // 2, (height - new_size) // 2, (width + new_size) // 2, (height + new_size) // 2))
    im = im.crop((25, 25, new_size - 25, new_size - 25))
    im_with_border = ImageOps.expand(im, border=3, fill=(255,255,255))
    return np.array(im_with_border)

def detect_pips_uploaded(uploaded_image, hue_threshold):
    if uploaded_image is None:
        return None
    image = uploaded_image[:, :, :3]
    image = cv2.resize(image, (512, 512))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue = 60
    lower_hue, upper_hue = max(0, hue - hue_threshold), min(179, hue + hue_threshold)
    lower_hsv = np.array([lower_hue, 50, 20])
    upper_hsv = np.array([upper_hue, 255, 255])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    count, result_frame = search_contours(mask, image, source="image")
    cv2.putText(result_frame, f'Total pip count is: {count}', (10, result_frame.shape[0] - 30), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
    return result_frame

iface_uploaded = gr.Interface(detect_pips_uploaded,
    inputs=[
        gr.inputs.Image(type="numpy", label="Upload Image", source="upload"),
        gr.inputs.Slider(label="Hue Threshold", minimum=0, maximum=500, step=1, default=250)
    ],
    outputs=gr.outputs.Image(type="numpy", label="Result"),
    title='<b><font size="4">🁫Image Processing demonstration of the findContours function in OpenCV using Python:🁫</b>',
    description='<div style="text-align:center;"><b style="font-size:20px;">An application to help you keep score when playing Dominos</b><br>Use your Ipad take photo and upload to calculate a score<br>Note: lighting and camera angles are key factors :)</div>',
    allow_flagging=False,
    live=False,
    theme="dark",
    )

iface_uploaded.launch()
