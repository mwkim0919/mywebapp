# Create your views here.
import datetime
import urllib2

from django.contrib import auth
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.utils import timezone

from forms import RegistrationForm
from park.models import *
import park.parse