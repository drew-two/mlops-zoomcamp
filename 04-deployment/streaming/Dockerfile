FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install pipenv 

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "my_lambda_function.py", "./" ]

CMD [ "my_lambda_function.lambda_handler" ]
