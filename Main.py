
from Yawn import YawnDetector
from HeadPose import HeadPoseDetector
from Camera import CameraManager
from counter import SharedCounter
from threading import Thread 
from EyeDetector import EyeDetectorMesh

import customtkinter
import os
import tkinter
from PIL import Image
import globals
globals.systemON = False
globals.eyeON = True
globals.headON = True
globals.yawnON = True
globals.soundON = True
globals.yawnON = True

#eyeON = headON = yawnON = True
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        logo = "Capstone_logo_with_text.png"
        self.title("Intelligent Drowsy Driver Detection System")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, logo)), size=(50, 70))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Capstone_logo_without_text.png")), size=(100, 100))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Capstone_logo_without_text.png")), size=(25, 35))
        #self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
        #                                         dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "home.png")),
                                                       size=(30, 30))
        self.detection_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "detection-settings.png")),
                                                       size=(30, 30))
        self.eye_detection_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "eye-scanner.png")),
                                                       size=(30, 30))
        self.yawn_detection_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "yawning-scanner.png")),
                                                          size=(30, 30))
        self.head_detection_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "head-scanner.png")),
                                                          size=(30, 30))
        self.alert__image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "alarm.png")),
                                                          size=(30, 30))
        self.sound_alert_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "sound-alert.png")),
                                                          size=(30, 30))
        self.vibration_alert_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "car-seat.png")),
                                                        size=(30, 30))


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.logo_image,#ID\u00b3S
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Detection Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.detection_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Alert Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.alert__image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["System","Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        def turnOn():
            self.On_Off.configure(text="Turn Off", fg_color="red",hover_color="dark red", command=turnOff)
            globals.systemON = True
            print("Systen On")

        def turnOff():
            self.On_Off.configure(text="Turn On",fg_color="green", hover_color="dark green",command=turnOn)
            globals.systemON = False
            print("systen Off")

        self.On_Off = customtkinter.CTkButton(self.home_frame, text="Turn On",fg_color="green",hover_color="dark green", command=turnOn,)
        self.On_Off.grid(row=1, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(2,weight=1)

        def switch1_event():
            print("switch toggled, current value:", switch1_var.get())
            globals.eyeON = switch1_var.get()

        switch1_var = customtkinter.BooleanVar(value=True)
        switch1 = customtkinter.CTkSwitch(self.second_frame, text="Eye  Detection", command=switch1_event,
                                         variable=switch1_var, onvalue=True, offvalue=False)
        switch1.grid(row=1,column=0,padx=5,pady=20)
        self.eye_label_image = customtkinter.CTkLabel(self.second_frame, text="",
                                                                   image=self.eye_detection_image)
        self.eye_label_image.grid(row=1, column=1, padx=5, pady=20)

        def switch2_event():
            print("switch toggled, current value:", switch2_var.get())
            globals.headON = switch2_var.get()

        switch2_var = customtkinter.BooleanVar(value=True)
        switch2 = customtkinter.CTkSwitch(self.second_frame, text="Head Detection", command=switch2_event,
                                         variable=switch2_var, onvalue=True, offvalue=False)
        switch2.grid(row=2,column=0,padx=5,pady=20)
        self.head_label_image = customtkinter.CTkLabel(self.second_frame, text="",
                                                                   image=self.head_detection_image)
        self.head_label_image.grid(row=2, column=1, padx=5, pady=20)

        def switch3_event():
            print("switch toggled, current value:", switch3_var.get())
            globals.yawnON = switch3_var.get()

        switch3_var = customtkinter.BooleanVar(value=True)
        switch3 = customtkinter.CTkSwitch(self.second_frame, text="Yawn Detection", command=switch3_event,
                                         variable=switch3_var, onvalue=True, offvalue=False)
        switch3.grid(row=3,column=0,padx=5,pady=20)
        self.yawn_label_image = customtkinter.CTkLabel(self.second_frame, text="",
                                                                   image=self.yawn_detection_image)
        self.yawn_label_image.grid(row=3, column=1, padx=5, pady=20)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(2, weight=1)

        def switch4_event():
            print("switch toggled, current value:", switch4_var.get())
            globals.soundON = switch2_var.get()

        switch4_var = customtkinter.BooleanVar(value=True)
        switch4 = customtkinter.CTkSwitch(self.third_frame, text="Sound Alert", command=switch4_event,
                                          variable=switch4_var, onvalue=True, offvalue=False)
        switch4.grid(row=1, column=0, padx=5, pady=20)
        self.sound_label_image = customtkinter.CTkLabel(self.third_frame, text="",
                                                      image=self.sound_alert_image)
        self.sound_label_image.grid(row=1, column=1, padx=5, pady=20)

        def switch5_event():
            print("switch toggled, current value:", switch5_var.get())
            globals.vibrationON = switch5_var.get()

        switch5_var = customtkinter.BooleanVar(value=True)
        switch5 = customtkinter.CTkSwitch(self.third_frame, text="Vibration  ", command=switch5_event,
                                          variable=switch5_var, onvalue=True, offvalue=False)
        switch5.grid(row=2, column=0, padx=5, pady=20)
        self.vibration_label_image = customtkinter.CTkLabel(self.third_frame, text="",
                                                       image=self.vibration_alert_image)
        self.vibration_label_image.grid(row=2, column=1, padx=5, pady=20)


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()


    camera_manager = CameraManager()
    counter = SharedCounter()

    Eye_Detector = EyeDetectorMesh(counter, camera_manager)
    eye = Thread(target=Eye_Detector.run)
    
    
    face_mesh_detector = YawnDetector(counter, camera_manager)
    detector_thread = Thread(target=face_mesh_detector.run)

    head_pose = HeadPoseDetector(counter, camera_manager)
    pose_thread = Thread(target=head_pose.run)

    detector_thread.start()

    eye.start()

    pose_thread.start()

    interface = Thread(target=app.mainloop())
    interface.start()

    interface.join()
    eye.join()
    detector_thread.join()
    pose_thread.join()


    camera_manager.stop()
