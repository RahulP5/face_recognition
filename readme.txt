Required Libraries Installation:

((Installing OpenCV For Python:2
[sudo apt-get install python-opencv]))



Install dlib on the Raspberry Pi:

Step #1: Update swap file size, boot options, and memory split

a.Increase swap file size:

[sudo nano /etc/dphys-swapfile]
CONF_SWAPSIZE=100
update it to use 1024MB rather than 100MB
(After Change size hit ctrl+x then y then hit Enter)

After you have updated the /etc/dphys-swapfile  file, 
run the following two commands to restart the swap service:
[sudo /etc/init.d/dphys-swapfile stop]
[sudo /etc/init.d/dphys-swapfile start]

To confirm that your swap size has been increased.
[free -m]

b.Change your boot options:
[sudo raspi-config]
And then select
 
[Boot Options => Desktop / CLI => Console Autologin]
This will ensure that your Raspberry Pi boots directly to a terminal

However, before you exit raspi-config , be sure to update your memory split, as detailed below.

c.Update your memory split:

This is simple enough using raspi-config . 
Go back to the main screen
select [Advanced Options => Memory Split , where you’ll see the 64MB/128MB prompt]
Update this value to be 16MB/64MB and then exit.

Restart your Raspberry Pi.

After Reboot Rpi.

Step #2: Install dlib prerequisites

[sudo apt-get update]
[sudo apt-get install build-essential cmake]
[sudo apt-get install libgtk-3-dev]
[sudo apt-get install libboost-all-dev]

The pip  command should already be installed on your Raspberry Pi 
(you can verify this by executing the pip  command and ensuring that it does indeed exist) 
— otherwise, you can install pip  via:

[wget https://bootstrap.pypa.io/get-pip.py]
[sudo python get-pip.py]

Step #3: Use pip to install dlib with Python bindings:

[sudo pip install numpy]
[sudo pip install scipy]
[sudo pip install scikit-image]
[sudo pip install imutils]
[sudo pip install dlib]

On my Raspberry Pi 3+, this compile took approximately 1hr.

Step #4: Reset your swap file size, boot options, and memory split:

Important — before you walk away from your machine, 
be sure to reset your swap file size to 100MB 
(using the process detailed in the “Step #1: Increase swap file size” section above).

You can then reset your GPU/RAM split to 64MB as well as update the boot options 
to boot into the desktop interface versus the command line.

[Boot Options => Desktop / CLI => Desktop Autologin]
This will ensure that your Raspberry Pi boots again in desktop mode

After making these changes, reboot your Raspberry Pi to ensure they take affect.




*************************************************************************************

dataset/ : 
This directory should contain sub-directories for each person you would like your facial recognition system to recognize.
(dataset/rahul/0001.jpg)

How to create a custom face recognition dataset:

Method #1: Face enrollment via OpenCV and webcam:

This first method to create your own custom face recognition dataset is appropriate when:

1.You are building an “on-site” face recognition system
2.And you need to have physical access to a particular person to gather example images of their face

Such a system would be typical for companies, schools, 
or other organizations where people need to physically show up and attend every day.

To gather example face images of these people, we may escort them to a special room where a video camera is setup to (1) 
detect the (x, y)-coordinates of their face in a video stream and (2) write the frames containing their face to disk.

We may even perform this process over multiple days or weeks to gather examples of their face in:

1.Different lighting conditions
2.Times of day
3.Moods and emotional states
…to create a more diverse set of images representative of that particular person’s face.

path of your project(where all files are saved>cd path/

(e.g.= pi@raspberry:~/facerec $  )
after selection path run following command in terminal

in file manager first create folder name with dataset
in dataset folder create folder with person name

for create folder use [mkdir <foldername>]

[e.g. pi@raspberry:~/facerec $ mkdir dataset]
this command creates dataset folder inside facerec folder

[e.g. pi@raspberry:~/facerec/dataset $ mkdir Rahul]
this command creates Rahul folder inside dataset folder

for delete folder use [rm -rf mydir]
[e.g. pi@raspberry:~/facerec/dataset $ rm -rf Rahul1]


[python build_face_dataset.py --cascade haarcascade_frontalface_default.xml --output dataset/rahul]
--output dataset/rahul=store captured images in dataset/rahul folder

after run above command press 
K=capture and keep image
q=quit

(The “k” key must be pressed for each frame  we’d like to “keep”. 
I recommend keeping frames of your face at different angles, areas of the frame)


after capturing person images run following command.

[python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog]


After running the script, you’ll have a pickle file at your disposal. Mine is named   encodings.pickle  
— this file contains the 128-d face embeddings for each face in our dataset.
(The --detection-method cnn  will not work on a Raspberry Pi,
 but certainly can be used if you’re encoding your faces with a capable machine.)



at last run follow command it will start video stream and dect faces.
[python face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle]






Our face recognition pipeline is running at approximately 1-2 FPS. 
The vast majority of the computation is happening when a face is being recognized, 
not when it is being detected. Furthermore,the more faces in the dataset,
the more comparisons are made for the voting process, 
resulting in slower facial recognition.



















