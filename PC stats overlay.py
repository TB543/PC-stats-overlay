readme = open("readme.txt", "w")
readme.write("How To Use:\n\n1. when running the program an overlay in the top right will display some of your pcs "
             "statistics\n2. CPU temp might show an error, this is normal, run OpenHardwareMonitor.exe in the folder "
             "called OpenHardwareMonitor and this will fix the error\n3. if you do not want to run this program every "
             "time, under options select start minimized\n4. if you do not want to see the window for "
             "OpenHardwareMonitor, select minimize to tray in the same options menu\n5. if you do not want to see the "
             "cmd window when the python file is run open the Launch PC stats overlay.vbs with a text editor and on "
             "line 2 where it says file path here, enter the file path to the python file, save the file and run "
             "Launch PC stats overlay.vbs instead of the python file") 
readme.close()

import os
from tkinter import *
try:
    import GPUtil
    import psutil
    import wmi
except:
    imports = open("imports.bat", "w")
    imports.write("@echo off\npip install WMI\npip install psutil\npip install GPUtil")
    imports.close()
    os.system('imports.bat')
    os.remove('imports.bat')
    import GPUtil
    import psutil
    import wmi


overlay = Tk()
overlay.title("PC stats overlay")
overlay.attributes('-fullscreen', True)
overlay.wm_attributes('-transparentcolor', overlay['bg'])
overlay.attributes('-topmost', True)
label = Label(overlay, text="", fg="white", font=("Times New Roman", 30))
label.place(relx=1.0, rely=0.0, anchor='ne')

while True:

    overlay.update()

    # gpu stats
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        gpu_load = f"GPU load: {int(gpu.load * 100)}%"
        gpu_temperature = int(gpu.temperature)

    # cpu load
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        pass
    CPU = f"CPU load: {psutil.cpu_percent()}%"

    # cpu temp
    CPU_temp = "Error"
    error = True
    w = wmi.WMI(namespace="root\OpenHardwareMonitor");
    temperature_infos = w.Sensor();
    for sensor in temperature_infos:
        if sensor.SensorType == u'Temperature':
            if sensor.Name == "CPU Package":
                CPU_temp = int(sensor.Value)
                error = False

    # ram stats
    RAM = f"RAM load: {psutil.virtual_memory().percent}%"

    stats = "GPU temp: " + str(gpu_temperature) + "°C" + "\n" + "CPU temp: " + str(CPU_temp) + "°C" + "\n" + gpu_load + "\n" + CPU + "\n" + RAM

    if error:

        CPU_temp = int(1)

    if gpu_temperature <= 70 and CPU_temp <= 70:

        label.destroy()
        label = Label(overlay, text=stats, fg="white", font=("Times New Roman", 15))
        label.place(relx=1.0, rely=0.0, anchor='ne')

    elif gpu_temperature >= 80 or CPU_temp >= 80:

        label.destroy()
        label = Label(overlay, text=stats, fg="red", font=("Times New Roman", 15))
        label.place(relx=1.0, rely=0.0, anchor='ne')

    elif CPU_temp > 70:

        label.destroy()
        label = Label(overlay, text=stats, fg="yellow", font=("Times New Roman", 15))
        label.place(relx=1.0, rely=0.0, anchor='ne')

    elif gpu_temperature > 70:

        label.destroy()
        label = Label(overlay, text=stats, fg="yellow", font=("Times New Roman", 15))
        label.place(relx=1.0, rely=0.0, anchor='ne')

