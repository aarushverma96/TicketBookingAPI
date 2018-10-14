from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from ticketApp.models import *
import json


'''
Functionalty that accept the details of screen and saves the information in the database 
saves information about seat structure, screen name and row 
'''
@api_view(['POST'])
def acceptDetails(request):
	data=request.data 																					  #Accessing the data form the request
	screen_name=data['name']	                                                                          #Assigning the screen name
	seatinfo=data['seatinfo']
	for r in seatinfo:																					  #Accessing the rows in the seat structure
		rows=seatinfo[r]
		row=r
		number_of_seats = rows['numberofSeats']
		aisle= rows['aisle']
		seat_structure=[]
		for i in range(0,number_of_seats):																   #Assigning the asile seats
			seat_structure.append(-1)
		for i in aisle:
			seat_structure[i]=-2
		str1=','.join(str(e) for e in seat_structure)
		s=Screens(screen_name=screen_name,rows=row,number_of_seats=number_of_seats,seats_structure=str1)   #Creating object of screens
		s.save()																						   #Saving the object


	#print(seatinfo)

	return HttpResponse(status=200)																		   #returning Http 200 response


'''
Api that reserve the tickets, accepts the request with screen, seat choice and return Http 200 if seats are avialable
and booked successfully else return Http 203 if seats are not booked
'''
@api_view(['POST'])
def reserveTickets(request,screen_name):
	data=request.data;
	reqSeats=data['seats']										#Accessing the requested seats
	available=1
	for  seats in reqSeats:
		reqRow=seats
		prevScreen=Screens.objects.get(screen_name=screen_name,rows=reqRow) #Accessing the requested screen object from the database
		prevseatStruct=prevScreen.seats_structure
		prevseatStruct = prevseatStruct.split(',')
		prevseatStructint = list(map(int, prevseatStruct))
		for i in reqSeats[seats]:
			if prevseatStructint[i] > 0:
				available=0
		if available == 0:
			return HttpResponse(status=203)                                #Returning http 203 if seats are not available 


		for i in reqSeats[seats]:										   #Booking the seats if seats are available
			if prevseatStruct[i] > '0':
				return HttpResponse(status=203)
			elif prevseatStruct[i] == '-2':
				prevseatStruct[i] = '2'
			elif prevseatStruct[i]== '-1':
				prevseatStruct[i]='1'
		str1=','.join(prevseatStruct)
		prevScreen.seats_structure=str1										#saving to the data base after booking the seats
		prevScreen.save()
			

	return HttpResponse(status=200)											#Returning Http 200 if seats are booked successfully

	

'''
Api that accepts request screen name, status as unreserved ans return json response with available seats in that screen.
'''

'''
Api that accepts request with screen name and number of seats to be booked and choices of seats and return available seats 
in the adjacent and contigous.  
'''
@api_view(['GET'])
def unreservedSeats(request,screen_name):
	if request.GET.get('status',''):					#If status is present in get request show unreserved seats
		status=request.GET['status']
		prevScreen=Screens.objects.filter(screen_name=screen_name) #Accessing the screen object

		response_data={}
		res_data2={}

		for obj in prevScreen:
			prevseatStruct=obj.seats_structure.split(',')
			resList=[]
			resRow=obj.rows
			prevseatStruct = list(map(int, prevseatStruct))
			for i in range(0,len(prevseatStruct)):			#checking for the unreserved seats in the seat structure
				if prevseatStruct[i]<0:
					resList.append(i)
			res_data2[resRow]=resList	
			response_data["seats"]=res_data2				#appending unreserved seats

		return JsonResponse(response_data,safe=False)       #returning json response of the unreserved data

	else:													#If number of seats and choice is given
		window=int(request.GET['numSeats'])
		choice=request.GET['choice']
		row=choice[0]
		ch=int(choice[1:len(choice)])
		reqScreen=Screens.objects.get(screen_name=screen_name,rows=row)
		seatStruct=reqScreen.seats_structure.split(',')
		seatStruct=list(map(int, seatStruct))
		

		res_data={}
		ans={}

		for i in range(ch-window+1,ch+1): 								#checking for the available seats using the sliding window concept
			availStruct=seatStruct[i:i+window]


			if 1 in availStruct or 2 in availStruct:
				pass
			elif -2 in availStruct:
				if availStruct[-1]==-2 and availStruct.count(-2)==1:
					seats=[]
					for j in range(i, i+window):
						seats.append(j)
					res_data[row] = seats
				else:
					pass
			else:
				seats=[]
				for j in range(i,i+window):
					seats.append(j)
				res_data[row]=seats

		error={"Error":"Seats not avaiable"}

		if len(res_data)==0:
			return JsonResponse(error,safe=False)   					#returning the error if no seats are avialable

		ans['avaiableSeats']=res_data 								    #Appending to the final list

		return JsonResponse(ans,safe=False)								#Returning the Json response of the choices of available seats
	