## Build
FROM public.ecr.aws/lambda/python:3.10 as build

## Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install botocore==1.32.6 --target ${LAMBDA_TASK_ROOT}

## Copy the source code
WORKDIR ${LAMBDA_TASK_ROOT}
COPY ./app ${LAMBDA_TASK_ROOT}/app
COPY ./lambda_function.py ${LAMBDA_TASK_ROOT}/

## Run the app
CMD ["lambda_function.handler"]
ENTRYPOINT [ "python", "-m", "app" ]
