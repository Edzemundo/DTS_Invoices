# Use the latest official Ubuntu 24.04 image from Docker Hub
FROM ubuntu:24.04

# Set the working directory in the container
WORKDIR /app

# Copy pip requirements file.
COPY requirements.txt .

# Install system dependencies
# RUN sudo rm /bin/sh &&  sudo ln -s /bin/bash /bin/sh
RUN rm /bin/sh &&  ln -s /bin/bash /bin/sh
RUN apt update && apt upgrade -y
# Dependencies for cv2 and pdf2image
RUN apt install curl git ffmpeg libsm6 libxext6 poppler-utils -y
# Needed to add python add-apt-repository
RUN apt install software-properties-common -y

# Install Poppler library for PDF manipulation
RUN apt install libpoppler-dev -y

# Installing python and python dependencies.
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.12 python3.12-venv python3-pip -y
RUN python3 -m venv dts_python_env
RUN source dts_python_env/bin/activate
RUN pip install -r requirements.txt --break-system-packages

# Run python program
CMD ["python3", "watch.py"]
