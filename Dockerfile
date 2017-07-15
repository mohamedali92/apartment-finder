FROM python:3
ADD scraper.py /
RUN pip install -U requirements.txt
CMD [ "python", "./scraper.py"  