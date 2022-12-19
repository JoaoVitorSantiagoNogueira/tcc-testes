from genericpath import isdir
from os import listdir, walk
from os.path import join, exists
from PIL import Image
from matplotlib.pyplot import pause
import numpy as np
import torch
import torch.utils.data as data
import torchvision.transforms as transforms
import random

import PIL

from skimage import io, feature, color, img_as_uint, util
from skimage.transform import resize
from .util import is_image_file, load_img


class DatasetFromFolder(data.Dataset):


    def __init__(self, image_dir, bbox = (0,0,1,1)):
        super(DatasetFromFolder, self).__init__()
        self.photo_path = image_dir

        #bounding box information
        self.set_region(bbox)
        self.frame_sum = 0

        #addition for scenes
        self.scenes = [image_dir + "\\" + x + "\\" for x in next(walk(image_dir))[1]] 

        ### create image files lists and randomize scene order
        self.image_filenames_tests = [[y + x for x in listdir(y) if is_image_file(x)] for y in self.scenes]
        self.shuffled_scenes = []
        self.next_scene()
        transform_list = [transforms.ToTensor(),transforms.ConvertImageDtype(torch.float32)]
        #transform_list = [transforms.ToTensor()]
        self.transform = transforms.Compose(transform_list)
        

    def __getitem__(self, index):
        # Load Image
        try:

            index_corrected = index - self.frame_sum

            
            #index is sequential, but the data set is not, so we have to decrement it after every scene
            if index_corrected >= len(self.current_scene) or index_corrected < 0:
                self.next_scene()
                #make sure it's updated
                index_corrected = index - self.frame_sum

            ## we need to add the scene name to path as well


            target_path = join(self.photo_path, self.current_scene[index_corrected])

            frame_num = target_path.split("e")[-1]
            frame_num = int(frame_num.split(".")[0]) - 1

            ### get first frame from scene
            frame_prev = self.prev

            target = load_img(target_path, bbox = self.bbox)
            #target = load_img(target_path)

            '''
            from matplotlib import pyplot as plt
            plt.imshow(target, interpolation='nearest')
            plt.show()
            pause()
            '''
            #cv2.imshow(frame_prev)

            #çççç TODO change image representation, don't want to deal with real time cnversions nor file system
            input = color.rgb2gray(target)

            '''
            #Lineart
            input = feature.canny(input,sigma = 1)  
            input = util.invert(input)
            input = Image.fromarray(np.uint8(input)*255)
            '''
            #line art        
            input = Image.fromarray(input)
            #previous frame
            frame_prev = self.transform(frame_prev)
            #real image
            target = self.transform(target)
            input = self.transform(input)

            return input, target, frame_prev
        except:
            print("Something went wrong frame:" + str(frame_num))
            return self[0]

    def __len__(self):
        return sum([len(x) for x in self.image_filenames_tests])


    #unnused
    #def get_prev(self, num):
    #    if not exists(join(self.photo_path,"frame"+str(num)+".jpg")):
    #        initial_prev_frame = Image.new("RGB",[256,256])
    #        return initial_prev_frame
    #    else:
    #        #define rnd num generator and if statement <0.5 take black or color
    #        rnd = np.random.uniform(0,1)
    #        if rnd <= 0.5:
    #            ### added box parameters ççç
    #            prev = load_img(join(self.photo_path,"frame"+str(num)+".jpg"), bbox = self.bbox)
    #        else:
    #            prev = Image.new("RGB",[256,256])
    #
    #        return prev

    def set_region(self, bbox):
        self.bbox = bbox

    def random_scene_order(self, scenes):
        shuffled_scenes_tmp = scenes[:] #error, for some f-ing reson
        random.shuffle(shuffled_scenes_tmp)
        return shuffled_scenes_tmp

    def next_scene(self):
        if ( len(self.shuffled_scenes) == 0):
            #reset the data set, and refresh the scene count
            self.shuffled_scenes = self.random_scene_order(self.image_filenames_tests)
            self.frame_sum = 0
            #also make sure the very first frame remains as out target
            self.prev = load_img(self.shuffled_scenes[0][0], bbox = self.bbox)
            self.prev
        else:
            #if we need to get a new scene, we need to decrement index by the frames in the scene
            self.frame_sum += len(self.current_scene)


        self.current_scene = self.shuffled_scenes.pop(0)
