# Import necessary libraries
import cv2  # OpenCV for image processing
from PIL import ImageOps  # PIL for image operations like cropping and padding
import numpy as np  # NumPy for numerical operations and array handling
import gradio as gr  # Gradio to create a web interface for the application
import warnings  # To handle warnings

# Suppress user warnings to keep the output clean and readable
warnings.filterwarnings("ignore", category=UserWarning)

# Global variables for font style and color palette
font = cv2.FONT_HERSHEY_SIMPLEX  # Font style for text in OpenCV
font_scale = 1  # Font scale (size)
color_search = np.zeros((200, 200, 3), np.uint8)  # Color palette for search (not used in this script)
color_selected = np.zeros((200, 200, 3), np.uint8)  # Color palette for selected (not used)
hue = 0  # Initial hue value (for color filtering)

def search_contours(mask, frame, source):
    """
    Find and draw contours on the image.
    :param mask: Binary mask for the specific color range
    :param frame: The original image frame
    :param source: The source of the image (not used in the function)
    :return: Count of contours (pips) and the frame with contours drawn
    """
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pip_count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if 200 < area < 10000:  # Filter out contours that are too small or too large
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Draw contour
            pip_count += 1
            # Calculate the center of the contour
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
            cY = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
            cv2.circle(frame, (cX, cY), 3, (255, 255, 255), -1)  # Draw center point
            cv2.putText(frame, str(pip_count), (cX - 16, cY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    return pip_count, frame

def center_crop_with_padding(image):
    """
    Crop the image to a square and add white padding.
    :param image: The original image
    :return: The cropped and padded image
    """
    im = Image.fromarray(image)
    width, height = im.size
    new_size = min(width, height)
    # Crop the image to a square
    im = im.crop(((width - new_size) // 2, (height - new_size) // 2, (width + new_size) // 2, (height + new_size) // 2))
    # Crop further and add a border
    im = im.crop((25, 25, new_size - 25, new_size - 25))
    im_with_border = ImageOps.expand(im, border=3, fill=(255,255,255))
    return np.array(im_with_border)

def detect_pips_uploaded(uploaded_image, hue_threshold):
    """
    Detect and count the number of pips in the uploaded domino image.
    :param uploaded_image: The image uploaded by the user
    :param hue_threshold: The threshold for hue filtering
    :return: Processed image with pip count
    """
    if uploaded_image is None:
        return None
    image = uploaded_image[:, :, :3]  # Remove alpha channel if present
    image = cv2.resize(image, (512, 512))  # Resize image for consistent processing
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Convert image to HSV color space
    # Define the HSV range for color filtering
    lower_hsv = np.array([max(0, hue - hue_threshold), 50, 20])
    upper_hsv = np.array([min(179, hue + hue_threshold), 255, 255])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)  # Create a binary mask for the specified color range
    count, result_frame = search_contours(mask, image, source="image")  # Detect contours (pips)
    # Display the total pip count on the image
    cv2.putText(result_frame, f'Total pip count is: {count}', (10, result_frame.shape[0] - 30), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
    return result_frame

# Gradio interface setup
iface_uploaded = gr.Interface(detect_pips_uploaded,
    inputs=[
        gr.inputs.Image(type="numpy", label="Upload Image", source="upload"),  # Image upload input
        gr.inputs.Slider(label="Hue Threshold", minimum=0, maximum=500, step=1, default=250)  # Slider for hue threshold
    ],
    outputs=gr.outputs.Image(type="numpy", label="Result"),  # Output display
    title='<b><font size="4">🁫Image Processing demonstration of the findContours function in OpenCV using Python:🁫</b>',
    description='<div style="text-align:center;"><b style="font-size:20px;">An application to help you keep score when playing Dominos</b><br>Use your Ipad take photo and upload to calculate a score<br>Note: lighting and camera angles are key factors :)</div>',
    allow_flagging=False,
    live=False,
    theme="dark",
)

# Launch the Gradio interface
iface_uploaded.launch()
