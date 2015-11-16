__author__ = 'Van'
#-------------------------------------------------------------------------------
# Created on 14.12.2011
#
# @author: Van Der Korn
# @file: googlemachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
import lxml
import datetime
import lxml.html as html
from abc import ABCMeta, abstractmethod, abstractproperty
from  core.models.Vehicle import *
from decimal import *
from unidecode import unidecode
import re
from core.syntaxanalyzers.SyntaxanAlyzer import SyntaxAnalyzer
from urlparse import urlparse
class EbayComAuSyntaxAnalyzer(SyntaxAnalyzer):
    __metaclass__ = ABCMeta

    @abstractmethod
    def AnalyzeList(self, htmlstring):
        pass
    @abstractmethod
    def AnalyzeItem(self, htmlstring):
        pass

class EbayComAuSyntaxAnalyzerImplement(EbayComAuSyntaxAnalyzer):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.rootListIdName = 'ResultSetItems'
        self.itemsIdName = 'ListViewInner'
        self.itemClassNameHeading = 'lvtitle'
        self.itemClassNameDescription = 'lvsubtitle'
        self.itemClassNameThumbnailUrl = 'img'
        self.itemClassNamePrice = 'lvprice prc'
        self.itemClassNameDate = 'tme'


        self.detailIdName = 'Body'
        self.detailIdGalleryName = 'vi_main_img_fs_slider'
        self.detailIdConditionName = 'vi-itm-cond'
        self.detailSpecificationClassName = 'itemAttr'
        self.detailSpecificationItemClassName = 'attrLabels'
        self.detailPropertyNameDoors = 'Doors'
        self.detailPropertyNameMake = 'Manufacturer'
        self.detailPropertyNameColour = 'Colour'
        self.detailPropertyNameReleaseYear = 'Date of Manufacture'
        self.detailPropertyNameYear = 'Year of Manufacture'
        self.detailPropertyNameBodyType = 'Body Type'
        self.detailPropertyNameOdometer = 'Kilometres'
        self.detailPropertyNameTransmission = 'Transmission'
        self.detailPropertyNameFuelType = 'Fuel Type'
        self.detailPropertyNameModel = 'Model'
        self.detailPropertyNameSaleBy = 'For Sale by'
        self.detailPropertyNameEngine = 'Engine Size'
        self.detailPropertyNameAdditionalFeatures = 'Options'
        self.detailPropertyNameSafetyFeatures = 'Safety Features'
        self.detailPropertyNameVIN = 'Vehicle Identification Number'
        self.detailMainPhotoProperty = 'itemprop'
        self.detailMainPhotoPropertyValue = 'image'


    def AnalyzeList(self, htmlstring):
        doc = html.fromstring(htmlstring)
        root = doc.xpath("//div[@id='%s']" % self.rootListIdName)[0]

        items = root.xpath(".//ul[@id='%s']/li" % self.itemsIdName)

        vehicles = list()
        for item in items:

            heading = item.xpath(".//*[@class='%s']/a/text()" % (self.itemClassNameHeading))[0]
            heading = unidecode(heading.strip())
            url = item.xpath(".//*[@class='%s']/a/@href" % (self.itemClassNameHeading))[0]

            thumbnailurlList = item.xpath(".//img[contains(@class,'%s')]/@src" % self.itemClassNameThumbnailUrl)
            thumbnailurlList2 = item.xpath(".//img[contains(@class,'%s')]/@imgurl" % self.itemClassNameThumbnailUrl)
            if len(thumbnailurlList2) > 0 :
                thumbnailurlList = thumbnailurlList2
            thumbnailurl = ''
            if len(thumbnailurlList) > 0 :
                thumbnailurl = thumbnailurlList[0]

            descriptionList = item.xpath(".//*[@class='%s']/text()" % self.itemClassNameDescription)
            description = ''
            if len(descriptionList) > 0 :
                description = unidecode(description.strip())

            priceList = item.xpath(".//*[@class='%s']//text()" % self.itemClassNamePrice)

            price=0
            if len(priceList) > 0 :
                priceList = map(lambda s: unidecode(s).strip(),priceList)
                priceList = filter(bool, priceList)
                price = ''.join([str(x) for x in priceList])
                price = price.replace("AU","")
                price = price.replace("$","")
                price = price.replace(",","")
                price = price.replace(".00","")
                price = price.strip()
                if  price.isdigit() == False : price=0

            lastModifiedList = item.xpath(".//*[@class='%s']//text()" % (self.itemClassNameDate))
            lastModified = None
            if len(lastModifiedList) > 0 :
                lastModified = ' '.join([str(unidecode(x).strip()) for x in lastModifiedList])
                lastModified = lastModified.strip()
                lastModified = datetime.datetime.strptime(lastModified, "%d-%b %H:%M")
                lastModified = lastModified.replace(year = datetime.date.today().year)

            vehicles.append(Vehicle(Heading = str(heading), Url = str(url), ThumbnailUrl = str(thumbnailurl), Description = str(description), Price = Decimal(price), LastModified = lastModified))
        return vehicles

    def AnalyzeItem(self, htmlstring):
        doc = html.fromstring(htmlstring)

        root = doc.xpath("//div[@id='%s']" % self.detailIdName )[0]


        originalurlList = root.xpath("//div[@id='%s']//li//img/@src" % self.detailIdGalleryName)
        if len(originalurlList) == 0 :
            originalurlList = root.xpath(".//img[@%s='%s']/@src" % (self.detailMainPhotoProperty, self.detailMainPhotoPropertyValue))

        if len(originalurlList) > 0 :
            regex = re.compile(r"\$_([\d\(\)]+)\.", re.IGNORECASE)
            for i, originalurl in enumerate(originalurlList):
                originalurlList[i] = regex.sub('$_1.', originalurl)


        listingTypeList = root.xpath(".//div[@id='%s']/text()" % self.detailIdConditionName)
        isNew = False
        if len(listingTypeList) > 0 :
            listingType = listingTypeList[0]
            listingType = listingType.strip()
            if listingType == 'New':
                isNew =  True

        isPrivateSellerList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameSaleBy, self.detailSpecificationItemClassName))
        isPrivateSeller = False
        if len(isPrivateSellerList) > 0:
            isPrivateSellerStr = isPrivateSellerList[0]
            if isPrivateSellerStr == 'Private Seller':
                isPrivateSeller =  True

        doorsList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameDoors, self.detailSpecificationItemClassName))
        doors = 0
        if len(doorsList) > 0 :
            doors = doorsList[0]
            doors = doors.strip()

        makeList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameMake, self.detailSpecificationItemClassName))
        make = ''
        if len(makeList) > 0 :
            make = makeList[0]
            make = make.strip()

        colourlist = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameColour, self.detailSpecificationItemClassName))
        colour = ''
        if len(colourlist) > 0 :
            colour = colourlist[0]
            colour = colour.strip()

        releaseYearList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameReleaseYear, self.detailSpecificationItemClassName))
        releaseYear = 0
        if len(releaseYearList) > 0 :
            releaseYear = releaseYearList[0]
            releaseYear = releaseYear.strip()
            releaseDate = datetime.datetime.strptime(releaseYear, "%m/%Y")
            releaseYear = releaseDate.year
        else:
            releaseYearList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameYear, self.detailSpecificationItemClassName))
            if len(releaseYearList) > 0 :
                releaseYear = releaseYearList[0]
                releaseYear = releaseYear.strip()


        bodylist = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameBodyType, self.detailSpecificationItemClassName))
        body = ''
        if len(bodylist) > 0 :
            body = bodylist[0]
            body = body.strip()

        odometerlist = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameOdometer, self.detailSpecificationItemClassName))
        odometer = 0
        if len(odometerlist) > 0 :
            odometer = odometerlist[0]
            odometer = odometer.replace(",","")
            odometer = odometer.strip()

        transmissionList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameTransmission, self.detailSpecificationItemClassName))
        transmission = ''
        if len(transmissionList) > 0 :
            transmission = transmissionList[0]
            transmission = transmission.strip()

        fuelTypeList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameFuelType, self.detailSpecificationItemClassName))
        fuelType = ''
        if len(fuelTypeList) > 0 :
            fuelType = fuelTypeList[0]
            fuelType = fuelType.strip()

        modelList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameModel, self.detailSpecificationItemClassName))
        model = ''
        if len(modelList) > 0 :
            model = modelList[0]
            model = model.strip()

        enginelist =  root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameEngine, self.detailSpecificationItemClassName))
        engine = 0
        if len(enginelist) > 0 :
            engine = enginelist[0]
            engine = engine.strip()

        additionalFeaturesList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s') and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameAdditionalFeatures, self.detailSpecificationItemClassName))
        additionalFeatures = ''
        if len(additionalFeaturesList) > 0 :
            additionalFeatures =  additionalFeaturesList[0]
            additionalFeatures = additionalFeatures.strip()

        safetyFeaturesList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s')  and @class='%s']/following-sibling::td/span/text()" % (self.detailSpecificationClassName, self.detailPropertyNameSafetyFeatures, self.detailSpecificationItemClassName))
        safetyFeature = ''
        if len(safetyFeaturesList) > 0 :
            safetyFeature =  safetyFeaturesList[0]
            safetyFeature = safetyFeature.strip()
        additionalFeatures = additionalFeatures + ' ' + safetyFeature

        vinList = root.xpath(".//div[@class='%s']//td[contains(text(),'%s')  and @class='%s']/following-sibling::td/b/a/text()" % (self.detailSpecificationClassName, self.detailPropertyNameVIN, self.detailSpecificationItemClassName))
        vin = ''
        if len(vinList) > 0 :
            vin = vinList[0]
            vin = vin.strip()

        return Vehicle(OriginalUrl=originalurlList, AdditionalFeatures=str(additionalFeatures), BodyType = str(body), Transmission = str(transmission), Engine = float(engine), Odometer = float(odometer), IsPrivateSeller = isPrivateSeller, Model=str(model), Make=str(make), Colour=str(colour), ReleaseYear=int(releaseYear), FuelType = str(fuelType), Vin=str(vin), Doors=int(doors), IsNew = isNew)
