import datetime

__author__ = 'Van'
#-------------------------------------------------------------------------------
# Created on 14.12.2011
#
# @author: Van Der Korn
# @file: googlemachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
import lxml
import lxml.html as html
from abc import ABCMeta, abstractmethod, abstractproperty
from  core.models.Vehicle import *
from decimal import *
from unidecode import unidecode
import re
from core.syntaxanalyzers.SyntaxanAlyzer import SyntaxAnalyzer
from urlparse import urlparse
class CarsalesComAuSyntaxAnalyzer(SyntaxAnalyzer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def AnalyzeList(self, htmlstring):
        pass
    @abstractmethod
    def AnalyzeItem(self, htmlstring):
        pass

class CarsalesComAuSyntaxAnalyzerImplement(CarsalesComAuSyntaxAnalyzer):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.rootListClassName = 'result-set-container'
        self.itemClassName = 'result-item'
        self.itemTagHeading = 'h2'
        self.itemClassThumbnailUrl = 'image-thumb'
        self.itemClassDescription = 'comments'

        self.itemClassPrice = 'primary-price'
        self.itemClassPriceProperty = 'data-price'

        self.itemClassBody = 'item-body'
        self.itemClassTransmission = 'item-transmission'
        self.itemClassEngine = 'item-engine'
        self.itemClassOdometer = 'item-odometer'
        self.itemClassLocation = 'call-to-action'
        self.itemClassPriceCondition = 'PriceType'
        self.itemClassAdType = 'ad-type'
        self.__location_dicts = {'ACT': 'ACT', 'NSW': 'New South Wales', 'NT': 'Northern Territory', 'QLD': 'Queensland', 'SA': 'South Australia', 'TAS': 'Tasmania', 'VIC': 'Victoria', 'WA': 'Western Australia'}


        self.rootDetailClassName = 'details'
        self.detailClassNameOriginal = 'media-gallery-footer'
        self.detailClassNameDescription = 'view-more-target'
        self.detailClassNameInfo = 'vertical table-striped'
        self.detailTagValueColour = 'Colour'
        self.detailIdSpecifications = 'specifications'
        self.detailTagValueFuelType = 'Fuel Type'
        self.detailTagValueReleaseYear = 'Launch Year'
        self.detailTagValueBadge = 'Badge'
        self.detailTagValueSeries = 'Series'
        self.detailTagValueDoors = 'Doors'
        self.detailTagValueGears = 'Gears'
        self.detailTagCountryOfOrigin= 'Country of Origin'
        self.detailTagSeatCapacity= 'Seat Capacity'
        self.detailTagValueFuelAverage = 'Fuel Consumption Combined'
        self.detailTagValueKerbWeigh = 'Kerb Weight'
        self.detailClassAdditionalFeatures = 'features-Standard'
        self.detailTagValueLastModified = 'Last Modified'


        self.detailTagValueVIN = 'VIN no'






    def AnalyzeList(self, htmlstring):
        doc = html.fromstring(htmlstring)
        root = doc.xpath("//div[contains(@class, '%s')]" % self.rootListClassName)[0]
        items = root.xpath(".//div[contains(@class, '%s')]" % self.itemClassName)
        vehicles = list()
        for item in items:

            heading = item.xpath(".//%s/a/text()" % (self.itemTagHeading))[0]
            heading = heading.strip()
            url = item.xpath(".//%s/a/@href" % (self.itemTagHeading))[0]

            thumbnailurl = item.xpath(".//a[@class='%s']/img/@src" % (self.itemClassThumbnailUrl))[0]
            if 'no-image' in thumbnailurl : thumbnailurl = ''

            descriptionList = item.xpath(".//div[@class='%s']/p/text()" % (self.itemClassDescription))
            description = ''
            if len(descriptionList) > 0 :
                description = descriptionList[0]

            priceList = item.xpath(".//div[@class='%s']/a/@%s" % (self.itemClassPrice, self.itemClassPriceProperty))

            price=0
            if len(priceList) > 0 :
                price = priceList[0]
                if  price.isdigit() == False : price=0

            #print(price)

            bodylist = item.xpath(".//li[@class='%s']/text()" % (self.itemClassBody))
            body = ''
            if len(bodylist) > 0 :
                body = bodylist[0]

            transmissionList = item.xpath(".//li[@class='%s']/text()" % (self.itemClassTransmission))
            transmission = ''
            if len(transmissionList) > 0 :
                transmission = transmissionList[0]

            enginelist = item.xpath(".//li[@class='%s']/text()" % (self.itemClassEngine))
            engine = 0
            cylinder = 0
            if len(enginelist) > 0 :
                engine = enginelist[0]
                engine = engine.strip()
                prog = re.compile('^(?P<cyl>[\d|\.]+)cyl\s(?P<engine>[\d|\.]+)L', re.IGNORECASE)
                m = prog.search(engine)
                cylinder = m.group('cyl')
                engine = m.group('engine')

            odometerlist = item.xpath(".//li[@class='%s']/text()" % (self.itemClassOdometer))
            odometer = 0
            if len(odometerlist) > 0 :
                odometer = odometerlist[0]
                odometer = odometer.replace(",","")
                odometer = odometer.replace("km","")
                odometer = odometer.strip()

            locationlist = item.xpath(".//div[@class='%s']/p/text()" % (self.itemClassLocation))
            location = ''
            if len(locationlist) > 0 :
                location = locationlist[0]
                location = location.strip()
                if location in self.__location_dicts:
                    location = self.__location_dicts[location]


            priceconditionlist = item.xpath(".//a[contains(@class, '%s')]/text()" % (self.itemClassPriceCondition))
            pricecondition = ''
            if len(priceconditionlist) > 0 :
                pricecondition = priceconditionlist[0]
                pricecondition = pricecondition.strip()

            adtype = item.xpath(".//div[@class='%s']/p/span/text()" % (self.itemClassAdType))[0]
            dealer = ''
            if "Dealer" in adtype:
                prog = re.compile('(?<=Dealer:)[\s|\w]+', re.IGNORECASE)
                m = prog.search(adtype)
                dealer = m.group(0)

            privateSellerCar = False
            if adtype == 'Private Seller Car':
                privateSellerCar =  True

            newCar = False
            if 'New Car' in adtype:
                newCar =  True

            driveaway = pricecondition == "Drive Away"

            vehicles.append(Vehicle(Heading = str(heading), Url = str(url), ThumbnailUrl = str(thumbnailurl), Description = str(description), Price = Decimal(price), BodyType = str(body), Transmission = str(transmission), Engine = float(engine), Odometer = float(odometer), Location = str(location), DriveAway = driveaway, Dealer = dealer, IsPrivateSeller = privateSellerCar, IsNew = newCar))
        return vehicles

    def AnalyzeItem(self, htmlstring):
        doc = html.fromstring(htmlstring)
        root = doc.xpath("//div[@class='%s']" % self.rootDetailClassName)[0]

        originalurlList = root.xpath(".//div[@class='%s']//img/@src" % (self.detailClassNameOriginal))
        if len(originalurlList) > 0 :
            for ndx, url in enumerate(originalurlList):
                o = urlparse(url)
                url_without_query_string = o.scheme + "://" + o.netloc + o.path
                originalurlList[ndx] = url_without_query_string

        descriptionsList =  root.xpath("//div[@class='%s']/p/text()" % self.detailClassNameDescription)
        description = ''
        if len(descriptionsList) > 0 :
            description = descriptionsList[0]
            description = description.strip().encode('utf8')

        info = root.xpath(".//table[@class='%s']" % (self.detailClassNameInfo))[0]

        colourlist = info.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueColour))
        colour = ''
        if len(colourlist) > 0 :
            colour = colourlist[0]

        lastModifiedList = info.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueLastModified))
        lastModified = None
        if len(lastModifiedList) > 0 :
            lastModified = lastModifiedList[0]
            lastModified = datetime.datetime.strptime(lastModified, "%d/%m/%Y")

        specifications = root.xpath(".//div[@id='%s']" % (self.detailIdSpecifications))[0]
        fuelTypeList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueFuelType))
        fuelType = ''
        if len(fuelTypeList) > 0 :
            fuelType = fuelTypeList[0]
            fuelType = fuelType.strip()


        releaseYearList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueReleaseYear))
        releaseYear = 0
        if len(releaseYearList) > 0 :
            releaseYear = releaseYearList[0]
            releaseYear = releaseYear.strip()

        badgeList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueBadge))
        badge = ''
        if len(badgeList) > 0 :
            badge = badgeList[0]
            badge = badge.strip()

        seriesList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueSeries))
        series = ''
        if len(seriesList) > 0 :
            series = seriesList[0]
            series = series.strip()

        gearsList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueGears))
        gears = 0
        if len(gearsList) > 0 :
            gears = gearsList[0]
            gears = gears.strip()

        doorsList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueDoors))
        doors = 0
        if len(doorsList) > 0 :
            doors = doorsList[0]
            doors = doors.strip()

        countryOfOriginList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagCountryOfOrigin))
        countryOfOrigin = ''
        if len(countryOfOriginList) > 0 :
            countryOfOrigin = countryOfOriginList[0]
            countryOfOrigin = countryOfOrigin.strip()

        seatcapacityList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagSeatCapacity))
        seatcapacity = 0
        if len(seatcapacityList) > 0 :
            seatcapacity = seatcapacityList[0]
            seatcapacity = seatcapacity.strip()

        fuelAverageList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueFuelAverage))
        fuelAverage = 0
        if len(fuelAverageList) > 0 :
            fuelAverage = fuelAverageList[0]
            fuelAverage = fuelAverage.replace("(L/100km)","")
            fuelAverage = fuelAverage.strip()


        kerbWeighList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueKerbWeigh))
        kerbWeigh = 0
        if len(kerbWeighList) > 0 :
            kerbWeigh = kerbWeighList[0]
            kerbWeigh = kerbWeigh.replace("(kg)","")
            kerbWeigh = kerbWeigh.strip()

        additionalFeaturesList = root.xpath(".//ul[@id='%s']//div[@class='col-7']//text()" % (self.detailClassAdditionalFeatures))

        additionalFeatures = ''
        if len(additionalFeaturesList) > 0 :
            additionalFeaturesList = map(lambda s: s.strip(),additionalFeaturesList)
            additionalFeaturesList = filter(bool, additionalFeaturesList)
            additionalFeatures = ', '.join([str(unidecode(x)) for x in additionalFeaturesList])
            additionalFeatures = additionalFeatures.strip()


        return Vehicle(OriginalUrl=originalurlList, Description=str(description), AdditionalFeatures=str(additionalFeatures), Colour=str(colour), FuelAverage = float(fuelAverage), KerbWeight = int(kerbWeigh), ReleaseYear=int(releaseYear), FuelType = str(fuelType), Badge=str(badge), Series=str(series), Gears=int(gears), SeatCapacity=int(seatcapacity),CountryOfOrigin=str(countryOfOrigin), Doors=int(doors), LastModified=lastModified)
