# aris-repo-4


# Vision Directory
## 0. pip install 
`pip install ultralytics`

`pip install opencv-python`

`pip install opencv-contrib-python` (`$ pip list | grep opencv`)
- [AttributeError: module 'cv2.aruco' has no attribute 'detectMarkers'](https://stackoverflow.com/questions/76186376/attributeerror-module-cv2-aruco-has-no-attribute-detectmarkers-python)

## 1. xy-coordinates
- #### pixel of xy = 640 * 480

![xy_coordinate](https://github.com/user-attachments/assets/99035a00-22e7-45a0-8d4a-cc4a04071353)

- #### bounding box

(x1,y1) = left top

(x2,y2) = right bottom

### position of jig (pixel)
> example

> fixed : 20 <= y <= 100

> - jig[0] : 480 <= x <= 580    (Xc,Yc) = (527,35)
> - jig[1] : 380 <= x <= 480    (Xc,Yc) = (427,35)
> - jig[2] : 280 <= x <= 380    (Xc,Yc) = (326,35)

## 2. yolov8 model
- #### bbox.pt (bounding box)
names {0: 'cup', 1: 'hand', **2: 'ice cream'**, 3: 'robot'}
- #### segmentation.pt
names {0: 'cup', **1: 'ice cream'**, 2: 'robot', 3: 'hand'}
- #### trash.pt
names {0: 'Glass', 1: 'Metal', 2: 'Paper', 3: 'Plastic', 4: 'Waste', 5: 'cup', **6: 'ice cream'**, 7: 'robot', 8: 'hand'}

> names for `def JigPosition`