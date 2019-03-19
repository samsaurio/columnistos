#!/bin/sh
#export TESTING='True'
export LOG_FOLDER='./logs/'

cd diarios || exit
scrapy crawl lanacionpy
scrapy crawl abc
scrapy crawl ultimahora
