from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
def index(request):
    return render(request, 'django_assistant/index.html', {})


def decode_dict(dict1):
    keys = dict1.keys()
    for key in keys:
	print "key is",key
	print "value is",dict1[key]
	if type(dict1[key]) == dict:
	    decode_dict(dict1[key])
    return ""

@csrf_exempt
def a_create_api(request):
    print "entering create_api"
    #~ import ipdb;ipdb.set_trace()
    edit_mode = request.POST.get("edit_mode",None)
    api_id = request.POST.get("api_id",None)
    url = request.POST.get("url",None)
    params = request.POST.get("params",None)
    desc = request.POST.get("descr",'')
    http_type = request.POST.get("http_type",None)
    
    if edit_mode == "add":
	api = Api()
	

    if edit_mode == "edit":
	api = Api.objects.get(id=api_id)
    
    api.url = url
    api.desc = desc
    api.http_type = http_type
    api.save()

    
    dict1 = {}
    dict1["result"] = "Success"
    return HttpResponse(json.dumps(dict1),content_type="application/json")

@csrf_exempt
def a_edit_params(request):
    edit_mode = request.POST.get("edit_mode",None)
    params = eval(request.POST.get("params",None))
    api_id = request.POST.get("api_id",None)
    apiparam_id = request.POST.get("apiparam_id",None)
    print request.POST
    tags = eval(request.POST.get("tags",None))
    
    
    
    if edit_mode == "add":
	api = Api.objects.get(id=api_id)
	param = ApiParam()
	param.params = params
	param.save()
	api.params.add(param)
	    
    if edit_mode == "edit":
	param = ApiParam.objects.get(id=apiparam_id)
	param.params = params
	param.save()
	    
    for tag in param.tags.all():
	param.tags.remove(tag)
	
    for tag in tags:
	tag = Tag.objects.get(id=tag)
	param.tags.add(tag)
    
    
    
    dict1 = {}
    dict1["result"] = "Success"
    return HttpResponse(dict1,content_type="application/json")

@csrf_exempt
def a_get_apis(request):
   
    list1 = []
    
    for api in Api.objects.all():
	list2 = []
	dict2 = {}
	dict2["api_id"] = api.id
	dict2["url"] = api.url
	dict2["params"] = api.get_params()	    
	dict2["http_type"] = api.http_type
	dict2["api_status"] = api.status
	list1.append(dict2)
    
    dict1={}
    dict1["result"] = "Success"
    dict1["response"] = list1
    return HttpResponse(json.dumps(dict1),content_type="application/json")

@csrf_exempt
def a_fetch_api_details(request):
    api_id = request.POST.get("api_id",None)
    
    
    api = Api.objects.get(id=api_id)
    api_dict = {}
    api_dict["id"] = api.id
    api_dict["url"] = api.url
    api_dict["params"] = api.get_params()
    api_dict["http_type"] = api.http_type
    api_dict["api_status"] = api.status
    api_dict["descr"] = api.desc
    
    
    dict1 = {}
    dict1["api"] = api_dict
    dict1["result"] = "Success"
    return HttpResponse(json.dumps(dict1),content_type="aplication/json")


@csrf_exempt
def a_delete_api(request):
    api_id = request.POST.get("api_id",None)
    api = Api.objects.get(id=api_id)
    for param in api.params.all():
	param.delete()
    
    api.delete()
    
    dict1 = {}
    dict1["result"] = "Success"
    return HttpResponse(json.dumps(dict1),content_type="application/json")


@csrf_exempt
def a_trial_api(request):
    print request.POST.get("var")
    dict1 = {}
    dict1["sample"] = [{"name":"jerin","age":"25"},{"name":"jerin2","age":"26"}]
    return HttpResponse(json.dumps(dict1),content_type="aplication/json")


@csrf_exempt
def a_edit_api_status(request):
    api_id = request.POST.get("api_id",None)
    api_status = request.POST.get("api_status",None)
    
    api = Api.objects.get(id=api_id)
    api.status = api_status
    api.save()
    dict1 = {}
    dict1["result"] = "Success"
    return HttpResponse(json.dumps(dict1),content_type="application/json")

@csrf_exempt
def a_edit_api(request):
    edit_element = request.POST.get("edit_element",None)
    api_id = request.POST.get("api_id",None)
    api = Api.objects.get(id=api_id)
    
    if edit_element == "basic_info":
	url = request.POST.get("url",None)
	http_type = request.POST.get("http_type",None)
	api.url = url
	api.http_type = http_type
	api.save()
	
    if edit_element == "info":
	print edit_element
	description = request.POST.get("description",None)
	api.desc = description
	api.save()
	
	
    dict1 = {}
    dict1["result"] = "Success"
    return HttpResponse(json.dumps(dict1),content_type="application/json")

@csrf_exempt
def a_delete_api_input(request):
    input_id = request.POST.get("input_id",None)
    print "input_id : ",input_id
    inputset = ApiParam.objects.get(id=input_id)
    inputset.delete()

    dict1 = {}
    dict1["result"] = "Success"
    return HttpResponse(json.dumps(dict1),content_type="application/json")


@csrf_exempt
def a_get_tags(request):
    list1 = []
    for tag in Tag.objects.all():
	dict2={}
	dict2["name"] = tag.name
	dict2["id"] = tag.id
	list1.append(dict2)
    
    dict1 = {}
    dict1["result"] = "Success"
    dict1["tags"] = list1
    return HttpResponse(json.dumps(dict1),content_type="application/json")
