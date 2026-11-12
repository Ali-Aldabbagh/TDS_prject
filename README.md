# Depth-Vision Terrain Detection for Wearable Locomotion Assistance

Real-time terrain recognition from a chest-mounted depth camera, built during my Ph.D. at
**Université catholique de Louvain (UCLouvain)**. The system looks at the ground ahead of a
walking person, segments it into surfaces, and classifies each one as **level ground, ramp
up/down or stairs up/down**, so that a powered prosthesis or a lower-limb exoskeleton can
adapt to upcoming terrain *before* the user steps on it. A wearable IMU adds gait
features (walking speed, cadence, heading) for path estimation.

## Demo video

[![Watch the demo on YouTube](https://img.youtube.com/vi/egoPBV8I34c/hqdefault.jpg)](https://youtu.be/egoPBV8I34c)

▶️ **https://youtu.be/egoPBV8I34c**

## How it works

```
Intel RealSense (depth + IMU)
        │  /camera/depth/color/points            /camera/imu
        ▼                                             ▼
 rscdsac  ── voxel down-sampling + ROI crop   imu_filter_madgwick ──► /imu/data
        │  /cdsac                                     │
        ▼                                             ▼
 TDS  ── IMU-based camera-tilt calibration, ground-frame alignment,
        surface-normal estimation, region-growing segmentation,
        per-surface features (height yc, distance zc, slope angle t)
        │   service call  ──►  classifier_server.py  (RBF-SVM, modeltotal.pkl)
        ▼
 /TP  (terrain_detection/cent)  ── terrain type, distance and height
                                   of the next 3–4 surfaces ahead
 /mya (PointCloud2)             ── point cloud coloured by class (for RViz)
```

| Class id | Terrain | Colour in `/mya` |
|:-:|---|---|
| 1 | Stairs descent | yellow |
| 2 | Ramp descent | purple |
| 3 | Level ground | green |
| 4 | Ramp ascent | red |
| 5 | Stairs ascent | blue |

The classifier is a scikit-learn `SVC(kernel='rbf', gamma=0.15)` trained on three geometric
features per segmented surface: centroid height `yc`, forward distance `zc` and surface tilt
`t` (degrees).

## Repository layout

```
terrain_detection/          ROS 1 (catkin) package
├── msg/cent.msg            output message: terrain type + distance/height per step ahead
├── srv/Classifier.srv      features → class service
└── src/
    ├── rscdsac.cpp         point-cloud pre-processing (voxel grid, ROI crop)
    ├── TDS.cpp             main terrain-detection node (latest: TDSV2–TDSV4 are variants)
    ├── calb.cpp            camera height / tilt calibration
    ├── features_recording.cpp  records surface features to build training sets
    ├── CT.cpp, FT.cpp, FC1.cpp, FR1.cpp, matrix_arrangement.cpp  experimental variants
    ├── classifier_server.py    ROS service wrapping the trained SVM (modeltotal.pkl)
    ├── Speed_Estimator*.py, Speed_predictor.py, Step_size*.py   IMU gait speed / step size
    ├── Angle_calculator*.py, path_estimator*.py, path_tracker.py heading & path estimation
    ├── recorder_*.py, save_*.py   data-logging utilities
    ├── modeltotal.pkl      trained terrain classifier (all subjects)
    └── speed_model7.pkl    trained walking-speed regressor
training/
├── train_svm.py            trains the terrain SVM → modeltotal.pkl
└── features/               surface-feature tables (yc, zc, t, label);
                            model1–8 = leave-one-subject-out folds, modelTotal = all
```

## Requirements

- Ubuntu 18.04 / 20.04 with **ROS 1** (Melodic / Noetic)
- PCL, `pcl_ros`, `pcl_conversions`, `message_filters`, `tf`, `cv_bridge`
- [`realsense2_camera`](https://github.com/IntelRealSense/realsense-ros) and
  [`imu_filter_madgwick`](http://wiki.ros.org/imu_filter_madgwick)
- Python: `numpy`, `scipy`, `pandas`, `scikit-learn`, `matplotlib`, `opencv-python`
  (`roslibpy` for `Speed_predictor.py`)
- Tested with an Intel RealSense D435i

> The `.pkl` models were pickled with an older scikit-learn. If loading fails on your
> version, retrain with `training/train_svm.py` (takes seconds).

## Build

```bash
cd ~/catkin_ws/src
git clone https://github.com/Ali-Aldabbagh/terrain-detection.git
cd ~/catkin_ws && catkin_make
source devel/setup.bash
```

## Run

```bash
# 1. Camera with point cloud and IMU
roslaunch realsense2_camera rs_camera.launch enable_pointcloud:=true \
  enable_gyro:=true enable_accel:=true unite_imu_method:=linear_interpolation \
  color_width:=424 color_height:=240 depth_fps:=15 color_fps:=15 \
  gyro_fps:=200 accel_fps:=63 initial_reset:=true

# 2. IMU orientation filter  (/camera/imu → /imu/data)
rosrun imu_filter_madgwick imu_filter_node _use_mag:=false /imu/data_raw:=/camera/imu

# 3. Classifier service — run from src/ so it finds modeltotal.pkl
cd ~/catkin_ws/src/terrain-detection/terrain_detection/src
rosrun terrain_detection classifier_server.py

# 4. Pre-processing and terrain detection
rosrun terrain_detection rscdsac
rosrun terrain_detection TDS
```

Visualise `/mya` in RViz and echo the terrain prediction with `rostopic echo /TP`.

## Retraining the classifier

```bash
cd training
python3 train_svm.py      # reads features/modelTotal.csv, writes modeltotal.pkl
cp modeltotal.pkl ../terrain_detection/src/
```

New feature tables can be recorded with the `features_recording` node.

## Related publications

If you use this code, please cite:

1. A. Al-Dabbagh et al., IEEE Xplore (2022): https://ieeexplore.ieee.org/abstract/document/9891830
2. A. Al-Dabbagh et al., IEEE Xplore (2021): https://ieeexplore.ieee.org/abstract/document/9636077

<!-- TODO: replace the two lines above with full titles/venues or BibTeX from IEEE Xplore ("Cite This" → BibTeX). -->

## Author

**Ali Al-Dabbagh** — Ph.D., UCLouvain · [ali-aldabbagh.github.io](https://ali-aldabbagh.github.io)

## License

Released under the [MIT License](LICENSE).
