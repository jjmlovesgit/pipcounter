# An application we call the "Pipcounter" to count your domino Pips from a picture 

An elegant and concise python program to count the pips on your dominoes for scoring

Run the code and be sure to try the sample images to test it. 

This program works best with a modern cell phone camera with images taken from directly over your dominoes.  

Hi res photos and decent light work best.

Be sure to watch the video and ask any questions in the comments section



• Start: The process begins.
• Read Image: An image is uploaded and read.
• Resize Image: The image is resized for consistent processing.
• Is Image None?: Checks if the image is null.
• Yes: If the image is null, the process ends returning None.
• No: If the image is not null, it proceeds to the next step.
• Convert to HSV: The image is converted to HSV color space.
• Apply Hue Threshold: A hue threshold is applied for color filtering.
• Create Mask: A binary mask is created for the specified color range.
• Search Contours: The script searches for contours in the image.
• Draw Contours and Calculate Pips: Contours are drawn, and pips (dots) are counted.
• Put Text on Image: The total pip count is displayed on the image.
End: Return Processed Image: The processed image with pip count is returned.

![image](https://github.com/jjmlovesgit/pipcounter/assets/47751509/8db4f74b-0eb5-4f12-8b94-05feb3f73724)


![image](https://github.com/jjmlovesgit/pipcounter/assets/47751509/8b3369d0-6b61-419e-9650-968547303885)

https://youtu.be/0Kgm_aLunAo
