import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cv2


def detect(image):
    j=0
    (H, W) = image.shape[:2]
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)
    boxes = []
    confidences = []
    classIDs = []
    for output in layerOutputs:
        i = 0  
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)    
            confidence = scores[classID]

            if confidence > 0.80:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.4)
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            cv2.rectangle(image, (x, y), (x + w, y + h), (255,0,0), 2)
            j+=1
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,0,0), 2)
    fiexd_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    #fig = plt.figure(figsize=(15,20))
    #ax = fig.add_subplot(111)
    #ax.imshow(fiexd_image)
    return fiexd_image, classIDs.count(0)

st.header('Welcome to the School Monitoring System')
st.subheader('Here you can monitor each location of your school, monitoring how many people there are in each location and if there is a crowd you can use the "ALERT" button to send a text message to the campus security guards. ')

#YOLO THINS
LABELS = open("yolo/coco.names").read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet("yolo/yolov3.cfg", "yolo/yolov3.weights")

stframe = st.empty()

In1 = st.selectbox('Selecione sua câmera de observação', ['GINÁSIO', 'LANCHONETE', 'WEBCAM'])

if In1 == 'WEBCAM':
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret,frame=cap.read()
        frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        frame , count =detect(frame)
        frm = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frm, width = 520)
        
    

if In1 == 'GINÁSIO':
    pass
    
if In1 == 'LANCHONETE':
    pass
    