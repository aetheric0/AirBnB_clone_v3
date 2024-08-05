#!/usr/bin/python3
""" Blueprint Creator
"""
from flask import Blueprint, render_template
from api.v1.views.index import *

app_views = Blueprint(url_prefix='/api/v1')
