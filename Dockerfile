FROM python:3.7-slim-buster

WORKDIR /usr/src/app

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/node.py ./

CMD [ "python", "./node.py" ]
