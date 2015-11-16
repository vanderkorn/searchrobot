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


class DriveComAuSyntaxAnalyzer(SyntaxAnalyzer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def AnalyzeList(self, htmlstring):
        pass
    @abstractmethod
    def AnalyzeItem(self, htmlstring):
        pass

class DriveComAuSyntaxAnalyzerImplement(DriveComAuSyntaxAnalyzer):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.rootListClassName = 'cT-searchResults'
        self.itemAttributeName = 'itemprop'
        self.itemAttributeValue = 'offers'
        self.itemPropertyName = 'itemprop'
        self.itemPropertyValueHeading = 'name'
        self.itemPropertyValueUrl = 'url'
        self.itemPropertyValueThumbnailUrl = 'image'
        self.itemPropertyValueDescription = 'description'
        self.itemPropertyValuePrice = 'price'
        self.itemClassNameBody = 'body'
        self.itemClassNameTransmission = 'transmission'
        self.itemClassNameEngine = 'engine'
        self.itemClassNameOdometer = 'odometer'
        self.itemClassNamePriceCondition = 'price'
        self.itemClassNamePriceLocation = 'location'
        self.itemClassNameAdType = 'type'

        self.rootDetailClassName = 'main'
        self.detailClassNameOriginal = 'jsImage'
        self.detailClassNameSpecification = 'accordion'
        self.detailTagValueColour = 'Colour'
        self.detailTagValueVIN = 'VIN no'
        self.detailTagValueFuelType = 'Fuel type'
        self.detailTagValueReleaseYear = 'Release Year'
        self.detailTagValueBadge = 'Badge'
        self.detailTagValueSeries = 'Series'
        self.detailTagValueGears = 'No. gears'
        self.detailTagSeatCapacity= 'Seat capacity'
        self.detailTagCountryOfOrigin= 'Country of origin'
        self.detailTagValueDoors = 'No. doors'
        self.detailTagValueKerbWeigh = 'Kerb Weight'
        self.detailTagValueFuelAverage = 'Average'


        self.detailClassAdditionalFeatures = 'list-std'




    def AnalyzeList(self, htmlstring):
        doc = html.fromstring(htmlstring)
        root = doc.xpath("//div[contains(@class, '%s')]" % self.rootListClassName)[0]
        items = root.xpath(".//li[@%s='%s']" % (self.itemAttributeName, self.itemAttributeValue))
        vehicles = list()
        for item in items:

            heading = item.xpath(".//a[@%s='%s']/text()" % (self.itemPropertyName, self.itemPropertyValueHeading))[0]
            urlList = item.xpath(".//a[@%s='%s']/@href" % (self.itemPropertyName, self.itemPropertyValueUrl))
            url = ''
            if len(urlList) > 0:
                url = urlList[0]
            else:
                continue

            thumbnailurl = item.xpath(".//img[@%s='%s']/@src" % (self.itemPropertyName, self.itemPropertyValueThumbnailUrl))[0]
            if 'no-image-available' in thumbnailurl : thumbnailurl = ''

            descriptionList = item.xpath(".//span[@%s='%s']/p/text()" % (self.itemPropertyName, self.itemPropertyValueDescription))
            description = ''
            if len(descriptionList) > 0 :
                description = descriptionList[0]

            pricelist = item.xpath(".//strong[@%s='%s']/text()" % (self.itemPropertyName, self.itemPropertyValuePrice))
            price = 0
            if len(pricelist) > 0 :
                price = pricelist[0]
                price = price.replace("$","")
                price = price.replace(",","")
                if  price.isdigit() == False : price=0

            #print(price)


            bodylist = item.xpath(".//dd[@class='%s']/text()" % (self.itemClassNameBody))
            body = ''
            if len(bodylist) > 0 :
                body = bodylist[0]

            transmissionList = item.xpath(".//dd[@class='%s']/text()" % (self.itemClassNameTransmission))
            transmission = ''
            if len(transmissionList) > 0 :
                transmission = transmissionList[0]

            enginelist = item.xpath(".//dd[@class='%s']/text()" % (self.itemClassNameEngine))
            engine = 0
            if len(enginelist) > 0 :
                engine = enginelist[0]
                engine = engine.replace(",",".")

            odometerlist = item.xpath(".//dd[@class='%s']/text()" % (self.itemClassNameOdometer))
            odometer = 0
            if len(odometerlist) > 0 :
                odometer = odometerlist[0]
                odometer = odometer.replace(",","")

            priceconditionlist = item.xpath(".//dd[@class='%s']/small/text()" % (self.itemClassNamePriceCondition))
            pricecondition = ''
            if len(priceconditionlist) > 0 :
                pricecondition = priceconditionlist[0]

            locationlist = item.xpath(".//dd[@class='%s']/abbr/@title" % (self.itemClassNamePriceLocation))
            location = ''
            if len(locationlist) > 0 :
                location = locationlist[0]

            adtype = item.xpath(".//dd[@class='%s']/text()" % (self.itemClassNameAdType))[0]
            dealer = ''
            if "Dealer" in adtype:
                dealer =  re.sub(r'\s+', '', adtype).replace("Dealer","").replace(":","")


            driveaway = pricecondition == "Drive Away"
            vehicles.append(Vehicle(Heading = str(heading), Url = str(url), ThumbnailUrl = str(thumbnailurl), Description = str(description), Price = Decimal(price), BodyType = str(body), Transmission = str(transmission), Engine = float(engine), Odometer = float(odometer), Location = str(location), DriveAway = driveaway, Dealer = dealer))
        return vehicles

    def AnalyzeItem(self, htmlstring):
        doc = html.fromstring(htmlstring)
        root = doc.xpath("//div[contains(@class, '%s')]" % self.rootDetailClassName)[0]

        originalurlList = list()
        scriptList = doc.xpath("//script[contains(., '%s')]/text()" % ('fullSizeImages'))
        if len(scriptList) > 0:
            script = scriptList[0]
            regex = re.compile(r"var fullSizeImages = \[(.*)\];", re.IGNORECASE)
            m = regex.search(script)
            if m is not None:
                urlsStr = m.group(1)
                urlsStr = urlsStr.strip()
                urlsStr = urlsStr.replace(' ', '')
                urlsStr = urlsStr.replace('\"', '')
                originalurlList = urlsStr.split(',')

        if len(originalurlList) == 0:
            originalurlList = root.xpath(".//img[@class='%s']/@src" % (self.detailClassNameOriginal))

        descriptions =  root.xpath("./p/text()")
        description = ' '.join([str(unidecode(x)) for x in descriptions])
        description = description.strip()

        specifications = root.xpath(".//ul[@class='%s']" % (self.detailClassNameSpecification))[0]

        colourlist = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueColour))
        colour = ''
        if len(colourlist) > 0 :
            colour = colourlist[0]

        vinlist = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueVIN))
        vin = ''
        if len(vinlist) > 0 :
            vin = vinlist[0]

        fuelTypeList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueFuelType))
        fuelType = ''
        if len(fuelTypeList) > 0 :
            fuelType = fuelTypeList[0]

        releaseYearList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueReleaseYear))
        releaseYear = 0
        if len(releaseYearList) > 0 :
            releaseYear = releaseYearList[0]

        badgeList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueBadge))
        badge = ''
        if len(badgeList) > 0 :
            badge = badgeList[0]

        seriesList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueSeries))
        series = ''
        if len(seriesList) > 0 :
            series = seriesList[0]

        gearsList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueGears))
        gears = 0
        if len(gearsList) > 0 :
            gears = gearsList[0]

        doorsList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueDoors))
        doors = 0
        if len(doorsList) > 0 :
            doors = doorsList[0]

        kerbWeighList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueKerbWeigh))
        kerbWeigh = 0
        if len(kerbWeighList) > 0 :
            kerbWeigh = kerbWeighList[0]

        fuelAverageList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagValueFuelAverage))
        fuelAverage = 0
        if len(fuelAverageList) > 0 :
            fuelAverage = fuelAverageList[0]
            fuelAverage = fuelAverage.strip()


        seatcapacityList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagSeatCapacity))
        seatcapacity = 0
        if len(seatcapacityList) > 0 :
            seatcapacity = seatcapacityList[0]

        countryOfOriginList = specifications.xpath(".//tr//*[text() = '%s']/following-sibling::td/text()" % (self.detailTagCountryOfOrigin))
        countryOfOrigin = ''
        if len(countryOfOriginList) > 0 :
            countryOfOrigin = countryOfOriginList[0]

        additionalFeaturesList = root.xpath(".//ul[@class='%s']//li/text()" % (self.detailClassAdditionalFeatures))
        additionalFeatures = ''
        if len(additionalFeaturesList) > 0 :
            additionalFeatures = ', '.join([str(unidecode(x)) for x in additionalFeaturesList])
            additionalFeatures = additionalFeatures.strip()


        return Vehicle(OriginalUrl=originalurlList, Description=str(description), AdditionalFeatures=str(additionalFeatures), Colour=str(colour), FuelAverage = float(fuelAverage), KerbWeight = int(kerbWeigh), Vin=str(vin), ReleaseYear=int(releaseYear), FuelType = str(fuelType), Badge=str(badge), Series=str(series), Gears=int(gears), SeatCapacity=int(seatcapacity),CountryOfOrigin=str(countryOfOrigin), Doors=int(doors))
        