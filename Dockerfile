FROM python:3.10-alpine

WORKDIR /app
ADD requirements.txt /app/requirements.txt
ADD src /app/src/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN ["python", "src/db.py"]
CMD ["python", "src/main.py"]