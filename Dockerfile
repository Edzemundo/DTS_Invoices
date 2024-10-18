# Use the latest official Python runtime image from Docker Hub
FROM conda/miniconda3

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

# Install system dependencies
# RUN sudo rm /bin/sh &&  sudo ln -s /bin/bash /bin/sh
RUN rm /bin/sh &&  ln -s /bin/bash /bin/sh
RUN conda update conda -y
RUN conda install poppler -y

# Installing python and python dependencies through conda
RUN conda init
RUN conda create --name dts_invoices python=3.12.7 -y
RUN $SHELL
RUN source activate dts_invoices

# Run python program
RUN python3 -m pip install -r requirements.txt

# Run the specified Python file (replace 'your_script.py' with the actual filename)
CMD ["python3", "watch.py"]