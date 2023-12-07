FROM python:3.9.12

RUN mkdir /app/

RUN python -m pip install --upgrade pip

WORKDIR /app
ADD . /app/

RUN pip install -r /app/requirements.txt
CMD ["python", "./haji_bot.py"]