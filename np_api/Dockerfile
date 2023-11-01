FROM python:3

WORKDIR usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/dto ./dto/
COPY ./app/model ./model/
COPY ./app/resources ./resources/
COPY ./app/service ./service/
COPY ./app/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
