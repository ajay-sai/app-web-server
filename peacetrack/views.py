#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import jinja2
import uuid
from jinja2.ext import loopcontrols
from webhub.checker import check
from webhub.models import *
from rest_framework import viewsets
from webhub.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
import django_filters
from paths import cpspath
from webhub import xlrd
import smtplib
import json

#SMTP port for sending emails
SMTP_PORT = 465

#link for the localhost
website = "http://systerspcweb.herokuapp.com/"

jinja_environ = jinja2.Environment(loader=jinja2.FileSystemLoader(['peacetrack/ui']), extensions=[loopcontrols])

#apis for peacetrack begin here

#for regions
class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer        

#List all region
@api_view(['GET', 'POST'])
def region_list(request):
     if request.method == 'GET':
        region = Region.objects.all()
        serializer = RegionSerializer(region, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = RegionSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a region instance.
@api_view(['GET', 'PUT', 'DELETE'])
def region_detail(request, pk):
    try:
        region = Region.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegionSerializer(region)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RegionSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for sectors
class SectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer        

#List all sectors
@api_view(['GET', 'POST'])
def sector_list(request):
     if request.method == 'GET':
        sector = Sector.objects.all()
        serializer = SectorSerializer(sector, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = SectorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a sector instance.
@api_view(['GET', 'PUT', 'DELETE'])
def sector_detail(request, pk):
    try:
        sector = Sector.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectorSerializer(sector)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SectorSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sector.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

#for ptposts
class PTPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    serializer_class = PTPostSerializer        
    model = PTPost

    def get_queryset(self):
	try:
	    post_sectors = self.request.QUERY_PARAMS['post_sectors']
	except:
	    post_sectors = None
	if post_sectors is not None and post_sectors == "True":
	    try:
		pk = self.request.QUERY_PARAMS['id']
	    except:
		pk = None
	    if pk is not None:
        	ptpost = PTPost.objects.get(pk=pk)
		self.serializer_class = SectorSerializer
		self.model = Sector
		queryset = ptpost.sector.all()
	else:
	    queryset = PTPost.objects.all()
	    try:
		vname = self.request.QUERY_PARAMS['vol_name']
	    except:
		vname = None
	    try:
		vemail = self.request.QUERY_PARAMS['vol_email']
	    except:
		vemail = None
	    if vname is not None:
        	queryset = queryset.filter(vol_name=vname)
	    if vemail is not None:
        	queryset = queryset.filter(vol_email=vemail)
        return queryset
#List all ptpost
@api_view(['GET', 'POST'])
def ptpost_list(request):
     if request.method == 'GET':
        ptpost = PTPost.objects.all()
        serializer = PTPostSerializer(ptpost, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = PTPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a ptpost instance.
@api_view(['GET', 'PUT', 'DELETE'])
def ptpost_detail(request, pk):
    try:
        ptpost = PTPost.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PTPostSerializer(ptpost)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PTPostSerializer(post, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ptpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#error    
#for projects
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer        

#List all projects
@api_view(['GET', 'POST'])
def project_list(request):
     if request.method == 'GET':
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a project instance.
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

    
#for goals
class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer        

#List all goal
@api_view(['GET', 'POST'])
def goal_list(request):
     if request.method == 'GET':
        goal = Goal.objects.all()
        serializer = GoalSerializer(goal, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = GoalSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a goal instance.
@api_view(['GET', 'PUT', 'DELETE'])
def goal_detail(request, pk):
    try:
        goal = Goal.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GoalSerializer(goal)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GoalSerializer(goal, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
        
#for objectives
class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer        

#List all objective
@api_view(['GET', 'POST'])
def objective_list(request):
     if request.method == 'GET':
        objective = Objective.objects.all()
        serializer = ObjectiveSerializer(objective, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = ObjectiveSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a objective instance.
@api_view(['GET', 'PUT', 'DELETE'])
def objective_detail(request, pk):
    try:
        objective = Objective.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ObjectiveSerializer(objective)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ObjectiveSerializer(objective, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        objective.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
#for indicators
class IndicatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer        

#List all indicator
@api_view(['GET', 'POST'])
def indicator_list(request):
     if request.method == 'GET':
        indicator = Indicator.objects.all()
        serializer = IndicatorSerializer(indicator, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = IndicatorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a indicator instance.
@api_view(['GET', 'PUT', 'DELETE'])
def indicator_detail(request, pk):
    try:
        indicator = Indicator.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IndicatorSerializer(indicator)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IndicatorSerializer(indicator, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        indicator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for outputs
class OutputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Output.objects.all()
    serializer_class = OutputSerializer        

#List all output
@api_view(['GET', 'POST'])
def output_list(request):
     if request.method == 'GET':
        output = Output.objects.all()
        serializer = OutputSerializer(output, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = OutputSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a output instance.
@api_view(['GET', 'PUT', 'DELETE'])
def output_detail(request, pk):
    try:
        output = Output.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OutputSerializer(output)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OutputSerializer(output, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        output.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    
#for outcomes
class OutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer        

#List all outcome
@api_view(['GET', 'POST'])
def outcome_list(request):
     if request.method == 'GET':
        outcome = Outcome.objects.all()
        serializer = OutcomeSerializer(outcome, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = OutcomeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a outcome instance.
@api_view(['GET', 'PUT', 'DELETE'])
def outcome_detail(request, pk):
    try:
        outcome = Outcome.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OutcomeSerializer(outcome)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OutcomeSerializer(outcome, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        outcome.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for activitys
class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer        

#List all activity
@api_view(['GET', 'POST'])
def activity_list(request):
     if request.method == 'GET':
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a activity instance.
@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, pk):
    try:
        activity = Activity.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivitySerializer(activity, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
#for measurements
class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer        

#List all measurement
@api_view(['GET', 'POST'])
def measurement_list(request):
     if request.method == 'GET':
        measurement = Measurement.objects.all()
        serializer = MeasurementSerializer(measurement, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = MeasurementSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a measurement instance.
@api_view(['GET', 'PUT', 'DELETE'])
def measurement_detail(request, pk):
    try:
        measurement = Measurement.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeasurementSerializer(measurement)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeasurementSerializer(measurement, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        measurement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
#for cohorts
class CohortViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer        

#List all cohort
@api_view(['GET', 'POST'])
def cohort_list(request):
     if request.method == 'GET':
        cohort = Cohort.objects.all()
        serializer = CohortSerializer(cohort, many=True)
        return Response(serializer.data)

     elif request.method == 'POST':
        serializer = CohortSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Retrieve, update or delete a cohort instance.
@api_view(['GET', 'PUT', 'DELETE'])
def cohort_detail(request, pk):
    try:
        cohort = Cohort.objects.get(pk=pk)
    except Pcuser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CohortSerializer(cohort)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CohortSerializer(cohort, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cohort.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#for volunteers
class VolunteerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
#    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    model = Volunteer

    def get_queryset(self):
	queryset = Volunteer.objects.all()
	try:
		vname = self.request.QUERY_PARAMS['vol_name']
	except:
		vname = None
	try:
		vemail = self.request.QUERY_PARAMS['vol_email']
	except:
		vemail = None
	try:
		vpost = self.request.QUERY_PARAMS['vol_ptpost']
	except:
		vpost = None
	try:
		vsector = self.request.QUERY_PARAMS['vol_sector']
	except:
		vsector = None
	if vname is not None:
            queryset = queryset.filter(vol_name=vname)
	if vemail is not None:
            queryset = queryset.filter(vol_email=vemail)
	if vpost is not None:
            queryset = queryset.filter(vol_ptpost=vpost)
	if vsector is not None:
            queryset = queryset.filter(vol_sector=vsector)
        return queryset

    #List all volunteer
    @api_view(['GET', 'POST'])
    def volunteer_list(request):
	if request.method == 'GET':
		volunteer = Volunteer.objects.all()
        	serializer = VolunteerSerializer(volunteer, many=True)
        	return Response(serializer.data)
    	elif request.method == 'POST':
        	serializer = VolunteerSerializer(data=request.DATA)
        	if serializer.is_valid():
            		serializer.save()
        	    	return Response(serializer.data, status=status.HTTP_201_CREATED)
       		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Retrieve, update or delete a volunteer instance.
    @api_view(['GET', 'PUT', 'DELETE'])
    def volunteer_detail(request, pk):
    	try:
        	volunteer = Volunteer.objects.get(pk=pk)
    	except Pcuser.DoesNotExist:
        	return Response(status=status.HTTP_404_NOT_FOUND)

    	if request.method == 'GET':
        	serializer = VolunteerSerializer(volunteer)
        	return Response(serializer.data)

    	elif request.method == 'PUT':
        	serializer = VolunteerSerializer(volunteer, data=request.DATA)
        	if serializer.is_valid():
            		serializer.save()
            		return Response(serializer.data)
        	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    	elif request.method == 'DELETE':
        	volunteer.delete()
        	return Response(status=status.HTTP_204_NO_CONTENT)

 
#called when user wishes to go to the Peacetrack from dashboard
def peacetrack(request):
    return HttpResponse(jinja_environ.get_template('peacetrack.html').render({"pcuser":None}))  


#Called when a user wants to see the details of a volunteer.
def volunteer(request):
    all_vol = Volunteer.objects.all()
    all_list=[]
    for vol in all_vol:
	temp={}
	temp['vol_name']=vol.vol_name
	temp['vol_ptpost']=vol.vol_ptpost
	temp['vol_sector']=vol.vol_sector
	temp['cohort_activity_meas']=[]
	for cohort in vol.vol_cohort.all():
		temp1={}
		temp1['activity']=[]
		for act in vol.vol_activity.all():
			if cohort.compare(act.activity_cohort):
				temp1['activity'].append(act)
		temp1['meas']=[]
		for meas in vol.vol_meas.all():
			if cohort.compare(meas.meas_cohort):
				temp1['meas'].append(meas)
		for i in range(max(len(temp1['activity']),len(temp1['meas']))):
			if i > 0:
				cohort=""
			act = ""
			if i < len(temp1['activity']):
				act = temp1['activity'][i]
			meas = ""
			if i < len(temp1['meas']):
				meas = temp1['meas'][i]
			temp['cohort_activity_meas'].append([cohort,act,meas])
	all_list.append(temp)
    return HttpResponse(jinja_environ.get_template('volunteer.html').render({"all_vol":all_vol,"all_list":all_list, "pcuser":request.user.pcuser}))

#Class Summary used to return objects to Summary of Peacetrack
class SummaryItem:
    post=""
    region=""
    sector=""
    project=""
    goal=""
    objective=""
    indicator=""
    ind_type_1=""
    ind_type_2=""
    value=0
    def __init__(self,post,region,sector,project,goal,objective,indicator,ind_type_1,ind_type_2,value):
	self.post=post
	self.region=region
	self.sector=sector
	self.project=project
	self.goal=goal
	self.objective=objective
	self.indicator=indicator
	self.ind_type_1=ind_type_1
	self.ind_type_2=ind_type_2
	self.value=value
    def as_json(self):
	return dict(post=self.post,region=self.region,sector=self.sector,project=self.project,goal=self.goal,objective=self.objective,indicator=self.indicator,ind_type_1=self.ind_type_1,ind_type_2=self.ind_type_2,value=self.value)


#Called when a user wants to see the summary of peacetrack volunteer db
def summary(request):
    all_output = Output.objects.all()
    all_outcome = Outcome.objects.all()
    all_list = []
    for output in all_output:
	temp= SummaryItem(output.output_ptpost.post_name, output.output_ptpost.post_region.region_name, output.output_sector.sector_code, output.output_ind.ind_obj.obj_goal.goal_project.project_name, output.output_ind.ind_obj.obj_goal.goal_name, output.output_ind.ind_obj.obj_name, output.output_ind.ind_desc, output.output_ind.ind_type_1, "Output", output.output_value)
	all_list.append(temp)
    for outcome in all_outcome:
	temp= SummaryItem(outcome.outcome_ptpost.post_name, outcome.outcome_ptpost.post_region.region_name, outcome.outcome_sector.sector_code, outcome.outcome_ind.ind_obj.obj_goal.goal_project.project_name, outcome.outcome_ind.ind_obj.obj_goal.goal_name, outcome.outcome_ind.ind_obj.obj_name, outcome.outcome_ind.ind_desc, outcome.outcome_ind.ind_type_1, "Outcome", outcome.outcome_value)
	all_list.append(temp)
    results = [each.as_json() for each in all_list]
    jsonDump = json.dumps(results)
#    json=ser.serialize("json",all_list)
#    return HttpResponse(jsonDump, content_type='application/json')
    return HttpResponse(jinja_environ.get_template('summary.html').render({"all_list":results,"pcuser":request.user.pcuser}))

def sectorEquate(sectors,sector2):
    temp = list(sectors)
    for sector1 in temp:
    	if sector1.sector_name==sector2.sector_name and sector1.sector_desc==sector2.sector_desc and sector1.sector_code==sector2.sector_code:
	    return True
    return False
