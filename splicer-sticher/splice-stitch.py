import cv2
from math import floor, ceil
import os



def splice(source_path, v_splits, h_splits, intesection, target_path):
     
    # iterrate through images
    # check all files and if they are images
    valid_images = [".jpg",".png"]
    for f in os.listdir(source_path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue

        #read the images
        image = cv2.imread(source_path + f)
        #define splits
        v_radious  = image.shape[1]/(v_splits-(intesection*v_splits)+intesection)
        v_distance = v_radious * (1-intesection)

        h_radious  = image.shape[0]/(h_splits-(intesection*h_splits)+intesection)
        h_distance = h_radious * (1-intesection)

        text = ""



        for i in range (0, v_splits):
            for j in range (0, h_splits):
                start_v = floor (v_distance*i)
                end_v   = ceil  (start_v + v_radious)

                start_h = floor (h_distance*j)
                end_h   = ceil  (start_h + h_radious)

                if (end_h > image.shape[0]):
                    end_h = image.shape[0]

                if (end_v > image.shape[1]):
                    end_v = image.shape[1]

                croped = image [start_h:end_h,start_v:end_v]

                dir = target_path + "\\" + str(i) + "\\" +str(j)+ "\\"
                os.makedirs(dir, exist_ok=True)
                dir += f

                cv2.imwrite(dir, croped) 
                print (dir)

                #text += f_name + "=" + str(start_v)+ "-" + str(end_v)+ ","  + str(start_h)+ "-" + str(end_h) + "\n"


    with open('reconstruct.txt', 'w') as f:
        f.write(text)

splice('D:\Files\FACUL\TCC\TCVC-master\img root\c/val/', 3, 3, 0.5, "D:\Files\FACUL\TCC\TCVC-master\splicer-sticher")