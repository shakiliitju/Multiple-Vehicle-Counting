# YOLOv8/YOLOv10 Multiple Vehicle Counting System

A real-time vehicle detection and counting system using YOLOv8 and YOLOv10 models with OpenCV. This project tracks multiple types of vehicles crossing predefined lines in a video feed and automatically saves images of detected vehicles.

## Features

- **Multi-Vehicle Detection**: Detects and tracks cars, buses, trucks, motorcycles, and bicycles
- **Bidirectional Counting**: Counts vehicles entering and leaving a designated area
- **Real-time Tracking**: Uses custom tracker for object persistence across frames
- **Automatic Image Capture**: Saves cropped images of detected vehicles with timestamps
- **Visual Interface**: Real-time display with bounding boxes, counts, and detection lines
- **Custom Model Support**: Uses both pre-trained and custom-trained YOLOv10 models

## Vehicle Types Supported

- **Cars** (Purple bounding box)
- **Buses** (Red bounding box)  
- **Trucks** (Yellow bounding box)
- **Motorcycles** (White bounding box)
- **Bicycles** (White bounding box)

## Project Structure

```
multiple-vehicle-counting/
│
├── main.py                 # Main application script
├── tracker.py             # Custom object tracking implementation
├── coco.txt               # COCO class names
├── dataset.yaml           # Dataset configuration for training
├── yolov10_custom.pt      # Custom trained YOLOv10 model
├── yolov10s.pt           # Pre-trained YOLOv10 small model
├── yolov8s.pt            # Pre-trained YOLOv8 small model
├── ju1.mp4, ju2.mp4      # Sample video files
├── test1.mp4, test2.mp4  # Test video files
├── images/               # Directory for saved vehicle images
├── dataset/              # Training dataset
│   ├── train/
│   ├── val/
│   └── test/
└── runs/                 # Training results and logs
```

## Requirements

### Dependencies

```bash
pip install ultralytics opencv-python pandas cvzone numpy
```

### System Requirements

- Python 3.7+
- OpenCV 4.x
- CUDA-capable GPU (recommended for better performance)
- Sufficient disk space for saving vehicle images

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd yolov8-multiple-vehicle-counting
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download pre-trained models** (if not included)
   - Place YOLOv10 models in the root directory
   - Ensure `yolov10_custom.pt` is available

4. **Prepare video files**
   - Place your video files in the root directory
   - Update the video file path in `main.py` if needed

## Usage

### Basic Usage

```bash
python main.py
```

### Configuration

**Video Source**: Change the video file in `main.py`:
```python
cap = cv2.VideoCapture('your_video.mp4')  # Replace with your video file
```

**Detection Lines**: Modify the counting lines position:
```python
cy1 = 350  # First line position
cy2 = 365  # Second line position
offset = 8  # Detection tolerance
```

**Model Selection**: Change the model file:
```python
model = YOLO("yolov10_custom.pt")  # Use different model file
```

### Controls

- **Mouse Movement**: Displays pixel coordinates (for line positioning)
- **'q' Key**: Quit the application
- **ESC**: Close the video window

## How It Works

### Detection Process

1. **Video Processing**: Reads video frame by frame (processes every 3rd frame for performance)
2. **Object Detection**: Uses YOLOv10 model to detect vehicles in each frame
3. **Classification**: Separates detected objects into vehicle categories
4. **Tracking**: Assigns unique IDs to vehicles using custom tracker
5. **Line Crossing**: Monitors when vehicles cross predefined counting lines
6. **Image Capture**: Automatically saves cropped vehicle images when crossing lines

### Tracking Algorithm

The custom tracker (`tracker.py`) uses:
- **Centroid Tracking**: Tracks objects based on their center points
- **Distance Calculation**: Uses Euclidean distance to associate detections
- **ID Management**: Assigns unique IDs to new objects and maintains them across frames

### Counting Logic

- **Entry Detection**: Vehicle crosses from line 1 (cy1) to line 2 (cy2)
- **Exit Detection**: Vehicle crosses from line 2 (cy2) to line 1 (cy1)
- **Duplicate Prevention**: Ensures each vehicle is counted only once per crossing

## Output

### Real-time Display

- Live video feed with bounding boxes around detected vehicles
- Vehicle type labels on each detection
- Real-time counts for entering and leaving vehicles
- Visual indication of counting lines

### Saved Images

Images are automatically saved to the `images/` directory with naming convention:
```
car_enter_2024-01-15_14-30-25.jpg
bus_leave_2024-01-15_14-30-26.jpg
truck_enter_2024-01-15_14-30-27.jpg
```

### Count Display

The interface shows:
- **Left Side**: Number of vehicles leaving (by type)
- **Right Side**: Number of vehicles entering (by type)
- **Real-time Updates**: Counts update as vehicles cross lines

## Custom Model Training

### Dataset Structure

The project includes a custom dataset with 15 vehicle classes:
- bicycle, car, motorcycle, bus, truck
- Animal Cart, Auto Rickshaw, Heavy Truck
- Large Bus, Medium Truck, Microbus
- Minibus, Rickshaw, Small Truck, Tempo

### Training Configuration

- **Dataset**: Located in `dataset/` directory
- **Configuration**: Defined in `dataset.yaml`
- **Classes**: 15 custom vehicle types
- **Format**: YOLO format with train/val/test splits

## Performance Optimization

### Frame Skipping
```python
if count % 3 != 0:
    continue  # Process every 3rd frame
```

### Video Resizing
```python
frame = cv2.resize(frame, (1020, 500))  # Resize for consistent processing
```

### Efficient Tracking
- Distance threshold of 35 pixels for object association
- Automatic cleanup of unused object IDs

## Troubleshooting

### Common Issues

1. **Model Loading Error**
   - Ensure model files are in the correct directory
   - Check file permissions and paths

2. **Video Not Loading**
   - Verify video file path and format
   - Ensure OpenCV supports the video codec

3. **Poor Detection Accuracy**
   - Adjust detection confidence threshold
   - Consider retraining with domain-specific data

4. **Performance Issues**
   - Increase frame skipping interval
   - Reduce video resolution
   - Use GPU acceleration if available

### Configuration Tips

- **Line Positioning**: Use mouse coordinates to set optimal counting lines
- **Offset Adjustment**: Modify offset value based on vehicle speeds
- **Model Selection**: Choose appropriate model size based on accuracy/speed requirements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Ultralytics**: For YOLOv8 and YOLOv10 implementations
- **OpenCV**: For computer vision functionality
- **CVZone**: For enhanced CV utilities

## Future Enhancements

- [ ] Add vehicle speed estimation
- [ ] Implement database logging
- [ ] Add web interface for remote monitoring
- [ ] Support for multiple detection zones
- [ ] Integration with traffic management systems
- [ ] Real-time analytics dashboard

## Contact

For questions, issues, or contributions, please open an issue on the GitHub repository.
