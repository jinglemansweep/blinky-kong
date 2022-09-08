# Blinky Kong LED Strip Game

![Video Demo](./docs/video.gif)

## Developing

Create a Python virtual environment and install dependencies:

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install --upgrade pip poetry
    poetry install

Run the application:

    source ./venv/bin/activate
    ./src/main.py -h

    # Examples
    ./src/main.py --host 10.0.2.86 --port 21324 --width 100 --offset 180 --flip --console
