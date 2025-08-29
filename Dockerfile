FROM python:3.11-slim

RUN apt-get update && apt-get -y install ffmpeg libsm6 libxext6

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["bash", "run.sh"]