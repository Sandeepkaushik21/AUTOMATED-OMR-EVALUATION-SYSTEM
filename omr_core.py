import cv2
import numpy as np
from PIL import Image

# Load image as RGB array
def load_image(file):
    img = Image.open(file).convert("RGB")
    return np.array(img)

# Resize to max dimension
def resize_max(image, max_dim=1200):
    h, w = image.shape[:2]
    if max(h, w) <= max_dim:
        return image
    scale = max_dim / float(max(h, w))
    return cv2.resize(image, (int(w*scale), int(h*scale)))

# Detect largest rectangular contour (OMR sheet boundary)
def find_largest_rect_contour(gray):
    blurred = cv2.GaussianBlur(gray,(5,5),0)
    edged = cv2.Canny(blurred,50,150)
    contours,_ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) == 4:
            return approx.reshape(4,2)
    return None

# Order points for perspective transform
def order_points(pts):
    rect = np.zeros((4,2),dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

# Perspective warp
def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl,tr,br,bl) = rect
    widthA = np.linalg.norm(br-bl)
    widthB = np.linalg.norm(tr-tl)
    maxWidth = int(max(widthA,widthB))
    heightA = np.linalg.norm(tr-br)
    heightB = np.linalg.norm(tl-bl)
    maxHeight = int(max(heightA,heightB))
    dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0,maxHeight-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth,maxHeight))
    return warped

# Detect if a cell is filled
def detect_filled(cell):
    _, th = cv2.threshold(cell,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    filled_fraction = (th>0).sum()/float(th.size)
    return filled_fraction > 0.35

# Evaluate a single OMR sheet
def evaluate_omr(file):
    """
    Returns detected answers as {q_no: choice_letter}
    Supports sheets with 100 questions, 5 subjects, 4 choices (A-D)
    """
    image_np = load_image(file)
    image_np = resize_max(image_np)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Find sheet boundary
    pts = find_largest_rect_contour(gray)
    if pts is not None:
        warped = four_point_transform(image_np, pts)
    else:
        warped = image_np

    warped_gray = cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY)

    # Layout constants (adjust if your sheet differs)
    total_questions = 100
    questions_per_row = 4  # 4 bubbles per row (A-D)
    rows = total_questions // questions_per_row
    h, w = warped_gray.shape
    cell_h = h / rows
    cell_w = w / questions_per_row

    answers = {}

    # Detect filled bubbles
    for r in range(rows):
        for c in range(questions_per_row):
            y1 = int(r * cell_h)
            y2 = int((r+1) * cell_h)
            x1 = int(c * cell_w)
            x2 = int((c+1) * cell_w)
            cell = warped_gray[y1:y2, x1:x2]
            filled = detect_filled(cv2.resize(cell, (60,60)))
            q_no = r*questions_per_row + c + 1
            if filled:
                answers[str(q_no)] = chr(ord('A') + c)
            else:
                answers[str(q_no)] = ""
    
    return answers
