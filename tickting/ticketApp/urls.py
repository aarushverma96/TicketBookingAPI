from django.conf.urls import url
from ticketApp import views



urlpatterns = [

	url(r'^screens/$', views.acceptDetails),
	url(r'^screens/(?P<screen_name>[A-Za-z][\w-]+)/reserve$', views.reserveTickets),
	url(r'^screens/(?P<screen_name>[A-Za-z][\w-]+)/seats$', views.unreservedSeats)


]