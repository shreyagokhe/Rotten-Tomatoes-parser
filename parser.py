# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 00:32:15 2020

@author: Shreya Gokhe
"""
# HTML tutorial https://www.w3schools.com/html/default.asp
from bs4 import BeautifulSoup
import re
import time
import requests
import csv

def run(url,pageNum):

    fw=open('reviews.txt','w',encoding='utf8') # output file

    writer=csv.writer(fw,lineterminator='\n')#create a csv writer for this file
    
    for p in range(1,pageNum+1): # for each page 

        print ('page',p)
        html=None

        if p==1: pageLink=url # url for page 1
        else: pageLink=url+'?type=&sort=&page='+str(p)# make the page url

        for i in range(5): # try 5 times

            #send a request to access the url
            response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                break # we got the file, break the loop
            else:time.sleep(5) # wait 2 secs
            
   
        # all five attempts failed, return  None
        if not response: return None
    
        html=response.text# read in the text from the file
        
        soup = BeautifulSoup(html,features="html.parser") # parse the html 

        reviews=soup.findAll('div', {'class':'row review_table_row'}) # get all the review divs

        for review in reviews:

            critic,rating,source,text,date='NA','NA','NA','NA','NA' # initialize critic and text 
            
            criticChunk=review.find('a',{'href':re.compile('/critic/')})
            if criticChunk: critic=criticChunk.text.strip()


            ratingChunk1 = review.find('div',{'class':'review_icon icon small rotten'})
            ratingChunk = review.find('div',{'class':'review_icon icon small fresh'})
            if ratingChunk1: 
                rating = 'rotten'
            elif ratingChunk:
                rating ='fresh'
            else: rating = 'NA'    
            
            sourceChunk= review.find('em',{'class':'critic-publication'})
            if sourceChunk: source=sourceChunk.text.strip()
            

            textChunk=review.find('div',{'class':'the_review'})
            if textChunk: text=textChunk.text.strip()
            
            
            dateChunk = review.find('div',{'class':'review-date'})
            if dateChunk: date=dateChunk.text.strip()
            
            
            writer.writerow([critic , rating , source , text , date]) # write to file 
            
    fw.close()


url='https://www.rottentomatoes.com/m/star_wars_the_rise_of_skywalker/reviews'#https://www.rottentomatoes.com/m/fishermans_friends/reviews  # https://www.rottentomatoes.com/m/space_jam/reviews/'
run(url,2)