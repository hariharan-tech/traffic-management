import telegram_bot
import numpy as np
import cv2
import mail_upload
import telegram_bot

probability_minimum = 0.5
threshold = 0.3

# for person on bike
weights0_path = "models\\bike\\yolov3-obj_final.weights"
configuration0_path = 'models\\bike\\yolov3_pb.cfg'
network0 = cv2.dnn.readNetFromDarknet(configuration0_path, weights0_path)
layers_names0_all = network0.getLayerNames()
layers_names0_output = [layers_names0_all[i-1] for i in network0.getUnconnectedOutLayers()]
labels0 = open('models\\bike\\coco.names').read().strip().split('\n')


# for helmet
weights1_path = 'models\helmet\yolov3-helmet.weights'
configuration1_path = 'models\helmet\yolov3-helmet.cfg'
network1 = cv2.dnn.readNetFromDarknet(configuration1_path, weights1_path)
layers_names1_all = network1.getLayerNames()
layers_names1_output = [layers_names1_all[i-1] for i in network1.getUnconnectedOutLayers()]
labels1 = open('models\helmet\helmet.names').read().strip().split('\n')
img_file = ".\\images\\new_pic.jpg"

def predict():
    image_input = cv2.imread(img_file)
    blob = cv2.dnn.blobFromImage(image_input,1/255.0,(416,416),swapRB=True,crop=False)
    network0.setInput(blob)
    network1.setInput(blob)
    output_from_network0 = network0.forward(layers_names0_output)
    output_from_network1 = network1.forward(layers_names1_output)
    np.random.seed(42)
    colours0 = np.random.randint(0,255,size=(len(labels0),3),dtype='uint8')
    colours1 = np.random.randint(0,255,size=(len(labels1),3),dtype='uint8')
    bounding_boxes0 = []
    confidences0 = []
    class_numbers0 = []

    bounding_boxes1 = []
    confidences1 = []
    class_numbers1 = []

    h,w = image_input.shape[:2]

    for result in output_from_network0:
        for detection in result:
            scores = detection[5:]
            class_current=np.argmax(scores)
            confidence_current=scores[class_current]
            if confidence_current>probability_minimum:
                box_current=detection[0:4]*np.array([w,h,w,h])
                x_center,y_center,box_width,box_height=box_current.astype('int')
                x_min=int(x_center-(box_width/2))
                y_min=int(y_center-(box_height/2))
                
                bounding_boxes0.append([x_min,y_min,int(box_width),int(box_height)])
                confidences0.append(float(confidence_current))
                class_numbers0.append(class_current)
                
    for result in output_from_network1:
        for detection in result:
            scores = detection[5:]
            class_current=np.argmax(scores)
            confidence_current=scores[class_current]
            if confidence_current>probability_minimum:
                box_current=detection[0:4]*np.array([w,h,w,h])
                x_center,y_center,box_width,box_height=box_current.astype('int')
                x_min=int(x_center-(box_width/2))
                y_min=int(y_center-(box_height/2))
                
                bounding_boxes1.append([x_min,y_min,int(box_width),int(box_height)])
                confidences1.append(float(confidence_current))
                class_numbers1.append(class_current)

    results0 = cv2.dnn.NMSBoxes(bounding_boxes0,confidences0,probability_minimum,threshold)
    results1 = cv2.dnn.NMSBoxes(bounding_boxes1,confidences1,probability_minimum,threshold)
    print(len(results0),len(results1))
    if len(results0) > len(results1): # if number of bikes detected is greater than the number of helmet
        if len(results0) > 0:
            for i in results0.flatten():
                x_min,y_min=bounding_boxes0[i][0],bounding_boxes0[i][1]
                box_width,box_height= bounding_boxes0[i][2],bounding_boxes0[i][3]
                colour_box_current=[int(j) for j in colours0[class_numbers0[i]]]   
                cv2.rectangle(image_input,(x_min,y_min),(x_min+box_width,y_min+box_height),colour_box_current,5)
                text_box_current0='{}: {:.4f}'.format(labels0[int(class_numbers0[i])],confidences0[i])
                cv2.putText(image_input,text_box_current0,(x_min,y_min-7),cv2.FONT_HERSHEY_SIMPLEX,1.5,colour_box_current,5)

        if len(results1) > 0:
            for i in results1.flatten():
                x_min,y_min=bounding_boxes1[i][0],bounding_boxes1[i][1]
                box_width,box_height= bounding_boxes1[i][2],bounding_boxes1[i][3]
                colour_box_current=[int(j) for j in colours1[class_numbers1[i]]]   
                cv2.rectangle(image_input,(x_min,y_min),(x_min+box_width,y_min+box_height),colour_box_current,5)
                text_box_current1='{}: {:.4f}'.format(labels1[int(class_numbers1[i])],confidences1[i])
                cv2.putText(image_input,text_box_current1,(x_min,y_min-7),cv2.FONT_HERSHEY_SIMPLEX,1.5,colour_box_current,5)
        cv2.imwrite(".\\images\\camera_cv2.jpg",image_input)
        telegram_bot.img_file = img_file
        mail_upload.img_file = img_file
        telegram_bot.send_alert_telegram()
        mail_upload.send_mail_alert()
    else:
        print("no issues")
# predict()

if __name__ == "__main__":
    predict()