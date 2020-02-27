FROM python:3.7.5-stretch
#RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
#RUN apk update
#RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev alpine-sdk
#Make dir if doesn't exist
WORKDIR /city-sensing
ADD . /city-sensing
#COPY src src
#COPY gunicorn.conf.py gunicorn.conf.py
#COPY requirements.txt requirements.txt
#RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
CMD ["gunicorn", "src.run:app", "-c", "./gunicorn.conf.py"]
