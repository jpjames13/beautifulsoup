# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 03:31:24 2017

@author: 4b53nc3
@author: Carnage
@author: H0ld71lls71ll
@author: M4573R(master) 
"""

from bs4 import BeautifulSoup
import csv
import glob
import os
import time
import re

base_path = "\\Users\\Carnage\\"
file_path = base_path+"\Desktop\Arizona State\POST_OPT\iTunesProductivity"



"""
    when main is called, it reads .about information from apptopia 
    and writes to a csv file.
"""
serverErrorUrls = []

"""
    when main is called, it reads .about information from apptopia 
    and writes to a csv file.
"""
def main():
    
    ###############################################
    '''
        Edit these variable to name your CSV file's
    '''
    ###############################################
    about_data_fileName = "about_dataTEST3"
    version_data_fileName = "version_dataTEST3"
    ###############################################
    ###############################################
    
    os.chdir(file_path)
    #writing headers
    writeAboutHeader(file_path,about_data_fileName)
    writeVersionHeader(file_path,version_data_fileName)
    writeAboutErrorLogHeader()    
    
    for file_type in glob.glob('*about.htm'):
        url = file_type
        appID = getAppID(url)
               
        #soup_ will be meant for about data
        soup_ = readHTML(file_type)
        
        #_soup will be meant for version data
        # _soup = readHTML(file_type)
        
        try:
            #gets about data in table format
            aboutDataTable =  (ReturnAboutTable(appID,soup_))
            #gets version data in table format
            versionDataTable =  (ReturnVersionTable(appID,soup_))
            
            #file name needs to be in quotations in the argument for write to csv method to be in seperate files
            WriteToCsv(aboutDataTable,about_data_fileName)
            
            #uncomment this later !!!!!!!!!!!!!!!!!!!
            WriteToCsv(versionDataTable,version_data_fileName)
        except IndexError as ex:
            print("Internal Error 500")
            WriteToAboutErrorLog(appID,url,"Internal Error 500")
            pass
        except AttributeError as ex:
            print("oops!", ex)
            WriteToAboutErrorLog(appID,url,ex)
            pass
        except TypeError as ex:
            print("oops!", ex) 
            WriteToAboutErrorLog(appID,url,ex)  
        except Exception as ex:
            print("oops!", ex)
            WriteToAboutErrorLog(appID,url,ex)
            pass

    print("Finished Processing")

    os.chdir(file_path)
    writeCSVHeader()
    writeErrorLogHeader()

    for file_type in glob.glob ('*sdk.htm'):

        try:
            print('Currently Processing ... '+file_type)
            url = file_path+file_type
            appID = getSDKID(url)
            soup = readHTML(file_type)

            if serverError(soup):
                writeServerErrorToErrorLog(url,appID,soup)
            elif paidAppsNoSDKInfo(soup):
                writeDotAsNullSDKInfo(soup,appID)
            else:
                dataTable = (returnTable(soup,appID))
                writeToCsv(dataTable)

        except Exception:
        	print("oops! exception")
        	writeGenericErrorToErrorLog(url,appID,'Exception')
        	pass
        except AttributeError:
        	print("oops! attribute")
        	writeGenericErrorToErrorLog(url,appID,'Attribute')
        	pass
        except TypeError:
            print("oops! type")
            writeGenericErrorToErrorLog(url,appId, 'Type')

    print('\nFinished Processing SDK Pages')

'''
    readHTML method reads input path
'''
def readHTML(InputPath):
    
    try:
        page = open(InputPath).read()
        soup = BeautifulSoup(page, "html.parser")
        return soup
    except Exception:
        print("oops! exception")
        pass
    except AttributeError:
        print("oops! attribute")
        pass
    except TypeError:
        print("oops! type")
        pass
'''
    END OF METHOD
'''
###############################################################################    
'''
    ReturnAboutTable method will return a table containing the necessary 
    .about data pulled from apptopia.
'''
def ReturnAboutTable(appid,_soup):
        
    #list variables
    appNames = ""
    ratingstars = []
    ratingstar = ""
    alltimeRating = []
    last30daysRate = []
    appDescriptions = []
    table = []
    #temporary variable to check if ratings exists
    tempVar = []
    day30check = []
    
    #10 stars variables
    listOf30DayStars = []
    listOfAllTimeStars = []

    star1_30day = []
    star2_30day = []
    star3_30day = []
    star4_30day = []
    star5_30day = []
    star1_AllTime = []
    star2_AllTime = []
    star3_AllTime = []
    star4_AllTime = []
    star5_AllTime = []
    
    #saves appName to a list
    for appInfo in _soup.find('main', attrs={'id': 'content'}):
        for appName in appInfo.findAll("div",{"class":"media-body"}):
            appNames = (appName.find('h1').text)  

#==============================================================================
# fixed errors on 8/20    
#==============================================================================

       
    #Checks to see if 30 ratings or all time ratings even exists
    for contents in _soup.find_all("section",{"class":"page-section"}):
        for div in contents.find_all("div",{"class":"text-center"}):
            tempVar.append(div.text)
            
    for div in _soup.find_all("div",{"class":"text-center"}):
        day30check.append(div.text)
    #print(day30check[1])
     
    #Checking ratings before assigning
    if "This app has not yet been rated." in tempVar[0]:
        star1_30day.append(".")
        star2_30day.append(".")
        star3_30day.append(".")
        star4_30day.append(".")
        star5_30day.append(".")
                
        star1_AllTime.append(".")
        star2_AllTime.append(".")
        star3_AllTime.append(".")
        star4_AllTime.append(".")
        star5_AllTime.append(".")
    elif day30check[1] == ('This app has no ratings in the last 30 days.'):
        #if function that checks 
        #for star attributes
        AllTimetableInDiv = _soup.find("div",{"id":"ratings-1"})   
        table_2 = AllTimetableInDiv.find("table")
        
        #Finds star ratings in All Time
        for td in table_2.find_all("td",{"class":"quiet text-right"}):
            for j in td:
                listOfAllTimeStars.append(re.findall('\d+(?:\.\d+)?[A-Z]?', str(j)))
        
        star1_30day.append(".")
        star2_30day.append(".")
        star3_30day.append(".")
        star4_30day.append(".")
        star5_30day.append(".")
        
        star1_AllTime = (listOfAllTimeStars[0])
        star2_AllTime = (listOfAllTimeStars[1])
        star3_AllTime = (listOfAllTimeStars[2])
        star4_AllTime = (listOfAllTimeStars[3])
        star5_AllTime = (listOfAllTimeStars[4])
    elif day30check[1] != ('This app has no ratings in the last 30 days.'):
        #if function that checks 
        #for star attributes
        #print("we did it")
        tableInDiv = _soup.find("div",{"id":"ratings-0"})   
        table_1 = tableInDiv.find("table")
        AllTimetableInDiv = _soup.find("div",{"id":"ratings-1"})   
        table_2 = AllTimetableInDiv.find("table")
        
        #Finds star ratings in 30 days tab        
        for td in table_1.find_all("td",{"class":"quiet text-right"}):
            for i in td:
                listOf30DayStars.append(re.findall('\d+(?:\.\d+)?[A-Z]?', str(i)))
        
        #Finds star ratings in All Time
        for td in table_2.find_all("td",{"class":"quiet text-right"}):
            for j in td:
                listOfAllTimeStars.append(re.findall('\d+(?:\.\d+)?[A-Z]?', str(j)))
        
        star1_30day = (listOf30DayStars[0])
        star2_30day = (listOf30DayStars[1])
        star3_30day = (listOf30DayStars[2])
        star4_30day = (listOf30DayStars[3])
        star5_30day = (listOf30DayStars[4])
                
        star1_AllTime = (listOfAllTimeStars[0])
        star2_AllTime = (listOfAllTimeStars[1])
        star3_AllTime = (listOfAllTimeStars[2])
        star4_AllTime = (listOfAllTimeStars[3])
        star5_AllTime = (listOfAllTimeStars[4])

#==============================================================================
# 8/20/2017 fixed errors
#==============================================================================

    #prints out ratings
    for ratings in _soup.findAll("div",{"class":"rating_allstars"}):
    #    print(ratings.find('div'))
        ratingstar = ratings.find('div')
        #converting the none type object to a 1-5 scale with the ConvertRatings method
        ratingstars = ConvertRatings(ratingstar)
        
        #prints out total ratings
        for checkAllTime in _soup.find("div",{"class":"h-tab-item hide"}):
            #totalraters.append(totalratings.find('div').text)           
            alltime = (_soup.findAll("div",{"class":"stat-huge text-center"}))
            try:

                #utilizing regex to extract int from css 
                #list of 2 ints 1st is 30 days 2nd is all time
                ratinglist = re.findall('\d+(?:\.\d+)?[A-Z]?', str(alltime))
                
                if len(ratinglist)>1:
                    alltimeRating = (ratinglist[1])
                    last30daysRate = (ratinglist[0])
                else:
                    #even if there is no last 30 day rating there might be all time
                    alltimeRating = (ratinglist[0])
                    
            except:
                x = ""       

                if x == "":
                    null = "."
                    alltimeRating = null
                    last30daysRate = null

    #print(versions)
    
    #extracts app description
    for description in _soup.findAll("div",{"class":"app-description"}):
        appDescriptions_ = (description.find('p').text)
        appDescriptions = appDescriptions_
                                    
    #appending list to table to be returned
        row = []               
        row.append(appid)
        row.append(appNames.replace("\n","").replace(",","").replace("<br>",""))
        row.append(kIsBad(ratingstars))        
        row.append(kIsBad(alltimeRating))
        row.append(kIsBad(last30daysRate))
        row.append(appDescriptions.replace("\n","").replace(",","").replace("<br>",""))
        row.append(kIsBad(star1_30day[0]))
        row.append(kIsBad(star2_30day[0]))
        row.append(kIsBad(star3_30day[0]))
        row.append(kIsBad(star4_30day[0]))
        row.append(kIsBad(star5_30day[0]))
        row.append(kIsBad(star1_AllTime[0]))
        row.append(kIsBad(star2_AllTime[0]))
        row.append(kIsBad(star3_AllTime[0]))
        row.append(kIsBad(star4_AllTime[0]))
        row.append(kIsBad(star5_AllTime[0]))
        table.append(row)
        
        return table

'''
    END OF METHOD
'''
###############################################################################
'''
    ReturnVersionTable method will return a table containing the necessary 
    .version data pulled from apptopia.
'''
def ReturnVersionTable(appId,soup_):
    #table variables
    table1 = soup_.find('table')
    table_rows = table1.find_all('tr')

    #list variables
    appNames = ""
    descriptions = []
    versions = []
    versionMonth = []
    versionYear = []
    #ratingstars = ""
    #totalraters = []
    #alltimeRating = []
    #last30daysRate = []
    table = []
    #types of data to be extracted
    
    #saves appName and descriptions to a list
    for appInfo in soup_.find('main', attrs={'id': 'content'}):
        for appName in appInfo.findAll("div",{"class":"media-body"}):
            appNames = (appName.find('h1').text)
            #print(appNames)
        for description in appInfo.findAll("div",{"class":"version-description"}):
            desc = (description.find('p').text)
            
            #if no description then text becomes a "." period
            if desc != "":
                descriptions.append(desc)
            else:
                null = "."
                descriptions.append(null)
    
    #saves versionsNo, version month and year to list
    for tr in table_rows:
        for i in tr.find_all('h3'):
            #this represents the version no
            versions.append(i.text)
        for i in tr.find_all("div",{"class":"month"}):
            versionMonth.append(i.text)
        for i in tr.find_all("div",{"class":"year"}):
            versionYear.append(i.text)
                                    
    #appending list to table to be returned
    for i in range(len(versions)):
        row = []
        row.append(appId)
        row.append(appNames)
        row.append(versions[i].replace("Version ",""))
        row.append(versionYear[i]+" "+versionMonth[i])
        #row.append(versionYear[i])
        #the .replace function only works with strings
        #you've been screwing up because you were trying to use the function on
        #list objects
        row.append(descriptions[i].replace("\n","").replace(",","").replace("<br>",""))
        table.append(row)
        
    return table

'''
    END OF METHOD
'''
###############################################################################
'''
    This method checks to see if app is rated
'''
def ValidateRatings(soop):
    
    invalidstr = "This app has not yet been rated."
    null = False
    valid = True
    
    for appInfo in soop.find('div', attrs={'class': 'text-center'}):
        x = (appInfo.text) 
    
    if x == invalidstr:
        return (null)
    else:
        return valid

###############################################################################

'''
    WriteToCsv method is quite intuitive
'''
#write to csv now takes two arguments
def WriteToCsv(tableInput,fileName):
    with open(fileName+".csv", 'a') as myFile:        
       for row in tableInput:
        for column in row:
            #if column .contains /n then remove 
            myFile.write('%s,' % column)
        myFile.write('\n')
       #identify which rows script is processing
       print("Currently Processing ... "+row[1])
       myFile.close
   
'''
    END OF METHOD
'''
###############################################################################

'''
    WriteToErrorLog method is quite intuitive
'''
#write to csv now takes two arguments
def WriteToAboutErrorLog(appId,url,exception):
    
    row = []
    table = []
    row.append(appId)
    row.append(url)
    row.append(exception)
    
    for i in row:         
        table.append(i)
    
    with open('about_ErrorLog.csv', 'a',newline='') as f:
        writer = csv.writer(f)  
        writer.writerow(table)

   
'''
    END OF METHOD
'''

###############################################################################
def writeAboutErrorLogHeader():
    header = ['App_ID', 'URL', 'Exception']
    with open('about_ErrorLog.csv', 'w+',newline='') as f:
        dw = csv.DictWriter(f, fieldnames = header)
        dw.writeheader()
###############################################################################
'''
    None type object conversion method for Ratings
'''
def ConvertRatings(noneType):
        
        #converting the damn none type object to a string
        ratingstar_ = str(noneType)

        #using regex, this saves the floating numbers or int from string to a list
        ratingstars__ = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", ratingstar_)
        
        #ratingstars__ is a list of [0]data-ce-keys where applies
        #and the floating numbers that we need for the ratings
        #if len list is more than 1 remove [0] first item and assign
        #to ratingstars 
        if len(ratingstars__) > 1:
            x = ratingstars__[1:]
            ratingstars = x[0]
        else:
            ratingstars = ratingstars__[0]
        
        ratingstar = float(ratingstars)
        
        #scaling it to 5 stars
        rating = 5*(ratingstar/100)
        
        #round down to 2 decimals
        ratings = str(round(rating, 2))
        
        return ratings
###############################################################################
'''
    Method gets App Id
'''
def getAppID(url):
    appID = url.replace("_about.htm","")
    return appID

###############################################################################
'''
    Write Header Method
'''
def writeAboutHeader(filepath, fileName):
    header = ["App_ID", "App_Name", "All_Time_Ratings", "Total_Raters","No_Raters_last_30Days", "App_Description","star1_30day","star2_30day","star3_30day","star4_30day","star5_30day","star1_AllTime","star2_AllTime","star3_AllTime","star4_AllTime","star5_AllTime"]
    with open(filepath+'/'+fileName+'.csv','w+',newline='') as f:
        dw = csv.DictWriter(f, fieldnames = header)
        dw.writeheader()
        
###############################################################################
###############################################################################
'''
    Write Header Method
'''
def writeVersionHeader(filePath,FileName):
    header = ["App_ID", "App_Name", "Version_No.", "Version_Date","Version_Description"]
    with open(filePath+'/'+FileName+'.csv','w+',newline='') as f:
        dw = csv.DictWriter(f, fieldnames = header)
        dw.writeheader()
        
###############################################################################
'''
    Converting K to 000 and M to 000000 
'''
def kIsBad(x):
    
    y = 0
    j = []

    if 'K' in x:
        b = x.replace("K","")
        y = float(b) * 1000
        return y
    if 'M' in x:
        b = x.replace('M', '')
        y = int(b) * 1000000
        return y
    if 'B' in x:
        b= x.replace('B', '')
        y = int(b) * 1000000000
        return y
    #if its an empty list
    elif x == j:
        return (".")
    else:
        return x
            
#retrieve SDK-ID
def getSDKID(url):
    appID = (url.rsplit('/',1)[1]).rsplit('_',1)[0]
    return appID

def getAppName(soup):
    for h1 in soup.find('h1',{'class':'text-lg text-normal text-truncate m-b-xxxs m-r-xs l-h-xs'}):
                appName = h1.text
    return appName

#If there's an error in SDK, print to CSV
def serverError(soup):
    serverError = soup.find('div',{'class':'card card-sm m-x-auto'})

    if serverError:
       return True
    else:
       return False

def writeErrorLogHeader():
    header = ['App_ID', 'File_Location', 'Error_Description']
    with open('ErrorLog.csv', 'w+') as f:
        dw = csv.DictWriter(f, fieldnames = header)
        dw.writeheader()

def writeServerErrorToErrorLog(url, appID, soup):
    errorMessageArray = []
    for p in soup.find_all('p', {'class': 'text-xxl text-light m-b'}):
        errorMessageArray.append((p).text)

    for i in range(len(errorMessageArray)):
        row = []
        table = []
        row.append(appID)
        row.append(url)
        row.append(errorMessageArray[i])
        table.append(row)

    with open('ErrorLog.csv','a') as f:

        writer = csv.writer(f)
        writer.writerow(table[i])

def writeGenericErrorToErrorLog(url, appId, errorMessage):
    
    errorMessage = ''
    row = []
    row.append(appId)
    row.append(url)
    row.append(errorMessage)

    with open('ErrorLog.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def paidAppsNoSDKInfo(soup):

    paid = soup.find('div',{'class':'no-content-block'})
    nA = soup.find('div',{'class':'text-xxs-center text-xs no-content-block-new'})
    
    if paid or nA:
        #print('Paid or N/A No SDK Info Avalibale')
        return True
    else:
        #print('Free')
        return False

def returnTable(soup,appID):

    appIDArray = []
    appNamesArray = []
    sdkIDArray = []
    sdkTypeArray = []
    sdkNamesArray = []
    sdkDateArray = []
    sdkStatusArray = []
    table = []

    for uniqueSDKS in soup.find('div', attrs={'id': 'all_sdks'}):
        for sdkNames in uniqueSDKS.find_all('td',{'class': 'sdk-link'}):
            sdkNamesArray.append(sdkNames.text)
            for anchor in sdkNames.find_all('a'):
                sdkIDArray.append(anchor['href'])
        for sdkDate in uniqueSDKS.find_all('td',{'class': 'sdk-date'}):
            if len(sdkDate.text) < 13 :
                sdkDateArray.append(sdkDate.text)
            else:
                sdkDateArray.append((sdkDate.text).rsplit(' ',1)[0])
        for sdkStatus in uniqueSDKS.find_all('td', {'class': 'sdk-status text-nowrap text-xxxs'}):
            sdkStatusArray.append(sdkStatus.text)
        numOfSDKSUnderOneType = len(uniqueSDKS.find_all('td',{'class': 'sdk-link'}))
        for typeHeader in uniqueSDKS.find_all('div', {'class': 'panel-header bg-gray d-flex flex-items-xxs-middle b-t b-b text-sm'}):
            for i in range(numOfSDKSUnderOneType):
                sdkTypeArray.append((typeHeader.span.text).rsplit(' ',1)[0])

    for i in range(len(sdkNamesArray)):
        appNamesArray.append(getAppName(soup))
        appIDArray.append(appID)
        row = []
        row.append(appIDArray[i])
        row.append(appNamesArray[i])
        row.append(sdkIDArray[i])
        row.append(sdkNamesArray[i])
        row.append(sdkTypeArray[i])
        row.append(sdkDateArray[i])
        row.append(sdkStatusArray[i])
        table.append(row)
    
    return table

def writeToCsv(tableInput):
    with open('sdk_Info.csv','a') as f:
        for i in range(len(tableInput)):
            writer = csv.writer(f)
            writer.writerow(tableInput[i])
            '''
            writer.csv.writer(f)
            writer.writerow(tableInput[i])
    '''
    #f.close()
    #done = True
        
def writeDotAsNullSDKInfo(soup, appID):
    arrayToPrintForNoSDKInfoApps = [appID,getAppName(soup),u"\u2022",u"\u2022",u"\u2022",u"\u2022",u"\u2022"]
    with open('sdk_Info.csv','a') as f:
        writer = csv.writer(f)

        writer.writerow(arrayToPrintForNoSDKInfoApps)

    #f.close()
    #done = True
def writeCSVHeader():
    header = ["App_ID", "App_Name", "SDK_ID", "SDK_Name", "SDK_Type","Install_Uninstall_Date", "Status"]
    with open('sdk_Info.csv','w+') as f:
        dw = csv.DictWriter(f, fieldnames = header)
        dw.writeheader()

#if this script is not being imported it will run main
if __name__ == '__main__':
    main()
