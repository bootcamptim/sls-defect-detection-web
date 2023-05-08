# Real-time Defect Detection

This is a real-time defect detection application built using Flask, Flask-SocketIO, TensorFlow, and OpenCV. The application loads images from a specified directory, processes them with a pre-trained deep learning model, and streams the results to the web application.

## Features

- Real-time image processing using Flask and OpenCV
- Defect detection with pre-trained TensorFlow models
- Live video stream with defect predictions

## Installation

1. Install the required Python packages:

```bash
pip install Flask Flask-SocketIO tensorflow opencv-python-headless
```

2. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/user/repo.git
cd repo
```

3. Place your pre-trained TensorFlow models in the `models` directory.

4. Ensure your image source directory is set correctly in the `imdir` variable.

5. Run the application:

```bash
python sls-defect-detection-web.py
```

The application will be accessible at `http://localhost:5500`.

## Usage

1. Access the application at `http://localhost:5500`.
2. Select a pre-trained TensorFlow model from the dropdown menu.
3. The application will start processing the images in the specified directory and display the live video stream along with defect predictions.

## Files

- `sls-defect-detection-web.py`: The main application file containing the Flask server, WebSocket handling, and image processing code.
- `templates/index.html`: The HTML template for the main page of the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
