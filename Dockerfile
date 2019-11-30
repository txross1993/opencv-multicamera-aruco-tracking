FROM jjanzic/docker-python3-opencv:contrib-opencv-3.4.1
ENV PYTHONUNBUFFERED=1
COPY app /app
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
WORKDIR /app
ENTRYPOINT  ["python", "app.py"]