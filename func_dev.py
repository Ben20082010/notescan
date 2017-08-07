import cv2, numpy





points=[]
def pickpoints(img,points):

    # load the image, clone it, and setup the mouse callback function
    clone = img.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    # if there are two reference points, then crop the region of interest
    # from teh image and display it
    # if len(refPt) == 2:
    #     roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    #     cv2.imshow("ROI", roi)
    #     cv2.waitKey(0)

    # close all open windows
    cv2.destroyAllWindows()
    return points


def click(event, x, y, flags, param):
    # grab references to the global variables
    global points, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        cropping = True
        points.append(point)
        cv2.circle(img,point,5,(0,255,0),-1)