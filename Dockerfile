FROM python:3
ADD scraper.py /
RUN pip install -r requirements.txt
CMD [ "python", "./scraper.py"  