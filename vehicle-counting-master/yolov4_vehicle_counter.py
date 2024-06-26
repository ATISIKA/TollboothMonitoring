import cv2
import numpy as np
import dlib

trackers = []
confThreshold = 0.45  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image

classesFile = "res/coco.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

modelConfiguration = "yolov4-tiny.cfg"
modelWeights = "yolov4-tiny.weights"

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def findCenter(x, y, w, h):
    cx = int((x + w) / 2)
    cy = int((y + h) / 2)
    return cx, cy


def pointInRect(x, y, w, h, cx, cy):
    x1, y1 = cx, cy
    if (x < x1 and x1 < x + w):
        if (y < y1 and y1 < y + h):
            return True
    else:
        return False


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def postprocess(frame, outs):
    global inCount, outCount

    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    trackers_to_del = []
    for tid, trackersid in enumerate(trackers):
        trackingQuality = trackersid[0].update(frame)
        if trackingQuality < 6:
            trackers_to_del.append(trackersid[0])
    try:
        for trackersid in trackers_to_del:
            trackers.remove(trackersid)
    except IndexError:
        pass

    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        classId, conf, left, top, right, bottom = classIds[i], confidences[i], left, top, left + width, top + height

        rect = dlib.rectangle(left, top, right, bottom)
        (x, y, w, h) = rect_to_bb(rect)

        tracking = False

        for trackersid in trackers:
            pos = trackersid[0].get_position()
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())
            tx, ty = findCenter(startX, startY, endX, endY)

            t_location_chk = pointInRect(x, y, w, h, tx, ty)
            if t_location_chk:
                tracking = True

        if not tracking:
            tracker = dlib.correlation_tracker()
            tracker.start_track(frame, rect)
            trackers.append([tracker, frame])

    for num, trackersid in enumerate(trackers):
        pos = trackersid[0].get_position()
        startX = int(pos.left())
        startY = int(pos.top())
        endX = int(pos.right())
        endY = int(pos.bottom())

        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 250), 1)

        if endX < 320 and endY >= 280:
            inCount += 1
            trackers.pop(num)
        if endX > 320 and startY < 0:
            outCount += 1
            trackers.pop(num)


inCount = 0
outCount = 0
Font = cv2.FONT_HERSHEY_COMPLEX_SMALL

cap = cv2.VideoCapture('../highway.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_o = cv2.resize(frame, (640, 480))
    frame_cropped = frame_o[200:640, 0:640]

    blob = cv2.dnn.blobFromImage(frame_cropped, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    postprocess(frame_cropped, outs)

    cv2.putText(frame_o, f"IN:{inCount}", (20, 40), Font, 1, (255, 0, 0), 2)
    cv2.putText(frame_o, f"OUT:{outCount}", (550, 40), Font, 1, (255, 0, 0), 2)

    cv2.namedWindow('frame_o')
    cv2.moveWindow('frame_o', (0, 0))
    cv2.imshow('frame_o', frame_o)
    cv2.imshow('frame_cropped', frame_cropped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
