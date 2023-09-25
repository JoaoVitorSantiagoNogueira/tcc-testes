## Animation Frame Colouring With GANs
Paper to be released

### Introduction:
We are following up on a research conducted in [another paper](https://arxiv.org/abs/1904.09527),to use Generative Adversarial Networks to automatically colorize animation frames. 
The code present in this repository was originally done by the authors of that paper, and were further modified by us to attend our needs. Changes include:

-Shot separation
-Updated Libraries
-No random "Blank" frames throughout the training
-Using only the first frame as a colour reference

## Prerequisites
- Python 3
- PyTorch 1.0
- NVIDIA GPU + CUDA cuDNN

## Installation
- Clone this repo:
pip install -r requirements.txt
```
### Dataset:
You'll need to extract the frames you'll use to train the network. Ther is a scritp [FrameExtraction.py]('FrameExtraction.py') that helps this process in which a path to the video file and output folder for the extracted frames can be specified. Additionally, you'll have to split those frames in various folders corresponding to a 'shot', a frame sequence without cuts or transtions. This process will be automated latter, but by now it needs to be done by hand. 

### Training
To train the model, place the dataset folder in the same folder of your repository which will be used as the root path during training and testing. Run the following in terminal to begin the training process. Checkpoints are saved every epoch by default and samples are produced in the root directory every 250 iterations. Refer to the argument parser in [Train.py]('Train.py') for more configurability options. 
```bash
python train.py \
  --root [path to root directory (location of repo)] \
  --dataset [name of dataset folder in root directory] \
  --logfile [name of logfile to be generated to keep track of losses] \
  --checkpoint_path_G [loading a pretrained generator] \
  --checkpoint_path_D [loading a pretrained discriminator] \
  --batchSize [size of batch] \
```

## Citation
If you use this code for your research, please cite our paper /<TO BE PUBLISHED/>.
