# Download base image
FROM python:3.7

# Set variables
ARG APP_DIR=/usr/src/app
ARG PORT=5000

# Update the package manager and install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential nano && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# Copy the requirements file into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt 

RUN pip install --upgrade Flask
RUN pip install --upgrade itsdangerous

RUN pip3 install "monai[fire]"
RUN pip3 install pytorch-ignite==0.4.9

# Copy the application files into the container
COPY server.py test.py ./
COPY models ./models

# Expose the port and set the entry point
EXPOSE ${PORT}
ENTRYPOINT ["gunicorn"]

# Start the server
CMD ["--workers", "4", "--bind", "0.0.0.0:5000", "server:app", "--timeout", "3600"]
