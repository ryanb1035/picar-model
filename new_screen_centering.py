import cv2
import numpy as np

def find_green_dot(image_path):
    # Load the image
    image = cv2.imread(image_path)
    output_image = image.copy()

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range of green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    
    # Create a mask that only contains green colors
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 <= area <= 500:
            # Calculate the center of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                print("Green dot of interest found at:", cx, cy, "with area:", area)
                
                # Draw the contour on the output image
                cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 2)
    
    # Save the output image with contours
    cv2.imwrite('output_with_contours.jpg', output_image)
    print("Output image saved with green dot contours.")
    return output_image



    green_dots = []
    for contour in contours:
        # Calculate the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            green_dots.append({"coordinates": (cx, cy), "contour": contour})
            print("Green dot found at:", cx, cy)
    
    if not green_dots:
        print("No green dots found.")
    return green_dots

# Example usage
find_green_dot("green_dot_test_picture.png")