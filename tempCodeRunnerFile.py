with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        # image = cv2.resize(image, (1280, 720), fx=0, fy=0,
        #                    interpolation=cv2.INTER_CUBIC)
        image = cv2.flip(image, 1)
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                dataPointlandmark = []
                for idx, data_landmark in enumerate(hand_landmarks.landmark):
                    cx, cy = data_landmark.x*640, data_landmark.y*480
                    dataPointlandmark.append([int(cx), int(cy)])
                cv2.circle(image, dataPointlandmark[8], 2, (255, 0, 0), 2)
            dataBoxOn = []
            for no, checkdatabox in enumerate(dataBox):
                if dataPointlandmark[8][0] >= checkdatabox[0][0] and dataPointlandmark[8][1] >= checkdatabox[0][1] and dataPointlandmark[8][0] <= checkdatabox[1][0] and dataPointlandmark[8][1] <= checkdatabox[1][1]:
                    dataBoxOn.append(1)
                else:
                    dataBoxOn.append(0)
        else:
            dataBoxOn = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for number, databoxx in enumerate(dataBox):
            cv2.putText(image, str(number+1), (
                        int((databoxx[0][0]+databoxx[1][0])/2), int((databoxx[0][1]+databoxx[1][1])/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (28, 215, 249) if dataBoxOn[number] == 1 else (255, 0, 0), 5 if dataBoxOn[number] == 1 else 1)
            if dataBoxOn[number] == 1:
                print(databoxx if dataBoxOn[number] ==
                      1 else [0], [] if not dataPointlandmark else dataPointlandmark[8], dataBoxOn)
            cv2.rectangle(image, databoxx[0], databoxx[1], (255, 0, 0)
                          if dataBoxOn[number] == 1 else (0, 255, 0), 5 if dataBoxOn[number] == 1 else 1)
        dataimage = image.copy()
        dataimage = cv2.cvtColor(dataimage, cv2.COLOR_BGR2RGB)
        # cam.send(dataimage)

        cv2.imshow('MediaPipe Hands', image)
        # cam.sleep_until_next_frame()
        if cv2.waitKey(5) & 0xFF == 27:
            break