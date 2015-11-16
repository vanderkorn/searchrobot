#!/usr/bin/python 
#-------------------------------------------------------------------------------
# Created on 13.04.2015
# 
# @author: Van Der Korn
# @file: robo.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

from  core.robots.SearchRobot import *
from  core.robots.Dependencer import *



# create sites
# hosts = ['www.carsales.com.au']
hosts = ['www.ebay.com.au', 'www.gumtree.com.au', 'www.drive.com.au', 'www.carsales.com.au']
# count of ads
count = 5000
# register dependencies IOC
Dependencer.RegisterDependencies()
# create Search Robot instance
robot = SearchRobot()
# Run parsing sites parallel
robot.IndexParallel(hosts, count)

# hosts = ['www.drive.com.au']
# count = 10
# Dependencer.RegisterDependencies()
# robot = SearchRobot()
# robot.Index(hosts, count)

