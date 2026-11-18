
import sys
import requests
import bs4
import scrapy
import pandas
import nltk
import sklearn
import sumy

print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])
print("All required libraries imported successfully!")

if sys.prefix != sys.base_prefix:
    print("Virtual environment: ACTIVE")
else:
    print("Virtual environment: NOT ACTIVE")
