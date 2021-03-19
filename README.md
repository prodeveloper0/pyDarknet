# pyDarknet
This is Python wrapper library for Darknet which is a deep neural network framework by AlexeyAB running YOLO object detector.

This is implemented by `ctypes` and you can use complied shared library file (`libdark.so` / `darknet.dll`) on Darknet directely in you Python project.

# Requirements
* opencv-python

```bash
pip install -r requirements.txt
```

# Usages
## How to import `pyDarknet` on your project.
1. Copy compiled shared library file to on your project.
2. Rename the shared library file `libdarknet-gpu.so` or `libdarknet.so`.
     * pyDarknet selects `libdarknet-gpu.so` supporting GPU acceleration first. If there's no library surpoting GPU acceleration, pyDarknet select `libdarknet.so` alternatively.  
    * pyDarknet can detect shared library extensions by operating systems.  
    e.g.) `libdarknet.so` is for Linux, `libdarknet.dll` is for Windows.
3. Just import `pydarknet` package on your project.
    ```python
    import pydarknet
    ```
## How to load `YOLOv4` by `pyDarknet`.
It's simple. Just create a `Detector`.
```python
detector = pydarknet.Detector('yolov4.cfg', 'yolov4.weights', 'coco.names')
```
`cfg_filename` and `weights_filename` assigned as each `yolov4.cfg` and `yolov4.weights` must be filled. On the other hand, `names_filename` assigned as `coco.names` can be keep empty by passing `None`.

## How to detect objects by `YOLOv4` created by `pyDarknet`.
1. Prepare or load image.  
    * The input must have **HWC** shape.  
    * The input must be 3 channel BGR (**NOT RGB**) image commonly used in OpenCV.  

    If you are using OpenCV mainly, you can use ```cv2.imread``` / ```cv2.imdecode```.  
    ```python
    import cv2
    img = cv2.imread('image.png', cv2.IMREAD_COLOR)
    ```  
2. Call `detect` method in `Detector`.  
    ```python
    bboxes = detector.detect(img)
    ```
    `detect` method has `obj_thres`, `hier_thresh`, `nms_thresh` and `obj_filter`.  
    Three threshold paramaters having a posfix as `_thresh` are object detection paramaters. You can refence original paper or repository.  

    `obj_filter` is an option filtering bounding boxes you want by object names. It is must be list of object names or indices.  
    ```python
    detector.detect(..., obj_filter=['car', 'bus'])
    ```
    or
    ```python
    detector.detect(..., obj_filter['1', '2'])
    ```

## Results of Detector
The detector returns list of tuples like `(name, prob, gebox)`.  
```python
for name, prob, geobox in bboxes:
    x, y, w, h = geobox
```
_What is `geobox`? To distinguish a **bounding box** including both **name** and **geometry informations** on image and a box including only **geometry informations** on image. I called the latter `geobox`._

`name` is detected object name defined in `.names` file. if you not set `.names` file in the detector, `name` is object index (_NOT A **NUMBER**, BUT A **STRING** PRESENTATION NUMBER_) defined in the model.