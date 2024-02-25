import csv
import os
from program.models import Program 
import datetime 
from django.utils.formats import get_format


from django.db.models import Max, Avg,Sum, Count,Min
from easyaudit.models import RequestEvent, CRUDEvent, LoginEvent
import json
from django import template
from conceptnote.models import Icn, Impact
from program.models import Indicator
from itertools import chain
from user.models import Profile
from django.db.models import F    
from django.contrib.auth.models import Group, Permission, User

from django.shortcuts import get_object_or_404
from collections import defaultdict
from itertools import chain
from django import template

 

register = template.Library()
import datetime
def run():
     program_users = Program.objects.annotate(num_user=Count("users_role")).order_by('-num_user')[:12]
     for i in program_users:
        print(i)
    
"""
    user_activity = CRUDEvent.objects.filter(user=1).order_by('-id')[:12]
    for item in  user_activity:
        item.object_json_repr = jsonify(item.object_json_repr)
    qs1 = RequestEvent.objects.filter(user_id=1).values('datetime__date').annotate(id_count=Count('id', distinct=True))
    qs2 = RequestEvent.objects.filter(user_id=1, method='POST').values('datetime__date').annotate(count_login=Count('id', distinct=True))
    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['datetime__date']].update(collectible.items())

    all_request = list(collector.values()) 
    for request in all_request:
        print(request)
    
@register.filter(name='jsonify')
def jsonify(data):
    if isinstance(data, dict):
        return data
    else:
        return json.loads(data)



    collector = defaultdict(dict)

    for collectible in chain(qs1, qs2):
        collector[collectible['datetime__date']].update(collectible.items())

    all_request = list(collector.values()) 
     
	

	rma =RequestEvent.objects.filter(user_id=1).values('datetime__date').annotate(id_count=Count('id', distinct=True))
	login_activity = LoginEvent.objects.filter(user_id=1).values('datetime__date').annotate(count_login=Count('id', distinct=True))
	qs = list(chain(rma,login_activity))
	for r in qs:
		print(r)
	#start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
	#end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

	#print("Number of weeks from",start_date_str,"to",end_date_str)

	#for date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days + 1)):
		#week_num = date.isocalendar()[1]
		#print(date.strftime('%Y-%m-%d'),"is in week number",week_num)



    qs = Impact.objects.filter(icn_id=1).annotate(Count('indicators', distinct=True))
    
        
	  
    print(qs[0].indicators__count)
            


@register.filter(name='jsonify')
def jsonify(data):
    if isinstance(data, dict):
        return data
    else:
        return json.loads(data)

  labels = []
  data = []
  gdp = GDP.objects.values('country').annotate(agdp=Avg('gdp')).annotate(sgdp=Sum('gdp')).order_by('-agdp')
  for item in gdp:
    print(item)

	file = open('C:/Users/Habtamu-MC/Desktop/IPTS/programlist.csv')
	read_file = csv.reader(file)
	
	Program.objects.all().delete()

	count = 1
	
	for record in read_file:
		if count == 1:
			pass
		else:
			
			# Example usage
			date_string1 = record[4]
			result_datetime1 = convert_to_datetime(date_string1)
			date_string2 = record[4]
			result_datetime2= convert_to_datetime(date_string2)
		
 
			
			Program.objects.create(title = record[0], description = record[1], donor = record[2],
								fund_code = record[3], start_date = result_datetime1 , end_date = result_datetime2)
		
			
		count = count + 1
		


	def convert_to_datetime(input_str, parserinfo=None):
	
    	return parse(input_str, parserinfo=parserinfo)
"""