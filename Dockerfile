# Use the latest official Python runtime image from Docker Hub
FROM homebrew/brew:latest

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

#Install dependencies
RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
RUN sudo apt update
RUN brew install poppler
RUN brew install python3
#RUN apt-get install python3-pip -y
RUN python3 -m pip install -r requirements.txt --break-system-packages


# Run the specified Python file (replace 'your_script.py' with the actual filename)
CMD ["python3", "watch.py"]
