import numpy,http.client
import pandas as pd
import datetime


def downloadHTML(baseURL,fName):
    conn=http.client.HTTPSConnection(baseURL)
    conn.request("GET",fName,headers={"User-Agent":"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.11) Gecko/2009060311 Ubuntu/8.10 (intrepid) Firefox/3.0.11"} )
    resp=conn.getresponse()
    return str(resp.read()) 

def getElection(baseURL,fName,splitter,colIdx):
    content=downloadHTML(baseURL,fName)
    numbersSection=content.split(splitter)[1].split('</table>')[0]
    stateRows=numbersSection.split('United States presidential election in ')[1:]
    stateDict=dict()
    for row in stateRows:
        state=row.split('"')[0].strip().replace('the District','District').replace(' (state)','')
        #print(state)
        #print(row)
        #print(row.split('<td>')[colIdx].split('</td>')[0].strip().replace('%',''))
        repubShare=float(row.split('<td>')[colIdx].split('</td>')[0].strip().replace('%',''))
        stateDict[state]=repubShare
    return stateDict

abbrevDict={'Oklahoma':'OK', 'Arkansas':'AR',
 'New York':'NY', 
 'Oregon':'OR',
 'West Virginia':'WV', 
 'New Mexico':'NM',
 'Maryland':'MD',
 'Utah':'UT',
 'Georgia':'GA', 
 'South Carolina':'SC', 
 'Minnesota':"MN",
 'Virginia':'VA', 
 'Michigan':"MI", 
 'Hawaii':'HI', 
 'Maine':"ME", 
 'Puerto Rico':"PR",
 'Tennessee':'TN', 
 'Montana':'MT',
 'Idaho':'ID', 
 'Mississippi':"MS",
 'California':"CA", 
 'South Dakota':'SD',
 'Missouri':'MO',
 'Colorado':'CO',
 'Illinois':'IL',
 'Delaware':'DE', 
 'Louisiana':'LA', 
 'New York City':'NYC',
 'Kentucky':'KY',
 'Connecticut':'CT', 
 'Nebraska':'NE',
 'Ohio':'OH',
 'Washington':'WA', 
 'United States':"US", 
 'Massachusetts':"MA",
 'North Dakota':'ND', 
 'District of Columbia':'DC', 
 'the District of Columbia':'DC',           
 'Vermont':'VT',
 'New Hampshire':'NH',
 'Iowa':'IA',
 'Nevada':'NV',
 'Alabama':'AL',
 'Arizona':"AZ",
 'North Carolina':'NC', 
 'Wisconsin':'WI',
 'New Jersey':"NJ",
 'Rhode Island':'RI',
 'Texas':"TX", 
 'Alaska':'AK', 
 'Pennsylvania':"PA",
 'Wyoming':"WY",
 'Indiana':"IN",
 'Kansas':"KS",
 'Florida':"FL"}


 
def getPovertyRate():
    content=downloadHTML("en.wikipedia.org","/wiki/List_of_U.S._states_and_territories_by_poverty_rate")    
    content=content.replace('"flagicon"><a href="/wiki/Georgia_(U.S._state)" title="Georgia (U.S. state)"','"flagicon">')
    stateRows=content.split('/wiki/United_States"')[1].split('</table>')[0].strip().split("/wiki/")[1:]
    stateDct=dict()
    for row in stateRows[0:51]:
        if (row.find('title="Georgia') != -1):
            state='Georgia'
        else:
            state=row.split('>')[1].split('</a')[0].strip()
        povRate=float(row.split('<td>')[1].split('</td>')[0].replace('%','').strip().replace('\\n','').split('<sup')[0])
        stateDct[state]=povRate
    return stateDct


def getGini():
    #not used but valuable for double-checking purposes; ACS from 2019 is used for gini
    content=downloadHTML("en.wikipedia.org","/wiki/List_of_U.S._states_by_Gini_coefficient")
    stateRows=content.split('federal district')[1].split('</table>')[0].strip().split("<tr>")[1:]
    stateDct=dict()
    for row in stateRows:
        state=row.split('</a>')[0].split('>')[-1].strip()
        #print(state)
        #print(row)
        gini=float(row.split('<td>')[3].split('</td')[0].strip().replace('\\n',''))
        stateDct[state]=gini
    return stateDct
#    print(stateRows[0:5])
 

def getHumidity():
    content=downloadHTML('www.forbes.com','/sites/brianbrettschneider/2018/08/23/oh-the-humidity-why-is-alaska-the-most-humid-state/?sh=6e6afa6a330c') 
    #content=open('view-source:https://www.forbes.com/sites/brianbrettschneider/2018/08/23/oh-the-humidity-why-is-alaska-the-most-humid-state/?sh=6e6afa6a330c','r').read()  
    #import pdb; pdb.set_trace()
    stateRows=content.split('Average RH')[1].split('</table>')[0].strip().split("<tr>")[1:]
    stateDct=dict()
    #import pdb; pdb.set_trace()
    for row in stateRows:
        #print(row)
        state=row.split('<td>')[1].split('</td>')[0].strip()
        #print(state)
        humidity=float(row.split('<td>')[2].split('</td>')[0].strip().replace('%',''))
        #print(humidity)
        #import pdb; pdb.set_trace()
        stateDct[state]=humidity
    #double check this later
    stateDct['District of Columbia']=64
    return stateDct

def getDewPoint():
    content=downloadHTML('www.forbes.com','/sites/brianbrettschneider/2018/08/23/oh-the-humidity-why-is-alaska-the-most-humid-state/?sh=6e6afa6a330c') 
    #content=open('view-source:https://www.forbes.com/sites/brianbrettschneider/2018/08/23/oh-the-humidity-why-is-alaska-the-most-humid-state/?sh=6e6afa6a330c','r').read()  
    #import pdb; pdb.set_trace()
    stateRows=content.split('Average RH')[1].split('</table>')[0].strip().split("<tr>")[1:]
    stateDct=dict()
    #import pdb; pdb.set_trace()
    for row in stateRows:
        #print(row)
        state=row.split('<td>')[1].split('</td>')[0].strip()
        #print(state)
        dewPoint=float(row.split('<td>')[4].split('</td>')[0].strip().replace('\\xc2\\xb0F',''))
        #print(humidity)
        #import pdb; pdb.set_trace()
        stateDct[state]=dewPoint
    #double check this later
    stateDct['District of Columbia']=46.8
    return stateDct


#source: https://www.beckershospitalreview.com/rankings-and-ratings/states-ranked-by-uninsured-rates.html
uninsuredContent='''
<p>Texas: 29 percent<br /><br />Florida: 25 percent</p>
<p>Oklahoma: 24 percent <br /><br />Georgia: 23 percent</p>
<p>Mississippi: 22 percent <br /><br />Nevada: 21 percent&nbsp;</p>
<p>North Carolina: 20 percent<br /><br />South Carolina: 20 percent</p>
<p>Alabama: 19 percent<br /><br />Tennessee: 19 percent<br /><br />Idaho: 18 percent<br /><br />Alaska: 17 percent<br /><br />Arizona: 17 percent</p>
<p>Missouri: 17 percent <br /><br />Wyoming: 17 percent<br /><br />New Mexico: 16 percent <br /><br />South Dakota: 16 percent<br /><br />Arkansas: 15 percent<br /><br />Kansas: 15 percent<br /><br />Louisiana: 14 percent<br /><br />Virginia: 14 percent<br /><br />California: 13 percent<br /><br />Colorado: 13 percent<br /><br />Illinois: 13 percent<br /><br />Indiana: 13 percent<br /><br />Maine: 13 percent<br /><br />Montana: 13 percent<br /><br />New Jersey: 13 percent <br /><br />Oregon: 13 percent<br /><br />Utah: 13 percent<br /><br />Michigan: 12 percent <br /><br />Nebraska: 12 percent<br /><br />Washington: 12 percent<br /><br />West Virginia: 12 percent<br /><br />Delaware: 11 percent<br /><br />Maryland: 11 percent</p>
<p>New Hampshire: 11 percent <br /><br />North Dakota: 11 percent<br /><br />Ohio: 11 percent<br /><br />Connecticut: 10 percent<br /><br />Hawaii: 10 percent<br /><br />Kentucky: 10 percent<br /><br />New York: 10 percent <br /><br />Pennsylvania: 10 percent<br /><br />Wisconsin: 10 percent<br /><br />Iowa: 9 percent<br /><br />Rhode Island: 9 percent<br /><br />Massachusetts: 8 percent</p>
<p>Minnesota: 8 percent&nbsp;</p>
<p>Vermont: 7 percent&nbsp;</p>
<p>District of Columbia: 6 percent</p>
'''

def getUninsured():
    stateRows=uninsuredContent.split('<p>')[1:]
    stateDct=dict()
    for row in stateRows:
        row=row.replace('</p>\\r\\n','').replace('</p>','').replace('&nbsp;','')
        if (row.find('<br /><br />') != -1):
            rowSplits=row.split('<br /><br />')
        else:
            rowSplits=[row]
        for rs in rowSplits:
            state=rs.split(':')[0].strip()
            #print('state is',sthttps://thefactfile.org/u-s-states-and-their-border-states/ate)
            #print(rs)
            #print('row is',row)
            pct=float(rs.split(':')[1].replace(' percent','').strip())
            stateDct[state]=pct
    return stateDct
    

def getBorderStates():
     content=downloadHTML('thefactfile.org','/u-s-states-and-their-border-states/')
     content=content.replace('<br /> (The state which borders only one other U.S. state.)','')
     content=content.replace('<br /> (The state which touches the most other states.)','')
     content=content.replace('\\t','')
     content=content.replace('(water border)','')  
     rows=content.split('Number of bordering states')[1].split('</tb>')[0].split('<tr ')[1:]
     stateDct=dict()
     for row in rows:
        state=row.split('noreferrer">')[1].split('<')[0].strip()
        #print(state)
        if (state=='Wyoming'):
            borderingStates='Nebraska, South Dakota, Utah, Colorado, Idaho, Montana'
        else:
            borderingStates=row.split(state)[1].split('</a></td><td class="column-3">')[1].split('<')[0].strip()
        borderingStates=borderingStates.split(',')
        filt=[]
        for bo in borderingStates:
            if (bo.strip() != ''):
                filt.append(bo.strip())
        if (state=='Virginia'):
            stateDct[state]=['North Carolina','Tennessee','West Virginia','Kentucky','Maryland']
        else:
            stateDct[state]=filt
     return stateDct 

borderStatesCache={'Alabama': ['Mississippi', 'Tennessee', 'Florida', 'Georgia'], 'Alaska': ['None'], 'Arizona': ['Nevada', 'New Mexico', 'Utah', 'California', 'Colorado'], 'Arkansas': ['Oklahoma', 'Tennessee', 'Texas', 'Louisiana', 'Mississippi', 'Missouri'], 'California': ['Oregon', 'Arizona', 'Nevada'], 'Colorado': ['New Mexico', 'Oklahoma', 'Utah', 'Wyoming', 'Arizona', 'Kansas', 'Nebraska'], 'Connecticut': ['New York', 'Rhode Island', 'Massachusetts'], 'Delaware': ['New Jersey', 'Pennsylvania', 'Maryland'], 'Florida': ['Georgia', 'Alabama'], 'Georgia': ['North Carolina', 'South Carolina', 'Tennessee', 'Alabama', 'Florida'], 'Hawaii': ['None'], 'Idaho': ['Utah', 'Washington', 'Wyoming', 'Montana', 'Nevada', 'Oregon'], 'Illinois': ['Kentucky', 'Missouri', 'Wisconsin', 'Indiana', 'Iowa', 'Michigan'], 'Indiana': ['Michigan', 'Ohio', 'Illinois', 'Kentucky'], 'Iowa': ['Nebraska', 'South Dakota', 'Wisconsin', 'Illinois', 'Minnesota', 'Missouri'], 'Kansas': ['Nebraska', 'Oklahoma', 'Colorado', 'Missouri'], 'Kentucky': ['Tennessee', 'Virginia', 'West Virginia', 'Illinois', 'Indiana', 'Missouri', 'Ohio'], 'Louisiana': ['Texas', 'Arkansas', 'Mississippi'], 'Maine': ['New Hampshire'], 'Maryland': ['Virginia', 'West Virginia', 'Delaware', 'Pennsylvania'], 'Massachusetts': ['New York', 'Rhode Island', 'Vermont', 'Connecticut', 'New Hampshire'], 'Michigan': ['Ohio', 'Wisconsin', 'Illinois', 'Indiana', 'Minnesota'], 'Minnesota': ['North Dakota', 'South Dakota', 'Wisconsin', 'Iowa', 'Michigan'], 'Mississippi': ['Louisiana', 'Tennessee', 'Alabama', 'Arkansas'], 'Missouri': ['Nebraska', 'Oklahoma', 'Tennessee', 'Arkansas', 'Illinois', 'Iowa', 'Kansas', 'Kentucky'], 'Montana': ['South Dakota', 'Wyoming', 'Idaho', 'North Dakota'], 'Nebraska': ['Missouri', 'South Dakota', 'Wyoming', 'Colorado', 'Iowa', 'Kansas'], 'Nevada': ['Idaho', 'Oregon', 'Utah', 'Arizona', 'California'], 'New Hampshire': ['Vermont', 'Maine', 'Massachusetts'], 'New Jersey': ['Pennsylvania', 'Delaware', 'New York'], 'New Mexico': ['Oklahoma', 'Texas', 'Utah', 'Arizona', 'Colorado'], 'New York': ['Pennsylvania', 'Rhode Island', 'Vermont', 'Connecticut', 'Massachusetts', 'New Jersey'], 'North Carolina': ['Tennessee', 'Virginia', 'Georgia', 'South Carolina'], 'North Dakota': ['South Dakota', 'Minnesota', 'Montana'], 'Ohio': ['Michigan', 'Pennsylvania', 'West Virginia', 'Indiana', 'Kentucky'], 'Oklahoma': ['Missouri', 'New Mexico', 'Texas', 'Arkansas', 'Colorado', 'Kansas'], 'Oregon': ['Nevada', 'Washington', 'California', 'Idaho'], 'Pennsylvania': ['New York', 'Ohio', 'West Virginia', 'Delaware', 'Maryland', 'New Jersey'], 'Rhode Island': ['Massachusetts', 'New York', 'Connecticut'], 'South Carolina': ['North Carolina', 'Georgia'], 'South Dakota': ['Nebraska', 'North Dakota', 'Wyoming', 'Iowa', 'Minnesota', 'Montana'], 'Tennessee': ['Mississippi', 'Missouri', 'North Carolina', 'Virginia', 'Alabama', 'Arkansas', 'Georgia', 'Kentucky'], 'Texas': ['New Mexico', 'Oklahoma', 'Arkansas', 'Louisiana'], 'Utah': ['Nevada', 'New Mexico', 'Wyoming', 'Arizona', 'Colorado', 'Idaho'], 'Vermont': ['New Hampshire', 'New York', 'Massachusetts'], 'Virginia': ['North Carolina', 'Tennessee', 'West Virginia', 'Kentucky', 'Maryland'], 'Washington': ['Oregon', 'Idaho'], 'West Virginia': ['Pennsylvania', 'Virginia', 'Kentucky', 'Maryland', 'Ohio'], 'Wisconsin': ['Michigan', 'Minnesota', 'Illinois', 'Iowa'], 'Wyoming': ['Nebraska', 'South Dakota', 'Utah', 'Colorado', 'Idaho', 'Montana']}


def prepareData():
    
   
    stateLevelData=pd.read_csv('https://raw.githubusercontent.com/youyanggu/covid19-datasets/main/us_states_misc_stats.csv')
    unemploymentCols=[]
    for col in stateLevelData:
        if (col.find('unemployment') != -1):
            unemploymentCols.append(col)
    stateLevelData=stateLevelData.drop(unemploymentCols,axis=1)
    stateLevelData.drop(['stringency_index'],axis=1)
   
    stringencyDct=recreateStringency()
    def getStringency(stateName):
        return stringencyDct[stateName]
    
    stateLevelData['stringency_index']=stateLevelData['State/Territory'].apply(getStringency)

    stateLevelData=stateLevelData.drop(['covid_deaths_over_flu_deaths'],axis=1)
    elec08=downloadHTML('en.wikipedia.org','/wiki/2008_United_States_presidential_election')
    mcCainShare=getElection('en.wikipedia.org','/wiki/2008_United_States_presidential_election',splitter="State/district",colIdx=6)
    def getMcCain08(stateName):
        return mcCainShare[stateName]
    stateLevelData['McCain08Share']=stateLevelData['State/Territory'].apply(getMcCain08)
    trump16Share=getElection('en.wikipedia.org','/wiki/2016_United_States_presidential_election',splitter="State or<br />district",colIdx=5)
    romneyShare=getElection('en.wikipedia.org','/wiki/2012_United_States_presidential_election',splitter="State/District",colIdx=5)
    def getRomney12(stateName):
        return romneyShare[stateName]
    stateLevelData['Romney12Share']=stateLevelData['State/Territory'].apply(getRomney12)
     
    def getTrump16(stateName):
        return trump16Share[stateName]
    stateLevelData['Trump16Share']=stateLevelData['State/Territory'].apply(getTrump16)
    stateLevelData['Trump16McCain08Shift']=stateLevelData['Trump16Share']-stateLevelData['McCain08Share']
    #stateLevelData['Trump16Romney12Shift']=stateLevelData['Trump16Share']-stateLevelData['Romney12Share']
    povDct=getPovertyRate()
    def getPovRate(stateName):
        return povDct[stateName]
    stateLevelData['poverty_rate']=stateLevelData['State/Territory'].apply(getPovRate)
    
    
    humidityDct=getHumidity()
    def lookUpHumidity(stateName):
        return humidityDct[stateName]
    stateLevelData['relative_humidity']=stateLevelData['State/Territory'].apply(lookUpHumidity)
    
    dewPointDct=getDewPoint()
    def lookUpDewPoint(stateName):
        return dewPointDct[stateName]
    #stateLevelData['dew_point']=stateLevelData['State/Territory'].apply(lookUpDewPoint)
    
    nursingResidDct=getNursingHomeResidents()
    
    def lookUpNursingHomeResidents(stateName):
        return nursingResidDct[stateName]
    stateLevelData['nursing_resid_raw']=stateLevelData['State/Territory'].apply(lookUpNursingHomeResidents)
    stateLevelData['nursing_resid_per_pop']=stateLevelData['nursing_resid_raw']/stateLevelData['population']
    stateLevelData=stateLevelData.drop(['nursing_resid_raw'],axis=1)
    
    over65Dct=getPctOver65()
    def lookUpOver65(stateName):
        return over65Dct[stateName]
    stateLevelData['over_65_pct']=stateLevelData['State/Territory'].apply(lookUpOver65)
       
    uninsuredDct=getUninsured()
    def getUninsuredPct(stateName):
        return uninsuredDct[stateName]
    stateLevelData['uninsured_pct']=stateLevelData['State/Territory'].apply(getUninsuredPct)
    
    #giniDct=getGini()
    #def lookUpGini(stateName):
    #    return giniDct[stateName]
    #stateLevelData['gini_inequality']=stateLevelData['State/Territory'].apply(lookUpGini)
    
    giniACSDict=getGiniACS()
    def lookUpGiniACS(stateName):
        return giniACSDict[stateName]
    stateLevelData['gini_inequality']=stateLevelData['State/Territory'].apply(lookUpGiniACS)
    
    regularChurchDct=getRegularChurchPct()
    def lookUpRegularChurch(stateName):
        return regularChurchDct[stateName]
    stateLevelData['regular_church_pct']=stateLevelData['State/Territory'].apply(lookUpRegularChurch)
     
    seldomChurchDct=getSeldomChurchPct()
    def lookUpSeldomChurch(stateName):
        return seldomChurchDct[stateName] 
    
    stateLevelData['seldomornever_church_pct']=stateLevelData['State/Territory'].apply(lookUpSeldomChurch)
       
    #commuteWithOthersPct=getCommuteWithOthersPct()
    #def lookUpCommuteWithOthers(stateName):
    #    return commuteWithOthersPct[stateName]
    #stateLevelData['commute_with_others_pct']=stateLevelData['State/Territory'].apply(lookUpCommuteWithOthers)
    
    carsPerCapitaDct=getCarsPerCapitaPct()
    def lookUpCarsPerCapita(stateName):
        return carsPerCapitaDct[stateName]
    stateLevelData['cars_per_capita_pct']=stateLevelData['State/Territory'].apply(lookUpCarsPerCapita)
    
    shareInAptsDct=getShareInApts()
    def lookUpShareInApts(stateName):
        return shareInAptsDct[stateName]
    stateLevelData['share_in_apts_pct']=stateLevelData['State/Territory'].apply(lookUpShareInApts)
    diabetesDct=getDiabetesPct()
    def lookUpDiabetesPct(stateName):
        return diabetesDct[stateName]
    stateLevelData['diabetes_pct']=stateLevelData['State/Territory'].apply(lookUpDiabetesPct)
    
    doctorsDct=getDoctorsPerCapita()
    def lookUpDoctorsPerCapita(stateName):
        return doctorsDct[stateName]
    stateLevelData['doctors_per_capita']=stateLevelData['State/Territory'].apply(lookUpDoctorsPerCapita)
    
    highBloodPressureDct=getHighBloodPressurePct()
    def lookUpHighBloodPressure(stateName):
        return highBloodPressureDct[stateName]
    stateLevelData['high_blood_pressure_pct']=stateLevelData['State/Territory'].apply(lookUpHighBloodPressure)
    
    hispLatinDct=getHispanicLatinoPct()
    def lookUpHispanicLatinoPct(stateName):
        return hispLatinDct[stateName]
    stateLevelData['hispanic_latino_pct']=stateLevelData['State/Territory'].apply(lookUpHispanicLatinoPct)
    
    mexAmerDct=getMexicanAmericanPct()
    def lookUpMexicanAmericanPct(stateName):
        return mexAmerDct[stateName]
    stateLevelData['mex_amer_pct']=stateLevelData['State/Territory'].apply(lookUpMexicanAmericanPct)
    
    afrAmerDct=getAfricanAmericanPct()
    def lookUpAfricanAmericanPct(stateName):
        return afrAmerDct[stateName]
    stateLevelData['afr_amer_pct']=stateLevelData['State/Territory'].apply(lookUpAfricanAmericanPct)
    
    multiGenDct=getMultiGenPct()
    def lookUpMultiGenPct(stateName):
        return multiGenDct[stateName]
    stateLevelData['multi_gen_household_pct']=stateLevelData['State/Territory'].apply(lookUpMultiGenPct)
    
    under18Dct=getPctUnder18()
    def lookUpUnder18Pct(stateName):
        return under18Dct[stateName]
    stateLevelData['under_18_pct']=stateLevelData['State/Territory'].apply(lookUpUnder18Pct)
    
    undocumentedDct=getUndocumentedPct()
    def lookUpUndocumentedPct(stateName):
        return undocumentedDct[stateName]
    stateLevelData['undocumented_pct']=stateLevelData['State/Territory'].apply(lookUpUndocumentedPct)
    
    residentsPerHouseholdDct=getResidentsPerHousehold()
    def lookUpResPerHousehold(stateName):
        return residentsPerHouseholdDct[stateName]
    stateLevelData['res_per_household']=stateLevelData['State/Territory'].apply(lookUpResPerHousehold)
    
    cigUseDct=getCigUsePct()
    def lookUpCigUse(stateName):
        return cigUseDct[stateName]
    stateLevelData['cig_use_pct']=stateLevelData['State/Territory'].apply(lookUpCigUse)
    
    urb538Dct=getUrbanization538()
    def lookUpUrb538(stateName):
        return urb538Dct[stateName]
    stateLevelData['urb_index_538']=stateLevelData['State/Territory'].apply(lookUpUrb538)
    
    excessNYTDct=getExcessFromNYT()
    def lookUpExcessNYT(stateName):
        return excessNYTDct[stateName]
    stateLevelData['excess_nyt_pct']=stateLevelData['State/Territory'].apply(lookUpExcessNYT)
    
    popInCity=getPopInCityMin200K()
   
    def lookUpPopInCityMin200K(stateName):
        return popInCity[stateName]
    stateLevelData['pct_in_city_min_200k']=stateLevelData['State/Territory'].apply(lookUpPopInCityMin200K)
    stateLevelData['pct_in_city_min_200k']=stateLevelData['pct_in_city_min_200k']/stateLevelData['population']
    #2 slightly different data sources on DC lead to a pct over 100%, so fixing that.
    stateLevelData['pct_in_city_min_200k']=numpy.where(stateLevelData['pct_in_city_min_200k'].values > 1,1.,stateLevelData['pct_in_city_min_200k'].values)
    return addCovidDeathsByDateRange(addExcess(stateLevelData))
 
    
def recreateStringency(minDateInt=20200301):
    #columns of csv:
    #CountryName,CountryCode,RegionName,RegionCode,Jurisdiction,Date,C1_School closing,C1_Flag,C2_Workplace closing,C2_Flag,C3_Cancel public events,C3_Flag,C4_Restrictions on gatherings,C4_Flag,C5_Close public transport,C5_Flag,C6_Stay at home requirements,C6_Flag,C7_Restrictions on internal movement,C7_Flag,C8_International travel controls,E1_Income support,E1_Flag,E2_Debt/contract relief,E3_Fiscal measures,E4_International support,H1_Public information campaigns,H1_Flag,H2_Testing policy,H3_Contact tracing,H4_Emergency investment in healthcare,H5_Investment in vaccines,H6_Facial Coverings,H6_Flag,H7_Vaccination policy,H7_Flag,H8_Protection of elderly people,H8_Flag,M1_Wildcard,ConfirmedCases,ConfirmedDeaths,StringencyIndex,StringencyIndexForDisplay,StringencyLegacyIndex,StringencyLegacyIndexForDisplay,GovernmentResponseIndex,GovernmentResponseIndexForDisplay,ContainmentHealthIndex,ContainmentHealthIndexForDisplay,EconomicSupportIndex,EconomicSupportIndexForDisplay
    oxf=pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')  
    #print(list(set(oxf['RegionName'].values)))
    means=oxf[oxf.Date >= minDateInt].groupby('RegionName')['StringencyIndex'].mean()
    stateDct=dict()
    for state in abbrevDict:
        if (not (state in ['Puerto Rico','New York City','United States','the District of Columbia'])):
            if (state=='District of Columbia'):
                stateDct[state]=means['Washington DC']
            else:
                stateDct[state]=means[state]
    return stateDct

    
def addCovidDeathsByDateRange(stateLevelData):
    import os
    #files downloaded from https://covid.cdc.gov/covid-data-tracker/#trends_dailytrendsdeaths
    files=os.listdir('cdcCovidDeathsCleaned')
    stateDct=dict()
    for fle in files:
        df=addDateObj(pd.read_csv('cdcCovidDeathsCleaned/' + fle))
        state=fle.split('__')[0].strip().replace('_',' ')
        capitalized=[]
        for word in state.split(' '):
            if (word != 'of'):
                capitalized.append(word[0].upper() + word[1:])
            else:
                capitalized.append(word)
        state=' '.join(capitalized)
        stateDct[state]=df
    deaths_March1_2020_dct=dict()
    for state in stateDct:
        df=stateDct[state] 
        march1_2020=datetime.date(2020,3,1)
        deaths=df[df['DateObj'] >= march1_2020]['New Deaths'].sum()
        deaths_March1_2020_dct[state]=deaths
    deaths_March1_2020_dct['New York']=deaths_March1_2020_dct['New York'] + deaths_March1_2020_dct['New York City']
    
    deaths_June1_2020_dct=dict()
    for state in stateDct:
        df=stateDct[state] 
        june1_2020=datetime.date(2020,6,1)
        deaths=df[df['DateObj'] >= june1_2020]['New Deaths'].sum()
        deaths_June1_2020_dct[state]=deaths
    deaths_June1_2020_dct['New York']=deaths_June1_2020_dct['New York'] + deaths_June1_2020_dct['New York City']
    
    deaths_Oct1_2020_dct=dict()
    for state in stateDct:
        df=stateDct[state] 
        oct1_2020=datetime.date(2020,10,1)
        deaths=df[df['DateObj'] >= oct1_2020]['New Deaths'].sum()
        deaths_Oct1_2020_dct[state]=deaths
    deaths_Oct1_2020_dct['New York']=deaths_Oct1_2020_dct['New York'] + deaths_Oct1_2020_dct['New York City']
    
    usPop=330000000
    hundK=1e5
    def lookupDeathsSinceMarch(stateName):
        return deaths_March1_2020_dct[stateName]
    stateLevelData['deaths_since_march1_2020']=stateLevelData['State/Territory'].apply(lookupDeathsSinceMarch)
    stateLevelData['deaths_since_march1_2020_per330million']=usPop*stateLevelData['deaths_since_march1_2020']/stateLevelData['population']
    stateLevelData['deaths_since_march1_2020_per100k']=hundK*stateLevelData['deaths_since_march1_2020']/stateLevelData['population']
    
    def lookupDeathsSinceJune(stateName):
        return deaths_June1_2020_dct[stateName]
    stateLevelData['deaths_since_june1_2020']=stateLevelData['State/Territory'].apply(lookupDeathsSinceJune)
    stateLevelData['deaths_since_june1_2020_per330million']=usPop*stateLevelData['deaths_since_june1_2020']/stateLevelData['population']
    
    def lookupDeathsSinceOctober(stateName):
        return deaths_Oct1_2020_dct[stateName]
    stateLevelData['deaths_since_oct1_2020']=stateLevelData['State/Territory'].apply(lookupDeathsSinceOctober)
    stateLevelData['deaths_since_oct1_2020_per330million']=usPop*stateLevelData['deaths_since_oct1_2020']/stateLevelData['population']  
    stateLevelData['deaths_since_oct1_2020_per100k']=hundK*stateLevelData['deaths_since_oct1_2020']/stateLevelData['population']
    return stateLevelData


    
def addExcess(stateLevelData):
    excessDF=pd.read_csv('C:\\Users\joe_s\\OneDrive\\Berenson\\Excess_Deaths_Associated_with_COVID-19 (3).csv')
    excessDF=excessDF[excessDF.Type=='Predicted (weighted)']
    excessDF=excessDF[excessDF.Outcome=='All causes']
    addWeekEndDateObj(excessDF)
    #print('new excess')
    #excess death data in recent months is generally premature and often continues to trickle in for many weeks, so we will exclude it
    excessDF=excessDF[excessDF['WeekEndingObj'] < datetime.date(2021,4,1)]

    def abbrev(state):
        return abbrevDict[state]

    excessDF['StateAbbrev']=excessDF['State'].apply(abbrev)
    excessDF['SimpleExcess']=excessDF['Observed Number'] -excessDF['Average Expected Count']

    excessDFAfterMarch1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,3,1)]
    excessDFAfterJune1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,6,1)]
    excessDFAfterJuly1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,7,1)]
    excessDFAfterSept1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,9,1)]
    excessDFAfterOct1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,10,1)]
    excessDFAfterNov1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,11,1)]
    excessDFAfterDec1=excessDF[excessDF['WeekEndingObj'] >= datetime.date(2020,12,1)]

    def makeExcessDicts(exDF,excessToUse):
        totalToUse='Excess %s Estimate'%excessToUse
        sumExcess=exDF.groupby('State').sum()[totalToUse]
        sumExcessDict=dict(zip(sumExcess.index,sumExcess.values))
        sumExcessDict['New York']=sumExcessDict['New York'] + sumExcessDict['New York City']
        avgExpected=exDF.groupby('State').sum()['Average Expected Count']
        avgExpectedDict=dict(zip(avgExpected.index,avgExpected.values))
        avgExpectedDict['New York']=avgExpectedDict['New York'] + avgExpectedDict['New York City']
        states=list(avgExpectedDict.keys())
        pctExcessDict=dict(zip(states,[sumExcessDict[st]/avgExpectedDict[st] for st in states]))
        return pctExcessDict
    
    excessAfterMarchHigherDct=makeExcessDicts(excessDFAfterMarch1,'Higher')
    excessAfterMarchLowerDct=makeExcessDicts(excessDFAfterMarch1,'Lower')

    excessAfterJuneHigherDct=makeExcessDicts(excessDFAfterJune1,'Higher')
    excessAfterJuneLowerDct=makeExcessDicts(excessDFAfterJune1,'Lower')

    excessAfterJulyHigherDct=makeExcessDicts(excessDFAfterJuly1,'Higher')
    excessAfterJulyLowerDct=makeExcessDicts(excessDFAfterJuly1,'Lower')

    excessAfterSeptHigherDct=makeExcessDicts(excessDFAfterSept1,'Higher')
    excessAfterSeptLowerDct=makeExcessDicts(excessDFAfterSept1,'Lower')

    excessAfterOctHigherDct=makeExcessDicts(excessDFAfterOct1,'Higher')
    excessAfterOctLowerDct=makeExcessDicts(excessDFAfterOct1,'Lower')

    excessAfterNovHigherDct=makeExcessDicts(excessDFAfterNov1,'Higher')
    excessAfterNovLowerDct=makeExcessDicts(excessDFAfterNov1,'Lower')

    excessAfterDecHigherDct=makeExcessDicts(excessDFAfterDec1,'Higher')
    excessAfterDecLowerDct=makeExcessDicts(excessDFAfterDec1,'Lower')

    def getExcessAfterMarchHigher(state):
        return excessAfterMarchHigherDct[state]

    def getExcessAfterMarchLower(state):
        return excessAfterMarchLowerDct[state]

    def getExcessAfterJuneHigher(state):
        return excessAfterJuneHigherDct[state]

    def getExcessAfterJuneLower(state):
        return excessAfterJuneLowerDct[state]

    def getExcessAfterJulyHigher(state):
        return excessAfterJulyHigherDct[state]

    def getExcessAfterJulyLower(state):
        return excessAfterJulyLowerDct[state]

    def getExcessAfterSeptHigher(state):
        return excessAfterSeptHigherDct[state]

    def getExcessAfterSeptLower(state):
        return excessAfterSeptLowerDct[state]

    def getExcessAfterOctHigher(state):
        return excessAfterOctHigherDct[state]

    def getExcessAfterOctLower(state):
        return excessAfterOctLowerDct[state]

    def getExcessAfterNovHigher(state):
        return excessAfterNovHigherDct[state]

    def getExcessAfterNovLower(state):
        return excessAfterNovLowerDct[state]

    def getExcessAfterDecHigher(state):
        return excessAfterDecHigherDct[state]

    def getExcessAfterDecLower(state):
        return excessAfterDecLowerDct[state]

    for month in ['March','June','July','Sept','Oct','Nov','Dec']:
        if (month=='March'):
            getExcessHigher=getExcessAfterMarchHigher
            getExcessLower=getExcessAfterMarchLower
        elif (month=='June'):
            getExcessHigher=getExcessAfterJuneHigher
            getExcessLower=getExcessAfterJuneLower
        elif (month=='July'):    
            getExcessHigher=getExcessAfterJulyHigher
            getExcessLower=getExcessAfterJulyLower
        elif (month=='Sept'):    
            getExcessHigher=getExcessAfterSeptHigher
            getExcessLower=getExcessAfterSeptLower
        elif (month=='Oct'):    
            getExcessHigher=getExcessAfterOctHigher
            getExcessLower=getExcessAfterOctLower 
        elif (month=='Nov'):
            getExcessHigher=getExcessAfterNovHigher
            getExcessLower=getExcessAfterNovLower
        elif (month=='Dec'):
            getExcessHigher=getExcessAfterDecHigher
            getExcessLower=getExcessAfterDecLower
        stateLevelData['pctExcessAfter%s1_2020Higher'%month]=stateLevelData['State/Territory'].apply(getExcessHigher)
        stateLevelData['pctExcessAfter%s1_2020Lower'%month]=stateLevelData['State/Territory'].apply(getExcessLower)
        
        stateLevelData['pctExcessAfter%s1_2020'%month]=0.5*(stateLevelData['pctExcessAfter%s1_2020Higher'%month] + stateLevelData['pctExcessAfter%s1_2020Lower'%month] )
    return stateLevelData


def getExcessFromNYT():
    content=downloadHTML('www.nytimes.com','/interactive/2021/01/14/us/covid-19-death-toll.html')
   
    rows=content.split('g-loading" data-state="US-table"></div>')[1].split('<div class="chart-row " data-state="')[1:]
    stateDct=dict()
    for row in rows:
        state=row.split('<p class="statename">')[1].split('<')[0].strip()
        pct=row.split('<div class="rcell excesspct">')[1].split('<p>')[1].split('<')[0].strip()
        if (state=='Washington, D.C.'):
            state='District of Columbia'
        if (state=='Washington State'):
            state='Washington'
        stateDct[state]=float(pct.replace('%','').strip())
    stateDct['New York']=0.56*stateDct['New York (excluding N.Y.C.)'] + 0.44*stateDct['New York City']
    return stateDct
   
def getNursingHomeResidents():
    #https://www.kff.org/other/state-indicator/number-of-nursing-facility-residents/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D
    df=pd.read_csv('nursingHomeResidents2019.csv')
    return dict(zip(df['Location'].values,df['Number of Nursing Facility Residents'].values))

 
def getGiniACS():
    #source: https://www.census.gov/content/dam/Census/library/publications/2020/acs/acsbr20-03.pdf
    df=pd.read_csv('giniACS2019.txt',delimiter=' ')
    return dict(zip([v.replace('.','').strip().replace('_',' ') for v in df['State'].values],df['gini19'].values))

    
            
def getUrbanization538():
#https://fivethirtyeight.com/features/how-urban-or-rural-is-your-state-and-what-does-that-mean-for-the-2020-election/
    df=pd.read_csv('Urbanization538.csv')
    dct=dict(zip(df.STATE.values,df['URBANIZATION INDEX'].values))
    #eductated guess for DC, DC unavailable
    dct['District of Columbia']=13
    return dct
    
    
def getResidentsPerHousehold():
#https://www.indexmundi.com/facts/united-states/quick-facts/all-states/average-household-size#table
    df=pd.read_csv('resPerHousehold.csv')
    return dict(zip(df.State.values,df.Value.values))
    
    
def getUndocumentedPct():
    #source: https://www.pewresearch.org/hispanic/interactives/u-s-unauthorized-immigrants-by-state/
    df=pd.read_csv('UndocumentedPct.csv')
    pcts=[float(v.strip().replace('%','')) for v in df['Unauthorized immigrant % of population'].values]
    return dict(zip(df['State'],pcts))

def getCigUsePct():
    #https://www.cdc.gov/statesystem/cigaretteuseadult.html
    df=pd.read_csv('cigUseCDC.csv')
    return dict(zip(df['Location'].values,df['Data_Value'].values))
                
    
def getPctOver65():
    content=downloadHTML('www.prb.org','/resources/which-us-states-are-the-oldest/')
    content=content.split('Total Resident Population (thousands)')[1].split('</table ')[0].strip()
    rows=content.split('<tr>')[1:]
    stateDct=dict()
    for row in rows:
        state=row.split('<td>')[2].split('<')[0].strip()
        pct=float(row.split('<td>')[5].split('<')[0].strip())
        stateDct[state]=pct
    stateDct['District of Columbia']=12.1
    return stateDct

def getPctUnder18():
    df=pd.read_csv('pctUnder18.csv')
    return dict(zip(df['State'].values,df['Value'].values))


def getPctForeignBorn():
#sources:
#https://www.statista.com/statistics/312701/percentage-of-population-foreign-born-in-the-us-by-state/
    return { 'California': 26.8,
            'New Jersey': 23.4,
        'New York': 22.4,
        'Florida': 21.1,
        'Nevada': 19.8,
        'Hawaii': 19.3,
        'Massachusetts': 17.3,
        'Texas': 17.1,
        'Maryland': 15.4,
        'Washington': 14.9,
        'Connecticut': 14.8,
        'Illinois': 13.9,
        'Rhode Island': 13.7,
        'Arizona': 13.4,
        'Virginia': 12.7,
        'District of Columbia': 12.1,
        'Georgia': 10.3,
        'Delaware': 10,
        'Oregon': 9.7,
        'New Mexico': 9.6,
        'Colorado': 9.5,
        'Utah': 8.6,
        'North Carolina': 8.4,
         'Minnesota': 8.4,
        'Alaska': 8,
        'Nebraska': 7.4,
        'Kansas': 7.2,
        'Pennsylvania': 7,
        'Michigan': 7,
        'New Hampshire': 6.4,
        'Oklahoma': 6.1,
        'Idaho': 5.8,
        'Iowa': 5.6,
        'South Carolina': 5.6,
        'Tennessee': 5.5,
        'Indiana': 5.3,
        'Arkansas': 5.1,
        'Wisconsin': 5.1,
        'Ohio': 4.8,
        'Vermont': 4.7,
        'Kentucky': 4.4,
        'Missouri': 4.3,
        'Louisiana': 4.2,
        'North Dakota': 4.1,
        'South Dakota': 4.1,
        'Maine': 3.9,
        'Alabama': 3.6,
         'Wyoming': 3.1,
        'Montana': 2.3,
        'Mississippi': 2.1,
        'West Virginia':1.6 }
    
def getDoctorsPerCapita():
#sources:
#https://www.beckershospitalreview.com/workforce/50-states-ranked-by-most-active-physicians-per-100-000-population.html
#https://www.aamc.org/media/37876/download (for DC..note...possibly different methodology for DC, given different source

    return { 'Massachusetts': 449.5,
            'Maryland': 386,
        'New York': 375.1,
        'Rhode Island': 370,
        'Vermont': 367.1,
        'Connecticut': 352.1,
        'Maine': 330.2,
        'Pennsylvania': 320.5,
        'New Hampshire': 315.1,
        'Hawaii': 314.1,
        'New Jersey': 306.5,
        'Oregon': 303.4,
        'Minnesota': 302.7,
        'Ohio': 292.7,
        'Michigan': 287,
        'Colorado': 285.7,
        'Delaware': 284.6,
        'Illinois': 284.4,
        'California': 279.6,
        'Washington': 278.8,
        'Alaska': 276.9,
        'Missouri': 273.1,
        'Florida': 265.2,
         'Wisconsin': 264.9,
        'West Virginia': 263.4,
        'Virginia': 263.2,
        'Louisiana': 260.3,
        'North Carolina': 255,
        'Tennessee': 253.1,
        'Montana': 247.1,
        'New Mexico': 244.8,
        'Arizona': 242,
        'South Dakota': 240.4,
        'Nebraska': 239.2,
        'North Dakota': 237.6,
        'Kentucky': 230.9,
        'Indiana': 230.8,
        'South Carolina': 229.5,
        'Georgia': 228.7,
        'Kansas': 227.6,
        'Texas': 224.8,
        'Iowa': 218.2,
        'Alabama': 217.1,
        'Utah': 216.2,
        'Nevada': 213.5,
        'Wyoming': 207.9,
        'Arkansas': 207.6,
         'Oklahoma': 206.7,
        'Idaho': 192.6,
        'Mississippi': 191.3,
        'District of Columbia':847 }
            
def getDiabetesPct():
    #source:https://nccd.cdc.gov/Toolkit/DiabetesBurden/Prevalence
    import os
    fles=os.listdir('cdcDiabetes')
    stateDct=dict()
    for fle in fles:
        if (fle.find('.csv') != -1):
            inF=open('cdcDiabetes/%s'%fle,'r')
            line=inF.readline()
            state=line.split('Older, ')[1].split(',')[0].strip()
            line=inF.readline()
            line=inF.readline()
            #print(line)
            splts=line.split(',')
            rate=float(splts[1])
            stateDct[state]=rate
            inF.close()
    return stateDct

def getHighBloodPressurePct():   
#source: https://www.americashealthrankings.org/explore/annual/measure/Hypertension/state/ALL    
    df=pd.read_csv('highBloodPressure.csv')
    stringDct=dict(zip(df.STATE.values,df.VALUE.values))
    stringDct['New Jersey']=stringDct['New Jersey[27]']
    floatDct=dict()
    for state in stringDct:
        #print(state)
        stateFilt=state.replace('[27]','').strip()
        #print(stateFilt)
        floatDct[stateFilt]=float(stringDct[stateFilt].replace('%',''))
    return floatDct
                              
def getCommuteWithOthersPct():
    #source: https://www.bts.gov/browse-statistical-products-and-data/state-transportation-statistics/commute-mode
    carpoolPct=getCarpoolPct()
    publicTransPct=getPublicTransPct()
    stateDct=dict()
    for state in carpoolPct:
        stateDct[state]=carpoolPct[state] + publicTransPct[state]
    return stateDct


def getPopInCityMin200K():
    df=pd.read_csv('TopCitiesByPop.csv')
    summed=df.groupby('State')['Pop'].sum()
    dct=dict(zip([s.strip() for s in summed.index],summed.values))
    stateDct=dict()
    for state in abbrevDict:
        stateDct[state.strip()]=dct.get(state.strip(),0)
    return stateDct
    
def getMultiGenPct():
    #https://data.census.gov/cedsci/table?q=multigenerational&g=0100000US.04000.001&tid=ACSDT1Y2010.B11017&vintage=2010&hidePreview=true
    df=pd.read_csv('multiGen_census.csv')
    df['pct']=df['Estimate!!Total:!!Multigenerational households']/df['Estimate!!Total:']
    return dict(zip(df['Geographic Area Name'].values,df['pct'].values))

def getHispanicLatinoPct():
    content=downloadHTML('en.wikipedia.org','/wiki/List_of_U.S._states_by_Hispanic_and_Latino_population')
    content=content.split('pop 2017')[1].split('</table')[0].strip()
    rows=content.split('<tr>')[1:]
    stateDct=dict()
    for row in rows[0:51]:
        state=row.split('<th>')[1].split('</a')[-2].split('>')[-1].split('<')[0].strip()
        pct=float(row.split('<td')[10].split('<')[0].split('>')[1].replace('%','').replace('\\n','').strip())
        stateDct[state]=pct
    
    return stateDct

def getMexicanAmericanPct():
    content=downloadHTML('en.wikipedia.org','/wiki/List_of_U.S._states_by_Hispanic_and_Latino_population')
    content=content.split('Edit section: U.S. states by Mexican American')[1].split('</table')[0].strip()
    rows=content.split('<tr>')[1:]
    stateDct=dict()
    for row in rows[1:53]:
        state=row.split('title="')[1].split('>')[1].split('<')[0].strip()
        pct=float(row.split('<td ')[2].split('>')[1].split('<')[0].replace('\\n','').strip())
        stateDct[state]=pct
    stateDct['Georgia']=5.5
    return stateDct

def getAfricanAmericanPct():    
    content=downloadHTML('en.wikipedia.org','/wiki/List_of_U.S._states_and_territories_by_African-American_population')
    content=content.split('<th>African-American<br />Population  (2019)')[1]
    rows=content.split('<tr>')[2:]
    stateDct=dict()
    for row in rows[0:53]:
        if (row.find('America') != -1):
            continue
        state=row.split('<td')[3].split('title="')[-1].split('>')[1].split('<')[0].strip()
        pct=float(row.split('<td')[1].split('>')[1].split('<')[0].replace('%','').replace('\\n',''))
        stateDct[state]=pct
    return stateDct


def getCarsPerCapitaPct():
    content=downloadHTML('en.wikipedia.org','/wiki/List_of_U.S._states_by_vehicles_per_capita')
    content=content.split('id="2017_Rankings">2017 Rankings</span>')[1]
    content=content.split('<table class="wikitable sortable mw-collapsible">')[1].split('</table>')[0]
    rows=content.split('<tr>')[1:]
    stateDct=dict()
    for row in rows:
        if (row.find('<th>') != -1):
            continue
        state=row.split('<td>')[2].split('>')[1].split('</a')[0].strip()
        val=float(row.split('<td>')[3].split('</td>')[0].replace('\\n','').replace(',',''))
        stateDct[state]=val
    return stateDct
    
def getRegularChurchPct():
    #source:https://www.pewforum.org/religious-landscape-study/compare/attendance-at-religious-services/by/state/
    df=pd.read_csv('churchPct.csv')
    states=df['State'].values
    stateDct=dict()
    for state in states:
        stateDct[state]=float(df[df.State==state]['OncePerWeek'].values[0].replace('%',''))
    return stateDct


def getIntermittentChurchPct():
    #source:https://www.pewforum.org/religious-landscape-study/compare/attendance-at-religious-services/by/state/
    df=pd.read_csv('churchPct.csv')
    states=df['State'].values
    stateDct=dict()
    for state in states:
        stateDct[state]=float(df[df.State==state]['AFewTimesPerYear'].values[0].replace('%',''))
    return stateDct

def getSeldomChurchPct():
    #source:https://www.pewforum.org/religious-landscape-study/compare/attendance-at-religious-services/by/state/
    df=pd.read_csv('churchPct.csv')
    states=df['State'].values
    stateDct=dict()
    for state in states:
        #print(state)
        #if (str(state)
        stateDct[state]=float(df[df.State==state]['SeldomOrNever'].values[0].replace('%',''))
    return stateDct
    
def getShareInApts():
    #https://www.nmhc.org/research-insight/quick-facts-figures/quick-facts-resident-demographics/geography-of-apartment-residents/
    
    df=pd.read_csv('state-distribution-of-apartment-residents.csv')
    states=df['State'].values
    stateDct=dict()
    for state in states[0:50]:
        stateDct[state]=float(df[df.State==state]['Apartment Resident Share of State Population'].values[0].replace('%',''))
    stateDct['District of Columbia']=19#double check, this is for greater DC region?
    return stateDct

        


def getPublicTransPct():
    #source: https://www.bts.gov/browse-statistical-products-and-data/state-transportation-statistics/commute-mode
    df=pd.read_csv('CommuteData.csv')
    df=df[df.Year==2019]
    stateDct=dict()
    for state in abbrevDict:
        if (state in ['New York City','the District of Columbia']):
            continue
        stateDct[state]=df[lambda dFrame: numpy.logical_and(dFrame.State==state,dFrame.Mode=='Public transportation')]['Commute mode share (percent)'].values[0]
    return stateDct

def getCarpoolPct():
    #source: https://www.bts.gov/browse-statistical-products-and-data/state-transportation-statistics/commute-mode
    df=pd.read_csv('CommuteData.csv')
    df=df[df.Year==2019]
    stateDct=dict()
    for state in abbrevDict:
        if (state in ['New York City','the District of Columbia']):
            continue
        stateDct[state]=df[lambda dFrame: numpy.logical_and(dFrame.State==state,dFrame.Mode=='Carpool')]['Commute mode share (percent)'].values[0]
    return stateDct
                                 
def removeFirstTwoLines():
    import os
    files=os.listdir('cdcCovidDeaths')
    for fle in files:
        state=fle.split('__')[1].split(' ')[0].strip()
        inF=open('cdcCovidDeaths/' + fle,'r')
        line=inF.readline()
        line=inF.readline()
        outF=open('cdcCovidDeathsCleaned/%s__deaths.csv'%state,'w')
        line=inF.readline()
        
        while (line != ''):
            outF.writelines(line.strip() + '\n')
            line=inF.readline()
        outF.close()
    
def dateStrToDate(dStr):
    monthMap={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    splts=dStr.strip().split(' ')
    year=int(splts[2].strip())
    day=int(splts[1].strip())
    month=monthMap[splts[0].strip()]
    return datetime.date(year,month,day)
                   
def addDateObj(cdcDF):
    cdcDF['DateObj']=cdcDF['Date'].apply(dateStrToDate)
    return cdcDF

def dateStrExcessToDate(dStr):
    splts=dStr.strip().split('-')
    return datetime.date(int(splts[0]),int(splts[1]),int(splts[2]))

def addWeekEndDateObj(exDF):
    exDF['WeekEndingObj']=exDF['Week Ending Date'].apply(dateStrExcessToDate)
                   
    
  