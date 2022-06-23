import tkinter
import cv2
from PIL import Image, ImageTk
import sys
import sys
sys.path.append('/home/gregosh/Instalacyjne/librealsense/wrappers/python')


import pyrealsense2 as rs
import numpy as np


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

color_path = 'experiment_rgb.avi'
depth_path = 'experiment_depth.avi'

colorwriter = cv2.VideoWriter(color_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (1920, 1080), 1)
depthwriter = cv2.VideoWriter(depth_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (1920, 1080), 0)

# Start streaming
profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

align_to = rs.stream.color
align = rs.align(align_to)


window = tkinter.Tk()
window.title('RealSense Recorder')
        
window.geometry("1050x550")
window.eval('tk::PlaceWindow . center')
window.columnconfigure(0, weight=1)
window.columnconfigure(3, weight=1)
window.rowconfigure(0,weight=1)
                  
            
def b1clicked():
    print('Preview')
    video_loop()
            
def b2clicked():
    print('Record')
    show_entry_fields()
    try:
         vidprev 
    except NameError:
        print('No preview present ...')
    else:
        window.after_cancel(vidprev)
    record_video_loop()
            
def b3clicked():
    print('Stopped ...')
    window.after_cancel(vidrec)
    pipeline.stop()
    
def b4clicked():
    print('Files names ...')
    color_path = e1.get()
    depth_path = e2.get()
            
def redirector(inputstring):
    textbox.insert(tkinter.INSERT, inputstring)   
    textbox.see(tkinter.END)
            
def show_entry_fields():
    print('Video file: {0}\nDepth file: {1}'.format(e1.get(), e2.get()))
    
def preview_video_loop():
    
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
            
    #depth_frame = frames.get_depth_frame()
    #color_frame = frames.get_color_frame()
    #if not depth_frame or not color_frame:
    #    continue
    
    # Convert images to numpy array
    #depth_image = np.asanyarray(depth_frame.get_data())
    #color_image = np.asanyarray(color_frame.get_data())
            
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
            
    #if not aligned_depth_frame or not color_frame:
    #    continue
                
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
            
            
    depth_image_8U = cv2.convertScaleAbs(depth_image, alpha=0.03)
    #print(type(depth_image_8U))
    #print(depth_image_8U.shape)
        
    #colorwriter.write(color_image)
    #depthwriter.write(depth_image_8U)
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    
    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape
    
    # If depth and color resolutions are different, resize color image to match depth image for display
    #if depth_colormap_dim != color_colormap_dim:
    #    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
    #    images = np.hstack((resized_color_image, depth_colormap))
    #else:
    #    images = np.hstack((color_image, depth_colormap))
    global image1, img1
    image1 = (Image.fromarray(color_image)).resize((440,330), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(image1)
    print(color_image.shape)
    print(type(img1))
    #canvas1.create_image(0,0, image=img1, anchor='nw')
    canvas1.itemconfig(imageoncanvas1, image=img1)
    
    global image2, img2
    image2 = (Image.fromarray(depth_colormap)).resize((440,330), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(image2)
    canvas2.itemconfig(imageoncanvas2, image=img2)
    global vidprev
    vidprev = window.after(30, preview_video_loop)
  

def record_video_loop():
    
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
            
    #depth_frame = frames.get_depth_frame()
    #color_frame = frames.get_color_frame()
    #if not depth_frame or not color_frame:
    #    continue
    
    # Convert images to numpy array
    #depth_image = np.asanyarray(depth_frame.get_data())
    #color_image = np.asanyarray(color_frame.get_data())
            
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
            
    #if not aligned_depth_frame or not color_frame:
    #    continue
                
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
            
            
    depth_image_8U = cv2.convertScaleAbs(depth_image, alpha=0.03)
    #print(type(depth_image_8U))
    #print(depth_image_8U.shape)
        
    #colorwriter.write(color_image)
    #depthwriter.write(depth_image_8U)
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    
    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape
    
    # If depth and color resolutions are different, resize color image to match depth image for display
    #if depth_colormap_dim != color_colormap_dim:
    #    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
    #    images = np.hstack((resized_color_image, depth_colormap))
    #else:
    #    images = np.hstack((color_image, depth_colormap))

    colorwriter.write(color_image)
    depthwriter.write(depth_image_8U)
    global vidrec
    vidrec = window.after(30, record_video_loop)


        
sys.stdout.write = redirector
        
#image1p = Image.open("tiger1.jpg").resize((400,350))
#img1p = ImageTk.PhotoImage(image1p)
        
#image2 = Image.open("tiger2.jpg").resize((400,350))
#img2 = ImageTk.PhotoImage(image2)

canvas1 = tkinter.Canvas(window, width=400, height=350, bg='red')     
#canvas1 = tkinter.Canvas(width=400, height=350, bg='black')
canvas1.grid(column=0, row=0, columnspan=2, rowspan=9, sticky='NSEW')
#canvas1.create_image(0,0,image=img1, anchor='nw')
imageoncanvas1 = canvas1.create_image(0, 0, anchor='nw')
  
     
canvas2 = tkinter.Canvas(width=400, height=350, bg='green')
canvas2.grid(column=3,row=0, columnspan=2, rowspan=9, sticky='NSEW')
#canvas2.create_image(0,0,image=img2, anchor='nw')
imageoncanvas2 = canvas2.create_image(0, 0, anchor='nw')
        
b1 = tkinter.Button(text='Preview', command=preview_video_loop)
b2 = tkinter.Button(text='Record', command=b2clicked)
b3 = tkinter.Button(text='Stop', command=b3clicked)
b4 = tkinter.Button(text="Set names", command=b4clicked)
        
b1.grid(column=5, row=0, sticky='WE')
b2.grid(column=5, row=1, sticky='WE')
b3.grid(column=5, row=3, sticky='WE')
b4.grid(column=5, row=8, sticky='WE')

l1 = tkinter.Label(text="Video file:")
l2 = tkinter.Label(text="Depth file:")

e1 = tkinter.Entry()
e2 = tkinter.Entry()

l1.grid(column=5, row=4, sticky='WE')
e1.grid(column=5, row=5, sticky='WE')

l2.grid(column=5, row=6)
e2.grid(column=5, row=7)

textbox = tkinter.Text(height=7)
textbox.grid(column=0, row=9, columnspan=4)

          
window.mainloop()