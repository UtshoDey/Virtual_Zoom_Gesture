import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
width, height = 2560, 1440
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.7)
startDist = None
scale = 0
cx, cy = width, height

while True:
    success, img = cap.read()
    img = cv2.flip(img, 3)
    hands, img = detector.findHands(img)
    img1 = cv2.imread("sample.jpg")

    if len(hands) == 2:
        # print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
            # print("Zoom Gesture")
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            # point 8 is the tip of the index finger
            if startDist is None:
                # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)

                startDist = length

            # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)
            length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)

            scale = int((length - startDist) // 2)
            cx, cy = info[4:]
            # print(scale)
    else:
        startDist = None

    try:
        h1, w1, _ = img1.shape
        newH, newW = ((h1 + scale) // 2) * 2, ((w1 + scale) // 2) * 2
        img1 = cv2.resize(img1, (newW, newH))

        img[cy - newH // 2:cy + newH // 2, cx - newW // 2:cx + newW // 2] = img1

    except:
        pass

    cv2.imshow("Virtual ZOOM Gesture", img)
    cv2.waitKey(1)
