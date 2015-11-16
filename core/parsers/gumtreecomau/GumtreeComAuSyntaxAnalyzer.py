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
class GumtreeComAuSyntaxAnalyzer(SyntaxAnalyzer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def AnalyzeList(self, htmlstring):
        pass
    @abstractmethod
    def AnalyzeItem(self, htmlstring):
        pass

class GumtreeComAuSyntaxAnalyzerImplement(GumtreeComAuSyntaxAnalyzer):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.rootListIdName = 'srchrslt-adtable'
        self.itemPropertyName = 'itemprop'
        self.itemPropertyItemsValue = 'offers'

        self.itemPropertyHeading = 'name'
        self.itemPropertyUrl = 'url'
        self.itemPropertyThumbnailUrl = 'image'
        self.itemPropertyDescription = 'description'
        self.itemPropertyPrice = 'price'

        self.itemClassLocation = 'rs-ad-field rs-ad-location'


        self.galleryDetailIdName = 'ad-gallery'
        self.bodyDetailIdName = 'ad-body'
        self.titleDetailClassName = 'row-fluid c-position-relative'
        self.detailClassNameOriginal = 'carousel-item'
        self.detailIdNameDescription = 'ad-description'
        self.detailClassNameLocation = 'j-google-map-link c-pointer'
        self.detailPropertyNameLocation = 'data-address'
        self.detailPropertyNameLatitude = 'data-lat'
        self.detailPropertyNameLongitude = 'data-lng'
        self.detailClassNameAttribute = 'ad-attribute'
        self.detailDateValue = 'Date Listed'
        self.detailIdNameAttributeListingType = 'c-cars.forsaleby_s-wrapper'
        self.detailIdNameAttributeMake = 'c-cars.carmake_s-wrapper'
        self.detailIdNameAttributeModel = 'c-cars.carmodel_s-wrapper'
        self.detailIdNameAttributeYear = 'c-cars.caryear_i-wrapper'
        self.detailIdNameAttributeColour = 'c-cars.colour_s-wrapper'
        self.detailIdNameAttributeBodyType = 'c-cars.carbodytype_s-wrapper'
        self.detailIdNameAttributeTransmission = 'c-cars.cartransmission_s-wrapper'
        self.detailIdNameAttributeOdometer = 'c-cars.carmileageinkms_i-wrapper'
        self.detailIdNameAttributeFuelType = 'c-cars.fueltype_s-wrapper'
        self.detailClassAdditionalFeatures = 'std-feature'
        self.detailTagValueDoors = 'No of Doors'
        self.detailTagValueGears = 'No of Seats'
        self.detailTagCountryOfOrigin= 'Country Of Origin'
        self.detailTagSeatCapacity= 'No of Seats'
        self.detailTagValueKerbWeigh = 'Kerb Weight'
        self.detailTagValueFuelAverage = 'Fuel Consumption City'
        self.detailTagValueEngine = 'Engine Capacity Litres'
        self.detailClassNmaeSpec = 'spec'
        self.detailTagValueCylinder = 'Cylinder Configuration'

    def AnalyzeList(self, htmlstring):
        doc = html.fromstring(htmlstring)
        root = doc.xpath("//ul[@id='%s']" % self.rootListIdName)[0]

        items = root.xpath(".//li[@%s='%s']" % (self.itemPropertyName, self.itemPropertyItemsValue))

        vehicles = list()
        for item in items:

            heading = item.xpath(".//span[@%s='%s']/text()" % (self.itemPropertyName, self.itemPropertyHeading))[0]
            heading = heading.strip()
            url = item.xpath(".//a[@%s='%s']/@href" % (self.itemPropertyName, self.itemPropertyUrl))[0]

            thumbnailurlList = item.xpath(".//img[@%s='%s']/@src" % (self.itemPropertyName, self.itemPropertyThumbnailUrl))
            thumbnailurl = ''
            if len(thumbnailurlList) > 0 :
                thumbnailurl = thumbnailurlList[0]

            descriptionList = item.xpath(".//p[@%s='%s']/span/text()" % (self.itemPropertyName, self.itemPropertyDescription))
            description = ''
            if len(descriptionList) > 0 :
                description = ' '.join([str(unidecode(x)) for x in descriptionList])
                description = description.strip()

            priceList = item.xpath(".//div[@%s='%s']/text()" % (self.itemPropertyName, self.itemPropertyPrice))

            price=0
            if len(priceList) > 0 :
                price = priceList[0]
                price = price.strip()
                price = price.replace("$","")
                price = price.replace(",","")
                price = price.replace(".00","")
                if  price.isdigit() == False : price=0

            locationlist = item.xpath(".//div[@class='%s']//text()" % (self.itemClassLocation))
            location = ''
            if len(locationlist) > 0 :
                location = ' '.join([str(unidecode(x).strip()) for x in locationlist])
                location = location.strip()

            vehicles.append(Vehicle(Heading = str(heading), Url = str(url), ThumbnailUrl = str(thumbnailurl), Description = str(description), Price = Decimal(price), Location = str(location)))
        return vehicles

    def AnalyzeItem(self, htmlstring):
        doc = html.fromstring(htmlstring)

        rootTitle = doc.xpath("//div[@class='%s']" % self.titleDetailClassName )[0]

        rootBody = doc.xpath("//div[@id='%s']" % self.bodyDetailIdName )[0]

        rootGalleryList = doc.xpath("//div[@id='%s']" % self.galleryDetailIdName)
        originalurlList = ''
        if len(rootGalleryList) > 0 :
            rootGallery = rootGalleryList[0]
            originalurlList = rootGallery.xpath(".//li[contains(@class, '%s')]/span/@data-href-large" % (self.detailClassNameOriginal))

        descriptionsList =  rootBody.xpath("//div[@id='%s']/text()" % self.detailIdNameDescription)
        description = ''
        if len(descriptionsList) > 0 :
            descriptionsList = map(lambda s: s.strip(),descriptionsList)
            descriptionsList = filter(bool, descriptionsList)
            description = '\n '.join([str(unidecode(x)) for x in descriptionsList])
            description = description.strip().encode('utf8')

        addressList = rootTitle.xpath(".//span[@class='%s']/@%s" % (self.detailClassNameLocation, self.detailPropertyNameLocation))
        address = ''
        if len(addressList) > 0:
            address = addressList[0]
            address = address.strip()

        latList = rootTitle.xpath(".//span[@class='%s']/@%s" % (self.detailClassNameLocation, self.detailPropertyNameLatitude))
        latitude = 0
        if len(latList) > 0:
            latitude = latList[0]
            latitude = latitude.strip()

        lngList = rootTitle.xpath(".//span[@class='%s']/@%s" % (self.detailClassNameLocation, self.detailPropertyNameLongitude))
        longitude = 0
        if len(lngList) > 0:
            longitude = lngList[0]
            longitude = longitude.strip()

        #kerbWeighList = specifications.xpath(".//div[@class='row']//*[contains(text(),'%s')]/../following-sibling::div/div/text()" % (self.detailTagValueKerbWeigh))

        lastModifiedList = rootBody.xpath(".//dl[@class='%s']//dt[contains(text(),'%s')]/following-sibling::dd/text()" % (self.detailClassNameAttribute, self.detailDateValue))
        lastModified = None
        if len(lastModifiedList) > 0 :
            lastModified = lastModifiedList[0]
            lastModified = lastModified.strip()
            lastModified = datetime.datetime.strptime(lastModified, "%d/%m/%Y")

        listingTypeList = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd/text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeListingType))
        privateSellerCar = False
        if len(listingTypeList) > 0 :
            listingType = listingTypeList[0]
            listingType = listingType.strip()
            if listingType == 'Private seller':
                privateSellerCar =  True

        makeList = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd//text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeMake))
        make = ''
        if len(makeList) > 0 :
            makeList = map(lambda s: s.strip(),makeList)
            makeList = filter(bool, makeList)
            make = ' '.join([str(x) for x in makeList])
            make = make.strip()

        modelList = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd//text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeModel))
        model = ''
        if len(modelList) > 0 :
            modelList = map(lambda s: s.strip(),modelList)
            modelList = filter(bool, modelList)
            model = ' '.join([str(x) for x in modelList])
            model = model.strip()

        releaseYearList = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd//text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeYear))
        releaseYear = 0
        if len(releaseYearList) > 0 :
            releaseYearList = map(lambda s: s.strip(),releaseYearList)
            releaseYearList = filter(bool, releaseYearList)
            releaseYear = ''.join([str(x) for x in releaseYearList])
            releaseYear = releaseYear.strip()


        colourlist = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd/text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeColour))
        colour = ''
        if len(colourlist) > 0 :
            colour = colourlist[0]
            colour = colour.strip()

        bodylist = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd/text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeBodyType))
        body = ''
        if len(bodylist) > 0 :
            body = bodylist[0]
            body = body.strip()

        transmissionList = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd/text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeTransmission))
        transmission = ''
        if len(transmissionList) > 0 :
            transmission = transmissionList[0]
            transmission = transmission.strip()

        odometerlist = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd/text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeOdometer))
        odometer = 0
        if len(odometerlist) > 0 :
            odometer = odometerlist[0]
            odometer = odometer.replace(",","")
            odometer = odometer.strip()

        fuelTypeList = rootBody.xpath(".//dl[@class='%s' and @id='%s']/dd/text()" % (self.detailClassNameAttribute, self.detailIdNameAttributeFuelType))
        fuelType = ''
        if len(fuelTypeList) > 0 :
            fuelType = fuelTypeList[0]
            fuelType = fuelType.strip()

        additionalFeaturesList = rootBody.xpath("//li[@class='%s']/text()" % (self.detailClassAdditionalFeatures))
        additionalFeatures = ''
        if len(additionalFeaturesList) > 0 :
            additionalFeaturesList = map(lambda s: s.strip(),additionalFeaturesList)
            additionalFeaturesList = filter(bool, additionalFeaturesList)
            additionalFeatures = ', '.join([str(unidecode(x)) for x in additionalFeaturesList])
            additionalFeatures = additionalFeatures.strip()

        doorsList = rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec, self.detailTagValueDoors))
        doors = 0
        if len(doorsList) > 0 :
            doors = doorsList[0]
            doors = doors.strip()

        countryOfOriginList = rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec, self.detailTagCountryOfOrigin))
        countryOfOrigin = ''
        if len(countryOfOriginList) > 0 :
            countryOfOrigin = countryOfOriginList[0]
            countryOfOrigin = countryOfOrigin.strip()

        seatcapacityList = rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec, self.detailTagSeatCapacity))
        seatcapacity = 0
        if len(seatcapacityList) > 0 :
            seatcapacity = seatcapacityList[0]
            seatcapacity = seatcapacity.strip()

        kerbWeighList = rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec, self.detailTagValueKerbWeigh))
        kerbWeigh = 0
        if len(kerbWeighList) > 0 :
            kerbWeigh = kerbWeighList[0]
            kerbWeigh = kerbWeigh.replace("kg","")
            kerbWeigh = kerbWeigh.strip()

        fuelAverageList =  rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec, self.detailTagValueFuelAverage))
        fuelAverage = 0
        if len(fuelAverageList) > 0 :
            fuelAverage = fuelAverageList[0]
            fuelAverage = fuelAverage.strip()

        enginelist =  rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec, self.detailTagValueEngine))
        engine = 0
        if len(enginelist) > 0 :
            engine = enginelist[0]
            engine = engine.replace("L","")
            engine = engine.strip()

        cylinderlist =  rootBody.xpath("//li[@class='%s']//span[contains(text(),'%s')]/following-sibling::span/text()" % (self.detailClassNmaeSpec,self.detailTagValueCylinder))
        cylinder = 0
        if len(cylinderlist) > 0 :
            cylinder = cylinderlist[0]
            r = re.findall(r'\d+', cylinder)
            cylinder = r[0]



        return Vehicle(OriginalUrl=originalurlList, Description=str(description), AdditionalFeatures=str(additionalFeatures), BodyType = str(body), Transmission = str(transmission), Engine = float(engine), Odometer = float(odometer), IsPrivateSeller = privateSellerCar, Model=str(model), Make=str(make), Coordinate = ("%s,%s" % (float(latitude), float(longitude))), Colour=str(colour), FuelAverage = float(fuelAverage), KerbWeight = int(kerbWeigh), ReleaseYear=int(releaseYear), FuelType = str(fuelType), SeatCapacity=int(seatcapacity),CountryOfOrigin=str(countryOfOrigin), Doors=int(doors), LastModified=lastModified)
