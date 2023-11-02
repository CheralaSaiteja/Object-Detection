from ultralytics import YOLO
import cv2

class YOLOV8_PreTrained:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.video_capture = cv2.VideoCapture(self.camera_id)
        self.yolov8_model = YOLO("v8_Model/yolov8n.pt")
        self.yolov8_model.to('cuda')

        if not self.video_capture.isOpened():
            raise Exception("Could not open camera.")
        
    def start_inference(self):
        while True:
            ret, frame = self.video_capture.read()

            if not ret:
                break
            self.current_frame = frame
            self.process_frame()
            cv2.imshow('YOLOV8_PreTrained', self.current_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop_inference()

    def process_frame(self):
        results = self.yolov8_model(self.current_frame)

        for result in results:

            # convert all to lists
            class_list = result.boxes.cls.tolist()
            confidence_list = result.boxes.conf.tolist()
            box_param_xyxy_list = result.boxes.xyxy.tolist()
            
            # draw boxes
            for index in range(len(class_list)):
                # for now we are only considering human detection
                if class_list[index] == 0.0:

                    # calculate start and end points 
                    # convert floats to int
                    box_start_point = ((int)(box_param_xyxy_list[index][0]), (int)(box_param_xyxy_list[index][1]))
                    box_end_point = ((int)(box_param_xyxy_list[index][2]), (int)(box_param_xyxy_list[index][3]))

                    # draw rectangle and text
                    cv2.rectangle(self.current_frame, box_start_point, box_end_point, (255, 0, 0), 2)
                    cv2.putText(self.current_frame, f"Human {confidence_list[index]}", box_start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    def stop_inference(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    yolo_model = YOLOV8_PreTrained(camera_id=0)
    yolo_model.start_inference()