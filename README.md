# To Run
1. Checkout this repo
2. RUN `docker build -t overbond_submission:latest .`
3. Run `docker run -v /path/to/your/input-output/folder:/submission/resources -e INPUT_FILE_NAME=sample_input.json -e OUTPUT_FILE_NAME=sample_output.json overbond_submission:latest`
4. To run tests:

   a. ```pip install \
          --no-warn-script-location \
          --trusted-host pypi.org \
          -r requirements.txt```
          
   b. Run `pytest`