# API Guide

## Introduction

This document summarises all the API calls one would need for PeaceTrack Mobile Apps and MACC to communicate. The project uses Django REST Framework for the API implemenation. In this document, I have written the `curl` requests for each task. Android and iOS apps must find the equivalent of these requests or how to implement these requests in Java and Swift respectively. 
 
## Overview

Django REST Framework provides us clean and easy URLs for API access. We can use `curl` requests to thee URLs for easy data acess. Following are some of the plus points to django-rest-framework.

1. Easy to extend their Serializer base class to create custom serializers and
resources
2. Well-documented
3. More flexible than TastyPie, less opinionated, and wonderfully architected.
4. API Browser that comes automatically with DRF has proved itself to be
invaluable.
5. Ease-of-use

For further information about it, please refer: [Django REST Framework documentation](http://www.django-rest-framework.org/)

## API Root

To access the API root visit the following URL:

	http://10.2.194.247:8001/api/

Replace the IP address with the IP address of your server. If you get an Authentication Error, make sure to login and the accont used for login sould have privilege to access APIs. From here you can access the data for all of the models by visiting the corresponding links from the API Root. For example, to access the goals visi:  http://10.2.194.247:8001/api/goals/

## Accessing the APIs programmatially

While interacting with the API through the web browser, we can login, and the browser session will provide the required authentication for the requests. If we're interacting with the API programmatically we need to explicitly provide the authentication credentials on each request.

If we try to create a snippet without authenticating as follows, we'll get an error.
	
	$ curl -X GET http://10.2.194.247:8001/api/goals/
	{"detail": "Authentication credentials were not provided."}

We make this request succesful by adding the username and password. Since we'll need the data in JSON format we add "?format=json" at the end of the URL. The following will successfully fetch all the goals in JSON format.

	$ curl -X GET http://10.2.194.247:8001/api/goals/?format=json -u admin:mypassword
	{"count": 1, "next": "null", "previous": null, "results": [{"goal_name": "Goal 1: Improve Teaching", "goal_title": "Improve Teaching", "goal_stmt": "Improve Teaching by training teachers by experts", "goal_project": 1, "id": 1}]}

**Make sure to replace the IP address correctly**

### Accessing Posts

Use the following to fetch all Posts

	$ curl -X GET http://10.2.194.247:8001/api/ptposts/?format=json -u admin:mypassword

Use the following to fetch the Post who's `id` = 1

	$ curl -X GET http://10.2.194.247:8001/api/ptposts/1/?format=json -u admin:mypassword

Replace the `1` here with the `id` of the post you need

Use the following to create a new Post 

	$ curl -X POST -H "Content-Type: application/json" http://10.2.194.247:8001/api/ptposts/ -d '{"post_name": "Thailand", "post_region": 1, "sector": [1, 2]}' -u admin:mypassword

Use the following to modify a Post who's `id` = 1
	
	$ curl -X PUT -H "Content-Type: application/json" http://10.2.194.247:8001/api/ptposts/1/ -d '{"post_name": "Thailand", "post_region": 1, "sector": [1, 2, 4], "id": 1}' -u admin:mypassword

Replace the `1` here with the `id` of the post you need

### Accessing Sectors

Use the following to fetch all Sectors

	$ curl -X GET http://10.2.194.247:8001/api/sectors/?format=json -u admin:mypassword

Use the following to fetch the Sector who's `id` = 1

	$ curl -X GET http://10.2.194.247:8001/api/sectors/1/?format=json -u admin:mypassword

Replace the `1` here with the `id` of the sector you need

Use the following to create a new Sector

	$ curl -X POST -H "Content-Type: application/json" http://10.2.194.247:8001/api/sectors/ -d '{"sector_name": "Education", "sector_desc": "Improve Education", "sector_code": "ED"}' -u admin:mypassword

Use the following to modify a Sector who's `id` = 1
	
	$ curl -X PUT -H "Content-Type: application/json" http://10.2.194.247:8001/api/sectors/1/ -d '{"sector_name": "Education", "sector_desc": "Improve Rural Education", "sector_code": "ED", "id": 1}' -u admin:mypassword

Replace the `1` here with the `id` of the sector you need

Use the following to fetch the Sectors belonging to a Post

	$ curl -X GET http://10.2.194.247:8001/api/ptposts/?post_sectors=True&id=1&format=json -u admin:mypassword

Make sure to use the id of the Post who's Sectors you want to fetch as a value for the parameter `id`

### Accessing Projects

Use the following to fetch all Projects

	$ curl -X GET http://10.2.194.247:8001/api/projects/?format=json -u admin:mypassword

