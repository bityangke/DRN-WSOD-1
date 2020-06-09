# Enabling Deep Residual Networks for Weakly Supervised Object Detection

This project is based on [Detectron](https://github.com/facebookresearch/Detectron).


## License

DRN-WSOD is released under the [Apache 2.0 license](https://github.com/DRN-WSOD/DRN-WSOD/blob/DRN-WSOD/LICENSE). See the [NOTICE](https://github.com/DRN-WSOD/DRN-WSOD/blob/DRN-WSOD/LICENSE) file for additional details.


## Installation

**Requirements:**

- NVIDIA GPU, Linux, Python3.6
- Caffe2 in pytorch v1.5.0, various standard Python packages, and the COCO API; Instructions for installing these dependencies are found below

### Caffe2

Clone the pytorch repository:
```
# pytorch=/path/to/clone/pytorch
git clone https://github.com/pytorch/pytorch.git $pytorch
cd $pytorch
git checkout v1.5.0
git submodule update --init --recursive
```

Install Python dependencies:
```
pip3 install -r $pytorch/requirements.txt
```

Build caffe2:
```
cd $pytorch
sudo USE_OPENCV=On USE_LMDB=On BUILD_BINARY=On python3 setup.py install
```


### Other Dependencies

Install the [COCO API](https://github.com/cocodataset/cocoapi):
```
pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
```

Install the [pycococreator](https://github.com/waspinator/pycococreator):
```
pip3 install git+git://github.com/waspinator/pycococreator.git@0.2.0
```


### DRN-WSOD

Clone the DRN-WSOD repository:
```
# DRN-WSOD=/path/to/clone/DRN-WSOD
git clone https://github.com/DRN-WSOD/DRN-WSOD.git $DRN-WSOD
cd $DRN-WSOD
git submodule update --init --recursive
```

Install Python dependencies:
```
pip3 install -r requirements.txt
```

Set up Python modules:
```
make
```

Build the custom C++ operators library:
```
./build_ops.sh
```


### Dataset Preparation
Please follow [this](https://github.com/DRN-WSOD/DRN-WSOD/blob/DRN-WSOD/detectron/datasets/data/README.md#creating-symlinks-for-pascal-voc) to creating symlinks for PASCAL VOC.

Download proposals ([MCG](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/mcg/) or Selective Search or Edge Boxes) to detectron/datasets/data, and transform it to pickle serialization format:
```
cd detectron/datasets/data
tar xvzf MCG-Pascal-Main_trainvaltest_2007-boxes.tgz
cd ../../../
python3 tools/convert_mcg.py voc_2007_train detectron/datasets/data/MCG-Pascal-Main_trainvaltest_2007-boxes detectron/datasets/data/proposals/mcg_voc_2007_train.pkl
python3 tools/convert_mcg.py voc_2007_val detectron/datasets/data/MCG-Pascal-Main_trainvaltest_2007-boxes detectron/datasets/data/proposals/mcg_voc_2007_val.pkl
python3 tools/convert_mcg.py voc_2007_test detectron/datasets/data/MCG-Pascal-Main_trainvaltest_2007-boxes detectron/datasets/data/proposals/mcg_voc_2007_test.pkl
```


### Model Preparation

Download models from this [here](https://1drv.ms/u/s!AodeRhn8mpxoh1-VUIt27bZumzqQ?e=QalzaB) and untar File:
```
tar xvf models.tar
mv models $DRN-WSOD
```

Then we have the following directory structure:
```
DRN-WSOD
|_ models
|  |_ DRN-WSOD
|     |_ resnet18_ws_model_120.pkl
|     |_ resnet150_ws_model_120.pkl
|     |_ resnet101_ws_model_120.pkl
|_ ...
```


## Quick Start: Using DRN-WSOD

### WSDDN

ResNet18-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/wsddn_R-18-WS-C5_1x.yaml OUTPUT_DIR experiments/wsddn_r-18-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet50-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/wsddn_R-50-WS-C5_1x.yaml OUTPUT_DIR experiments/wsddn_r-50-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet101-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/wsddn_R-101-WS-C5_1x.yaml OUTPUT_DIR experiments/wsddn_r-101-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

VGG16
```
./scripts/train_wsl.sh --cfg configs/voc_2007/wsddn_V-16-C5_1x.yaml OUTPUT_DIR experiments/wsddn_v-16_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

### ContextLocNet

ResNet18-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/contextlocnet_R-18-WS-C5_1x.yaml OUTPUT_DIR experiments/contextlocnet_r-18-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet50-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/contextlocnet_R-50-WS-C5_1x.yaml OUTPUT_DIR experiments/contextlocnet_r-50-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet101-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/contextlocnet_R-101-WS-C5_1x.yaml OUTPUT_DIR experiments/contextlocnet_r-101-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

VGG16
```
./scripts/train_wsl.sh --cfg configs/voc_2007/contextlocnet_V-16-C5_1x.yaml OUTPUT_DIR experiments/contextlocnet_v-16_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

### OICR

ResNet18-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/oicr_R-18-WS-C5_1x.yaml OUTPUT_DIR experiments/oicr_r-18-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet50-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/oicr_R-50-WS-C5_1x.yaml OUTPUT_DIR experiments/oicr_r-50-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet101-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/oicr_R-101-WS-C5_1x.yaml OUTPUT_DIR experiments/oicr_r-101-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

VGG16
```
./scripts/train_wsl.sh --cfg configs/voc_2007/oicr_V-16-C5_1x.yaml OUTPUT_DIR experiments/oicr_v-16_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

### PCL

ResNet18-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/pcl_R-18-WS-C5_1x.yaml OUTPUT_DIR experiments/pcl_r-18-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet50-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/pcl_R-50-WS-C5_1x.yaml OUTPUT_DIR experiments/pcl_r-50-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet101-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/pcl_R-101-WS-C5_1x.yaml OUTPUT_DIR experiments/pcl_r-101-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

VGG16
```
./scripts/train_wsl.sh --cfg configs/voc_2007/pcl_V-16-C5_1x.yaml OUTPUT_DIR experiments/pcl_v-16_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

### CMIL

ResNet18-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/cmil_R-18-WS-C5_1x.yaml OUTPUT_DIR experiments/cmil_r-18-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet50-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/cmil_R-50-WS-C5_1x.yaml OUTPUT_DIR experiments/cmil_r-50-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

ResNet101-WS
```
./scripts/train_wsl.sh --cfg configs/voc_2007/cmil_R-101-WS-C5_1x.yaml OUTPUT_DIR experiments/cmil_r-101-ws_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```

VGG16
```
./scripts/train_wsl.sh --cfg configs/voc_2007/cmil_V-16-C5_1x.yaml OUTPUT_DIR experiments/cmil_v-16_voc2007_`date +'%Y-%m-%d_%H-%M-%S'`
```
