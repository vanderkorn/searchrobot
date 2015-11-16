# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: searchmachine.py
#-------------------------------------------------------------------------------

class Vehicle(object):
    '''
    classdocs
    '''


    def __init__(self, Heading = "", Description = "", Url = "", ThumbnailUrl = "", OriginalUrl = "", BodyType = "", Transmission = "", Engine = 0, Odometer = 0, Price = 0, Location = "", DriveAway = False, CountryOfOrigin = "", Vin = "", ReleaseYear = 0, Colour = "", FuelAverage=0, KerbWeight=0, FuelType = "", Badge = "", Series = "", Gears = 0, Doors=0, SeatCapacity=0 ,Dealer = "", TotalDealerPrice=False, AdditionalFeatures = "", IsNew = False, IsPrivateSeller = False, LastModified = None , Make = "", Model = "", Coordinate = ''):
        '''
        Constructor
        '''
        self.Heading = Heading
        self.Description = Description
        self.Url = Url
        self.ThumbnailUrl = ThumbnailUrl
        self.OriginalUrl = OriginalUrl
        self.BodyType = BodyType
        self.Transmission = Transmission
        self.Engine = Engine
        self.Odometer = Odometer
        self.Price = Price
        self.Location = Location
        self.DriveAway = DriveAway
        self.CountryOfOrigin = CountryOfOrigin
        self.Vin = Vin
        self.ReleaseYear = ReleaseYear
        self.Colour = Colour
        self.FuelAverage = FuelAverage
        self.KerbWeight = KerbWeight
        self.FuelType = FuelType
        self.Badge = Badge
        self.Series = Series
        self.Gears = Gears
        self.Doors = Doors
        self.SeatCapacity = SeatCapacity
        self.Dealer = Dealer
        self.TotalDealerPrice = TotalDealerPrice
        self.AdditionalFeatures = AdditionalFeatures
        self.IsNew = IsNew
        self.IsPrivateSeller = IsPrivateSeller
        self.LastModified = LastModified
        self.Make = Make
        self.Model = Model
        self.Coordinate = Coordinate

