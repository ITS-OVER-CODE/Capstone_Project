
from Yawn import YawnDetector
from HeadPose import HeadPoseDetector
from Camera import CameraManager
from counter import SharedCounter
from threading import Thread 
from Capstone_Project.yolov5.detect import parse_opt, main

if __name__ == '__main__':

    
    opt = parse_opt()
    main(opt)
    
    # camera_manager = CameraManager()
    # counter = SharedCounter()

    # face_mesh_detector = YawnDetector(counter, camera_manager)
    # detector_thread = Thread(target=face_mesh_detector.run)

    # head_pose = HeadPoseDetector(counter, camera_manager)
    # pose_thread = Thread(target=head_pose.run)

    # if True:
    #     detector_thread.start()

    # if True: 
    #     pose_thread.start()

    # detector_thread.join()
    # pose_thread.join()

    # camera_manager.stop()
