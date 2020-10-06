FROM python:3.8

LABEL firstname=Shadi, lastname=Boomi

WORKDIR /app

COPY . /app

EXPOSE 5010

RUN cut -d @ -f 1 requirements.txt > requirements_spare.txt
RUN pip install -r requirements_spare.txt

ENTRYPOINT ["python"]

CMD ["server.py"]