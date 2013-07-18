import os
import sys
import time
import simplejson
from dateutil import parser
from bs4 import BeautifulSoup
from django.http import HttpResponse, Http404
from phn_app.phn.models import *
from django.template import Context, loader
from django.template import RequestContext
from django.template.loader import get_template
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from phn_app.phn.forms import *
from django.core.files import File
from django.contrib.sessions.models import Session


def k(a,b):
    def _k(item):
        return (item[a],item[b])
    return _k

def wrap_article(pars): #wrap the extracted contents
        result = '<p align="right" color=grey>Published date: ' +  pars['date'] + '<br>'
        result += 'Publisher: ' + pars['publisher'] + '<br>'
        result += '<a href=' + pars['original_url'] + '>Link to the Orinal article</a></p><br>'
	if pars['image_url'] != 'NA':
                result += '<img width="160" height="160" src=' + pars['image_url'] + ' /><br><br>'
	result += '<h3>' + pars['title'] + '</h3>'
        temp = result + pars['article'] 
        rSoup = BeautifulSoup(temp)
        rSoup = rSoup.prettify(formatter="html")
        return(rSoup)

def wrap_front(pars, disease_id, doc_id): #wrap the extracted contents
        result = '<a href=/phn/?disease_id=' + disease_id + '&doc_id=' + doc_id + ' >'
        if pars['image_url'] != 'NA':
                result += '<img class=textWrap src=' + pars['image_url'] + ' width="30px" height="30px"; />'
	if pars['image_url'] != 'NA' and len(pars['title']) > 40:
		temp_title = pars['title'][0:40] + "..."
	else:
		temp_title =  pars['title']
        result += temp_title + '<br></a>'
	result += '<div id="bottom"><p>' +  pars['date'] + '<br>'
	result += pars['publisher'] + '<br></p></div>'
        rSoup = BeautifulSoup(result)
        rSoup = rSoup.prettify(formatter="html")
        return(rSoup)

def index(request):
	num_active_docs =10 
	try:
		risk_disease_all = RiskDisease.objects.all() ##should be passed from local.storage 
		idx = 1
		risk_disease = list()
		risk_disease_news = dict()
		for rd in risk_disease_all:
			risk_disease.append(rd.disease)
			disease_id = str(rd.disease.disease_id)
			active_path = "/home/jung/public_html/PHN/active_docs/" + disease_id + "/"
			doc_list = os.listdir(active_path)
			temp_list = []
			for doc in doc_list:
				temp = doc.split(".")
			        temp2 = [parser.parse(temp[1]).date(), temp[0].split("L")[0], doc]
			        temp_list.append(temp2)

			rs = sorted(temp_list, key=k(0,1), reverse=True)
			if len(rs) < num_active_docs:
				num_display = len(rs)
			else:
                		num_display = num_active_docs
			temp_news = list()
        		for i in range(0, num_display):
		                temp_file = open(active_path + rs[i][2], "r")
                	        temp_json = simplejson.load(temp_file)
 		                temp_file.close()
		                temp_article = wrap_front(temp_json, disease_id, rs[i][2])
				temp_news.append(temp_article)
			risk_disease_news[disease_id] = temp_news
		variables = RequestContext(request, {
			'has_disease': idx,
			'risk_disease': risk_disease,
			'risk_disease_news': risk_disease_news,
			})
		return render_to_response(
                       'news_page_front.html',
                       variables
                       )
			
	except RiskDisease.DoesNotExist:
		ds_list = list()
		for ds in Disease.objects.all():
               		temp = (ds.disease_id, ds.disease_name)
                        ds_list.append(temp)

		variables = RequestContext(request, {
                        'disease_list':[disease for disease in ds_list],
                        })
		return render_to_response(
                       	'news_page_front.html',
         	        variables
                        )

def phn_news(request):
	disease_id = request.GET.get('disease_id',None)
	doc_id = request.GET.get('doc_id', None)
	active_path = "/home/jung/public_html/PHN/active_docs/" + disease_id + "/"
	article_file = open(active_path + doc_id, "r")	
	article_json = simplejson.load(article_file)
        article_file.close()
        proc_article = wrap_article(article_json)
	variables = RequestContext(request, {
                                'article': proc_article,
                                })
	return render_to_response(
                        'news_page_article.html',
                        variables
                        )
	

def update_user_disease_list(request):
	disease_list = request.GET.getlist('disease_list')
	user = request.session.session_key
	for ds in disease_list:
		d = Disease.objects.get(disease_id=ds)
		rd = RiskDisease(user=user, disease=d)
		rd.save()

	return HttpResponseRedirect('/')

