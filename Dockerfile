FROM python:3.11-bookworm

# setup nodejs
ENV NODE_VERSION=16.13.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

WORKDIR /app

# setup backend requirements
COPY backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

# setup frontend requirements
COPY ui/package.json ui/package.json
WORKDIR /app/ui
RUN npm install

COPY . /app

# build frontend
WORKDIR /app/ui
RUN npm run build

# start the server
WORKDIR /app/backend
ENTRYPOINT ["python3"]
CMD ["app.py"]

# expose the port
EXPOSE 8000