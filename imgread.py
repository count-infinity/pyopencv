import cv2
import numpy as np
# Step 1 is already done since you've installed OpenCV

# Step 2: Read the image
image = cv2.imread('tnr.png')

# Step 3: Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 4: Apply threshold (you can also try Canny edge detection)
_, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Step 5: Find contours
contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# Initialize an empty list to hold the indices of second-level contours
second_level_contours = []

# Check each contour
for i, (next_, previous, first_child, parent) in enumerate(hierarchy[0]):
    # Check if the contour has a parent (not -1) and if that parent has a parent
    if parent != -1 and hierarchy[0][parent][3] != -1:
        second_level_contours.append(i)

print(len(second_level_contours))
# Loop through the contours
for i in second_level_contours:

    
    # Compute the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contours[i])

    if w < 10 or h < 10: continue

    # Extract the ROI from the image using the bounding box coordinates
    roi = image[y:y+h, x:x+w]

    next = input("Next:")


    # Display the ROI
    cv2.imshow(f'ROI {i}', roi)

    

    # Optionally, save the ROI to disk
    # cv2.imwrite(f'roi_{i}.jpg', roi)

cv2.waitKey(0)
cv2.destroyAllWindows()

