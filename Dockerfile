# Running unit tests and style checks
FROM python:3 AS compile-image
COPY . /submission
WORKDIR /submission
RUN pip install \
    --no-warn-script-location \
    --trusted-host pypi.org \
    -r requirements.txt

RUN pytest
ENV INPUT_FILE_NAME sample_input.json
ENV OUTPUT_FILE_NAME sample_output.json
ENTRYPOINT ./sde-test-solution.sh resources/$INPUT_FILE_NAME resources/$OUTPUT_FILE_NAME