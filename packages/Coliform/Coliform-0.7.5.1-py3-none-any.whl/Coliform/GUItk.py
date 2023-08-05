
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from Coliform import OneWire, MultiPlot, RPiGPIO, RPiCamera, RGBSensor
import os
import time

# Defining global variables
PUMPPWM = None
HEATPWM = None
rgb_array = None
ids = []
TemperatureNumber = None


def startGUI():
    filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))
    # filename = 'TestJPEG.jpeg'
    tf = 'PlotTextFile.txt'
    if os.path.isfile(tf):
        os.remove(tf)

    def heaterpoweron():
        try:
            HeaterPowerStatus.set('Heater ON')
            heaterbutton.configure(text='Heater OFF')
            heaterbutton.configure(command=heaterpoweroff)
            global HEATPWM
            HEATPWM = RPiGPIO.Controller(12, 100)
            HEATPWM.startup()
            heaterbutton.after(1000, heaterinput)
        except (RuntimeError, AttributeError, NameError):
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
            messagebox.showinfo(message='Heater not detected on pin 12, please make sure its connected.')

    def heaterinput():
        try:
            if HeaterPowerStatus.get() != 'Heater OFF':
                value = float(temp.get())
                sensor = float(TemperatureNumber[1])
                HEATPWM.HeaterPID(value, sensor)
            heaterbutton.after(1000, heaterinput)
        except ValueError:
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
            messagebox.showinfo(message='Please type number into Target Temperature box.')
            heaterbutton.after(1000, heaterinput)

    def heaterpoweroff():
        try:
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
        except ValueError:
            pass

    def onewireon():
        try:
            global ids
            global TemperatureNumber
            ids = OneWire.getOneWireID()
            TemperatureDegrees, TemperatureNumber = OneWire.getTempList()
            templabel.config(text=TemperatureDegrees)
            MultiPlot.GeneratePlotDataFile(tf, TemperatureNumber, start_time)
            if not ids:
                TempSensorPowerStatus.set('Temp. Sensor OFF')
                templabel.config(text='NULL')
            else:
                TempSensorPowerStatus.set('Temp. Sensor ON')
            templabel.after(1000, onewireon)
        except IndexError:
            pass

    def tempplot():
        try:
            y_title_axis = ['Temperature Plot', 'Temperature vs Time', 't(s)', 'T(C)', 'Sensor']
            MultiPlot.Plot(tf, len(ids), y_title_axis)
        except KeyError:
            messagebox.showinfo(message='No temperature sensor connected.')

    def savefile():
        tempfilename = 'TemperatureData.csv'
        y_variablename = 'TemperatureSensor'
        MultiPlot.SaveToCsv(tf, tempfilename, filepath, len(ids), y_variablename)
        messagebox.showinfo(message='File saved to directory.')

    def pumppoweron():
        try:
            PumpPowerStatus.set("Pump ON")
            pumpbutton.configure(text='Pump OFF')
            pumpbutton.configure(command=pumppoweroff)
            global PUMPPWM
            PUMPPWM = RPiGPIO.Controller(11, 100)
            PUMPPWM.startup()

        except ValueError:
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            PUMPPWM.shutdown()
            messagebox.showinfo(message='Please type number from 0-100 into Pump text box.')

        except (RuntimeError, AttributeError, NameError):
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            messagebox.showinfo(message='Pump not detected, Please make sure pump is connected to pin 11')

    def pumppoweroff():
        try:
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            PUMPPWM.shutdown()

        except (AttributeError, RuntimeError):
            messagebox.showinfo(message='Please make sure pump is connected to pin 11.')

    def pumppowerchange():
        try:
            PUMPPWM.setIntensity(pumpintensity.get())
        except ValueError:
            messagebox.showinfo(message='Please type number from 0-100 into Pump text box.')

    # def directorychosen():
    #     try:
    #         global filepath
    #         filepath = filedialog.askdirectory()
    #     except ValueError:
    #         pass

    root = Tk()
    root.title("Coliform Control GUI")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    temp = StringVar()
    PumpPowerStatus = StringVar()
    HeaterPowerStatus = StringVar()
    TempSensorPowerStatus = StringVar()
    pumpintensity = StringVar()

    HeaterPowerStatus.set('Heater OFF')
    PumpPowerStatus.set("Pump OFF")

    masterpane = ttk.Panedwindow(mainframe, orient=VERTICAL)

    toppane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)

    f2 = ttk.Labelframe(toppane, text='Temperature Sensor:', width=100, height=100)
    f3 = ttk.Labelframe(toppane, text='Heater:', width=100, height=100)
    toppane.add(f2)
    toppane.add(f3)
    masterpane.add(toppane)

    templabel = ttk.Label(f2)
    templabel.grid(column=1, row=2, sticky=W)
    ttk.Label(f2, text="Temperature:").grid(column=1, row=1, sticky=W)
    ttk.Button(f2, text='Show Plot', command=tempplot).grid(column=2, row=1, sticky=E)
    ttk.Button(f2, text='Save Data File', command=savefile).grid(column=2, row=2, sticky=(S, E))

    temp_entry = ttk.Entry(f3, width=7, textvariable=temp)
    temp_entry.grid(column=2, row=1, sticky=(W, E))
    ttk.Label(f3, text="Target Temperature:").grid(column=1, row=1, sticky=W)
    heaterbutton = ttk.Button(f3, text="Heater ON", command=heaterpoweron)
    heaterbutton.grid(column=1, row=2, sticky=W)

    bottompane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)
    f1 = ttk.Labelframe(bottompane, text='Status:', width=100, height=100)
    f4 = ttk.Labelframe(bottompane, text='Pump:', width=100, height=100)
    bottompane.add(f4)
    bottompane.add(f1)
    masterpane.add(bottompane)

    pumpbutton = ttk.Button(f4, text="Power ON", command=pumppoweron)
    pumpbutton.grid(column=1, row=1, sticky=W)
    pumpchangebutton = ttk.Button(f4, text="Submit", command=pumppowerchange)
    pumpchangebutton.grid(column=1, row=3, sticky=(W, E))
    pump_entry = ttk.Entry(f4, width=4, textvariable=pumpintensity)
    pump_entry.grid(column=1, row=2, sticky=(W, E))

    ttk.Label(f1, textvariable=TempSensorPowerStatus).grid(column=1, row=1, sticky=(W, E))
    ttk.Label(f1, textvariable=PumpPowerStatus).grid(column=1, row=2, sticky=(W, E))
    ttk.Label(f1, textvariable=HeaterPowerStatus).grid(column=1, row=3, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    temp_entry.focus()
    start_time = time.time()
    onewireon()
    heaterinput()
    root.mainloop()


def startCameraGUI():
    tf = 'PlotTextFile.txt'
    if os.path.isfile(tf):
        os.remove(tf)
    # filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))

    def setnormaloptions():
        try:
            exposuremode.set('')
            shutterspeedvar.set(0)
            # frameratevar.set('25')
            isovar.set(0)
            resolutionvary.set(1944)
            resolutionvarx.set(2592)
            delayvar.set(2)
            brightnessvar.set(50)
            previewtimeout.set(10)
            zoomvar.set('0.0,0.0,1.0,1.0')
            awbvar.set('')

        except ValueError:
            pass

    def setdarkoptions():
        try:
            exposuremode.set('')
            shutterspeedvar.set(6)
            # frameratevar.set('1/6')
            isovar.set(0)
            resolutionvary.set(1944)
            resolutionvarx.set(2592)
            delayvar.set(30)
            brightnessvar.set(50)
            previewtimeout.set(30)
            zoomvar.set('0.0,0.0,1.0,1.0')
            awbvar.set('')
        except ValueError:
            pass

    def picturetaken():
        try:
            # global filename
            # filename = datetime.strftime(datetime.now(),"%Y.%m.%d-%H:%M:%S")+'.jpeg'
            iso = 0
            resolution = '2592, 1944'
            delay = 30
            brightness = 50
            contrast = 0
            shutterspeed = 0

            global rgb_array
            if isovar.get():
                iso = isovar.get()
            if delayvar.get():
                delay = delayvar.get()
            if resolutionvarx.get() and resolutionvary.get():
                resolution = (resolutionvarx.get(), resolutionvary.get())
            if brightnessvar.get():
                brightness = brightnessvar.get()
            if contrastvar.get():
                contrast = contrastvar.get()
            if shutterspeedvar.get():
                shutterspeed = shutterspeedvar.get() * 10**6
            # if frameratevar.get():
            #     if '/' in frameratevar.get():
            #         framelist = frameratevar.get().split('/')
            #         if len(framelist) == 2:
            #             framerate = Fraction(int(framelist[0]), int(framelist[1]))
            #     else:
            #         framerate = int(frameratevar.get())
            rgb_array = RPiCamera.takePicture(iso=iso, timeout=delay, resolution=resolution, exposure=exposuremode.get(),
                                              brightness=brightness, contrast=contrast, shutterspeed=shutterspeed,
                                              zoom=tuple(map(float, zoomvar.get().split(','))), awb_mode=awbvar.get())
            red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(rgb_array)
            intensity_array = '\n'.join(['R:'+'{:.3f}'.format(red_intensity),
                                         'G:'+'{:.3f}'.format(green_intensity),
                                         'B:'+'{:.3f}'.format(blue_intensity),
                                         'I:'+'{:.3f}'.format(intensity)])
            intensitylabel.config(text=intensity_array)

            # messagebox.showinfo(message='JPEG created on directory')
        except (UnboundLocalError, IndexError):
            # messagebox.showinfo(message='Arduino not found, make sure it is connected to USB port')
            pass

    def showimageplot():
        try:
            RPiCamera.showPlot(rgb_array)
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing plot.')

    def showimage():
        try:
            RPiCamera.showImage(rgb_array)
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')
        # except AttributeError:
        #     pass

    def showredimage():
        try:
            RPiCamera.showImage(rgb_array, 'r')
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')
        # except AttributeError:
        #     pass

    def showgreenimage():
        try:
            RPiCamera.showImage(rgb_array, 'g')
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')

    def showblueimage():
        try:
            RPiCamera.showImage(rgb_array, 'b')
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')

    # def directorychosen():
    #     try:
    #         global filepath
    #         filepath = filedialog.askdirectory()
    #     except ValueError:
    #         pass

    def importimage():
        global rgb_array
        rgb_array = RPiCamera.importImage()

        red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(rgb_array)
        intensity_array = '\n'.join(['R:' + '{:.3f}'.format(red_intensity),
                                     'G:' + '{:.3f}'.format(green_intensity),
                                     'B:' + '{:.3f}'.format(blue_intensity),
                                     'I:' + '{:.3f}'.format(intensity)])
        intensitylabel.config(text=intensity_array)

    def saveimage():
        RPiCamera.saveImage(rgb_array)

    def saveallimages():
        foldername = 'ISO={}-Delay={}-Resolution={}x{}-Brightness={}-Contrast={}-ShutterSpeed={}' \
                     '-Exposure={}-AutoWhiteBalance={}-' \
                     'Zoom={}'.format(isovar.get(), delayvar.get(), resolutionvarx.get(), resolutionvary.get(),
                                      brightnessvar.get(), contrastvar.get(),
                                      shutterspeedvar.get(), exposuremode.get(), awbvar.get(), zoomvar.get())
        RPiCamera.saveAllImages(rgb_array, foldername)
        messagebox.showinfo(message='Finished Saving to Directory.')

    def preview():
        iso = 0
        resolution = '2592, 1944'
        brightness = 50
        contrast = 0
        shutterspeed = 0
        # framerate = 25
        timeout = 10

        global rgb_array
        if isovar.get():
            iso = isovar.get()
        if previewtimeout.get():
            timeout = previewtimeout.get()
        if resolutionvarx.get() and resolutionvary.get():
            resolution = (resolutionvarx.get(), resolutionvary.get())
        if brightnessvar.get():
            brightness = brightnessvar.get()
        if contrastvar.get():
            contrast = contrastvar.get()
        if shutterspeedvar.get():
            shutterspeed = shutterspeedvar.get()
        # if frameratevar.get():
        #     if '/' in frameratevar.get():
        #         framelist = frameratevar.get().split('/')
        #         if len(framelist) == 2:
        #             framerate = Fraction(int(framelist[0]), int(framelist[1]))
        #     else:
        #         framerate = int(frameratevar.get())
        #
        RPiCamera.startPreview(iso=iso, timeout=timeout, resolution=resolution, exposure=exposuremode.get(),
                               brightness=brightness, contrast=contrast, shutterspeed=shutterspeed,
                               zoom=tuple(map(float, zoomvar.get().split(','))), awb_mode=awbvar.get())

    # def realtimeplot():
    #     MultiPlot.GeneratePlotDataFile(tf, RPiCamera.returnIntensity(rgb_array), start_time)

    root = Tk()
    root.title("Image Processing GUI")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    isovar = IntVar()
    resolutionvarx = IntVar()
    resolutionvary = IntVar()
    exposuremode = StringVar()
    delayvar = IntVar()
    contrastvar = IntVar()
    brightnessvar = IntVar()
    shutterspeedvar = IntVar()
    # frameratevar = StringVar()
    previewtimeout = IntVar()
    zoomvar = StringVar()
    awbvar = StringVar()

    exposuremode.set('')
    shutterspeedvar.set(0)
    # frameratevar.set('1/6')
    isovar.set(0)
    resolutionvary.set(1944)
    resolutionvarx.set(2592)
    delayvar.set(5)
    brightnessvar.set(50)
    previewtimeout.set(10)
    zoomvar.set('0.0,0.0,1.0,1.0')
    awbvar.set('')

    masterpane = ttk.Panedwindow(mainframe, orient=VERTICAL)

    midpane = ttk.Panedwindow(masterpane, orient=VERTICAL)
    f3 = ttk.Labelframe(midpane, text='Camera Options:',
                        width=100, height=100)
    f4 = ttk.Labelframe(midpane, text='Exposure Modes:', width=100, height=100)
    f2 = ttk.Labelframe(midpane, text='Auto White Balance:', width=100, height=100)
    midpane.add(f3)
    midpane.add(f4)
    midpane.add(f2)
    masterpane.add(midpane)

    ttk.Label(f3, text='Delay: ').grid(column=1, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=delayvar)
    delay_variable.grid(column=2, row=1, sticky=W)

    ttk.Label(f3, text='Brightness: ').grid(column=3, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=brightnessvar)
    delay_variable.grid(column=4, row=1, sticky=W)

    ttk.Label(f3, text='Contrast: ').grid(column=5, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=contrastvar)
    delay_variable.grid(column=6, row=1, sticky=W)

    # ttk.Label(f3, text='Framerate: ').grid(column=7, row=1, sticky=E)
    # delay_variable = ttk.Entry(f3, width=4, textvariable=frameratevar)
    # delay_variable.grid(column=8, row=1, sticky=W)

    ttk.Label(f3, text='Shutter Speed(μs): ').grid(column=1, row=2, sticky=E)
    delay_variable = ttk.Entry(f3, width=6, textvariable=shutterspeedvar)
    delay_variable.grid(column=2, row=2, sticky=W)

    ttk.Label(f3, text='ISO: (max=800)').grid(column=3, row=2, sticky=E)
    iso_variable = ttk.Entry(f3, width=4, textvariable=isovar)
    iso_variable.grid(column=4, row=2, sticky=W)

    ttk.Label(f3, text='Preview Timeout: ').grid(column=5, row=2, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=previewtimeout)
    delay_variable.grid(column=6, row=2, sticky=W)

    ttk.Label(f3, text='Resolution:').grid(column=7, row=2, sticky=E)
    xresolution_variable = ttk.Entry(f3, width=4, textvariable=resolutionvarx)
    xresolution_variable.grid(column=8, row=2, sticky=E)
    ttk.Label(f3, text='x').grid(column=9, row=2)
    yresolution_variable = ttk.Entry(f3, width=4, textvariable=resolutionvary)
    yresolution_variable.grid(column=10, row=2, sticky=W)

    ttk.Label(f3, text='Zoom: ').grid(column=1, row=3, sticky=E)
    delay_variable = ttk.Entry(f3, width=15, textvariable=zoomvar)
    delay_variable.grid(column=2, row=3, sticky=W)

    awbmode_auto = ttk.Radiobutton(f2, text='auto', variable=awbvar, value='auto')
    awbmode_auto.grid(column=1, row=1, sticky=W)

    awbmode_fluorescent = ttk.Radiobutton(f2, text='fluorescent', variable=awbvar, value='fluorescent')
    awbmode_fluorescent.grid(column=2, row=1, sticky=W)

    awbmode_incandescent = ttk.Radiobutton(f2, text='incandescent', variable=awbvar, value='incandescent')
    awbmode_incandescent.grid(column=3, row=1, sticky=W)

    awbmode_off = ttk.Radiobutton(f2, text='off', variable=awbvar, value='off')
    awbmode_off.grid(column=4, row=1, sticky=W)

    awbmode_default = ttk.Radiobutton(f2, text='default', variable=awbvar, value='')
    awbmode_default.grid(column=5, row=1, sticky=W)

    awbmode_sun = ttk.Radiobutton(f2, text='sun', variable=awbvar, value='sun')
    awbmode_sun.grid(column=6, row=1, sticky=W)

    awbmode_cloud = ttk.Radiobutton(f2, text='cloud', variable=awbvar, value='cloud')
    awbmode_cloud.grid(column=7, row=1, sticky=W)

    awbmode_shade = ttk.Radiobutton(f2, text='shade', variable=awbvar, value='shade')
    awbmode_shade.grid(column=1, row=2, sticky=W)

    awbmode_tungsten = ttk.Radiobutton(f2, text='tungsten', variable=awbvar, value='tungsten')
    awbmode_tungsten.grid(column=2, row=2, sticky=W)

    awbmode_flash = ttk.Radiobutton(f2, text='flash', variable=awbvar, value='flash')
    awbmode_flash.grid(column=3, row=2, sticky=W)

    awbmode_horizon = ttk.Radiobutton(f2, text='horizon', variable=awbvar, value='horizon')
    awbmode_horizon.grid(column=4, row=2, sticky=W)

    exposuremode_night = ttk.Radiobutton(f4, text='night', variable=exposuremode, value='night')
    exposuremode_night.grid(column=1, row=1, sticky=W)

    exposuremode_auto = ttk.Radiobutton(f4, text='auto', variable=exposuremode, value='auto')
    exposuremode_auto.grid(column=2, row=1, sticky=W)

    exposuremode_verylong = ttk.Radiobutton(f4, text='verylong', variable=exposuremode, value='verylong')
    exposuremode_verylong.grid(column=3, row=1, sticky=W)

    exposuremode_spotlight = ttk.Radiobutton(f4, text='spotlight', variable=exposuremode, value='spotlight')
    exposuremode_spotlight.grid(column=4, row=1, sticky=W)

    exposuremode_sports = ttk.Radiobutton(f4, text='sports', variable=exposuremode, value='sports')
    exposuremode_sports.grid(column=5, row=1, sticky=W)

    exposuremode_off = ttk.Radiobutton(f4, text='off', variable=exposuremode, value='off')
    exposuremode_off.grid(column=6, row=1, sticky=W)

    exposuremode_default = ttk.Radiobutton(f4, text='default', variable=exposuremode, value='')
    exposuremode_default.grid(column=7, row=1, sticky=W)

    exposuremode_backlight = ttk.Radiobutton(f4, text='backlight', variable=exposuremode, value='backlight')
    exposuremode_backlight.grid(column=1, row=2, sticky=W)

    exposuremode_fireworks = ttk.Radiobutton(f4, text='fireworks', variable=exposuremode, value='fireworks')
    exposuremode_fireworks.grid(column=2, row=2, sticky=W)

    exposuremode_antishake = ttk.Radiobutton(f4, text='antishake', variable=exposuremode, value='antishake')
    exposuremode_antishake.grid(column=3, row=2, sticky=W)

    exposuremode_fixedfps = ttk.Radiobutton(f4, text='fixedfps', variable=exposuremode, value='fixedfps')
    exposuremode_fixedfps.grid(column=4, row=2, sticky=W)

    exposuremode_beach = ttk.Radiobutton(f4, text='beach', variable=exposuremode, value='beach')
    exposuremode_beach.grid(column=5, row=2, sticky=W)

    exposuremode_snow = ttk.Radiobutton(f4, text='snow', variable=exposuremode, value='snow')
    exposuremode_snow.grid(column=6, row=2, sticky=W)

    exposuremode_nightpreview = ttk.Radiobutton(f4, text='nightpreview', variable=exposuremode, value='nightpreview')
    exposuremode_nightpreview.grid(column=7, row=2, sticky=W)

    bottompane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)
    f5 = ttk.Labelframe(bottompane, text='Camera Options:', width=100, height=100)
    f6 = ttk.Labelframe(bottompane, text='Image Data:', width=100, height=100)
    bottompane.add(f5)
    bottompane.add(f6)
    masterpane.add(bottompane)

    ttk.Button(f5, text='Take Picture', command=picturetaken).grid(column=1, row=1, sticky=(W, E))
    ttk.Button(f5, text="Set Normal Options", command=setnormaloptions).grid(column=1, row=2, sticky=(W, E))
    ttk.Button(f5, text="Set Low Light Options", command=setdarkoptions).grid(column=1, row=3, sticky=(W, E))
    ttk.Button(f5, text="Camera Preview", command=preview).grid(column=1, row=4, sticky=(W, E))
    ttk.Button(f5, text="Show Plots", command=showimageplot).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(f5, text="Show Image", command=showimage).grid(column=2, row=1, sticky=(W, E))
    ttk.Button(f5, text="Import Image", command=importimage).grid(column=2, row=3, sticky=(W, E))
    ttk.Button(f5, text="Save Image", command=saveimage).grid(column=2, row=4, sticky=(W, E))
    ttk.Button(f5, text="Show Red", command=showredimage).grid(column=3, row=1, sticky=(W, E))
    ttk.Button(f5, text="Show Green", command=showgreenimage).grid(column=3, row=2, sticky=(W, E))
    ttk.Button(f5, text="Show Blue", command=showblueimage).grid(column=3, row=3, sticky=(W, E))
    ttk.Button(f5, text="Save All", command=saveallimages).grid(column=3, row=4, sticky=(W, E))

    ttk.Label(f6, text="Intensity: ").grid(column=1, row=1, sticky=(W, E))
    intensitylabel = ttk.Label(f6, text='Not Taken')
    intensitylabel.grid(column=1, row=2, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # start_time = time.time()
    root.mainloop()


def startRGBSensorGUI():
    tf = 'PlotTextFile.txt'
    if os.path.isfile(tf):
        os.remove(tf)
    # filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))

    def setnormaloptions():
        try:
            integrationvar.set('2.4')
            gainvar.set(1)

        except ValueError:
            pass

    def setdarkoptions():
        try:
            integrationvar.set('700')
            gainvar.set(60)
        except ValueError:
            pass

    def capturedata():
        try:
            global red_intensity, green_intensity, blue_intensity, clear_unfiltered, lux, color_temperature
            red_intensity, green_intensity, blue_intensity, clear_unfiltered, lux, color_temperature = RGBSensor.Capture(integrationtime=float(integrationvar.get()), gain=gainvar.get())
            intensity_array = '\n'.join(['R:'+'{}'.format(red_intensity),
                                         'G:'+'{}'.format(green_intensity),
                                         'B:'+'{}'.format(blue_intensity),
                                         'Clear:'+'{}'.format(clear_unfiltered),
                                         'Luminosity:{} lux'.format(lux),
                                         'Color Temperature:{} K'.format(color_temperature)])
            intensitylabel.config(text=intensity_array)

        except AttributeError:
            messagebox.showinfo(message='Too dark to determine color temperature.')

    # def directorychosen():
    #     try:
    #         global filepath
    #         filepath = filedialog.askdirectory()
    #     except ValueError:
    #         pass

    # def importimage():
    #     global rgb_array
    #     rgb_array = RPiCamera.importImage()
    #
    #     red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(rgb_array)
    #     intensity_array = '\n'.join(['R:' + '{:.3f}'.format(red_intensity),
    #                                  'G:' + '{:.3f}'.format(green_intensity),
    #                                  'B:' + '{:.3f}'.format(blue_intensity),
    #                                  'I:' + '{:.3f}'.format(intensity)])
    #     intensitylabel.config(text=intensity_array)

    def savedata():
        # foldername = 'ISO={}-Delay={}-Resolution={}x{}-Brightness={}-Contrast={}-ShutterSpeed={}' \
        #              '-Exposure={}-AutoWhiteBalance={}-' \
        #              'Zoom={}'.format(isovar.get(), delayvar.get(), resolutionvarx.get(), resolutionvary.get(),
        #                               brightnessvar.get(), contrastvar.get(),
        #                               shutterspeedvar.get(), exposuremode.get(), awbvar.get(), zoomvar.get())
        RGBSensor.saveData(red_intensity, green_intensity, blue_intensity, clear_unfiltered, lux, color_temperature)
        messagebox.showinfo(message='Finished Saving to Directory.')

    # def realtimeplot():
    #     MultiPlot.GeneratePlotDataFile(tf, RPiCamera.returnIntensity(rgb_array), start_time)

    root = Tk()
    root.title("RGB Sensor GUI")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    gainvar = IntVar()
    integrationvar = StringVar()

    gainvar.set(1)
    integrationvar.set('2.4')

    masterpane = ttk.Panedwindow(mainframe, orient=VERTICAL)

    midpane = ttk.Panedwindow(masterpane, orient=VERTICAL)
    f4 = ttk.Labelframe(midpane, text='Gain:', width=100, height=100)
    f2 = ttk.Labelframe(midpane, text='Integration Time:', width=100, height=100)
    midpane.add(f2)
    midpane.add(f4)
    masterpane.add(midpane)

    integration2_4 = ttk.Radiobutton(f2, text='2.4ms', variable=integrationvar, value='2.4')
    integration2_4.grid(column=1, row=1, sticky=W)

    integration24 = ttk.Radiobutton(f2, text='24ms', variable=integrationvar, value='24')
    integration24.grid(column=2, row=1, sticky=W)

    integration50 = ttk.Radiobutton(f2, text='50ms', variable=integrationvar, value='50')
    integration50.grid(column=3, row=1, sticky=W)

    integration101 = ttk.Radiobutton(f2, text='101ms', variable=integrationvar, value='101')
    integration101.grid(column=4, row=1, sticky=W)

    integration154 = ttk.Radiobutton(f2, text='154ms', variable=integrationvar, value='154')
    integration154.grid(column=5, row=1, sticky=W)

    integration700 = ttk.Radiobutton(f2, text='700ms', variable=integrationvar, value='700')
    integration700.grid(column=6, row=1, sticky=W)

    gain1 = ttk.Radiobutton(f4, text='1X', variable=gainvar, value=1)
    gain1.grid(column=1, row=1, sticky=W)

    gain4 = ttk.Radiobutton(f4, text='4X', variable=gainvar, value=4)
    gain4.grid(column=2, row=1, sticky=W)

    gain16 = ttk.Radiobutton(f4, text='16X', variable=gainvar, value=16)
    gain16.grid(column=3, row=1, sticky=W)

    gain60 = ttk.Radiobutton(f4, text='60X', variable=gainvar, value=60)
    gain60.grid(column=4, row=1, sticky=W)

    bottompane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)
    f5 = ttk.Labelframe(bottompane, text='Sensor Options:', width=100, height=100)
    f6 = ttk.Labelframe(bottompane, text='RGB Data:', width=100, height=100)
    bottompane.add(f5)
    bottompane.add(f6)
    masterpane.add(bottompane)

    ttk.Button(f5, text='Capture Data', command=capturedata).grid(column=1, row=1, sticky=(W, E))
    ttk.Button(f5, text="Set Normal Options", command=setnormaloptions).grid(column=1, row=2, sticky=(W, E))
    ttk.Button(f5, text="Set Low Light Options", command=setdarkoptions).grid(column=1, row=3, sticky=(W, E))
    # ttk.Button(f5, text="Show Plots", command=showimageplot).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(f5, text="Save Data", command=savedata).grid(column=1, row=4, sticky=(W, E))

    intensitylabel = ttk.Label(f6, text='Not Taken')
    intensitylabel.grid(column=1, row=1, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # start_time = time.time()
    root.mainloop()
