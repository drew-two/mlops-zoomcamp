FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

# do stuff here
RUN pip install -U pip
RUN pip install pipenv 

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "starter.py", "./" ]

RUN mkdir output

CMD [ "python", "starter.py", "2021", "4" ]