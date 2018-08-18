import calendar
import collections
import datetime
import os
import smtplib
import statistics
import time
import sys
import builtins
from colour import Color
import bs4
# My modules
import unittest
import CSSAssist
import ColorAssist
import EmailAssist
import MathAssist
import SeleniumAssist
import WeatherScrape
#bs4 and selenium modules
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
#Account info file
import AccountInfo

#   List of urls            ############################################
urlHomePage = "https://account.justenergy.com/Home"
urlAccountsPage = "https://account.justenergy.com/MyAccount"
urlAccountDetailsPage = urlAccountsPage + "/AccountDetails/"
urlUsagePage = "https://account.justenergy.com/UsageHistory/Index"
#   Base Class              ############################################


class SetUp(object):
    '''
    __init__:       Initialies driver and sets WebDriverWait object with
                    Wait time parameter
    _Login:         Logs into the user's profile and selects a
                    particular account
    _LogOut:        Logs out of the account and prints a messages
                    confirming whether or not the action was sucessful
    _TearDown:      Closes the driver
    '''

    def __init__(self):
        # Description: Sets up web driver and its corresponding
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1920x1080")
        self.options.add_argument("--incognito")
        self.chrome_driver = os.getcwd() + "\\chromedriver.exe"
        self.driver = webdriver.Chrome(
                                options=self.options,
                                executable_path=self.chrome_driver
                                )
        self.WaitTime = 15
        self.MaxWaitTime = 30
        self.Wait = WebDriverWait(driver=self.driver, timeout=self.WaitTime)

    def _Login(self):
        '''
        Description: This method navigates to the login page and
                      logs in the user
                        form
        :return: None
        '''
        self.driver.get(url=urlHomePage)
        if(not(SeleniumAssist.WaitForPage(
            wait_obj=self.Wait,
            pageurl=urlHomePage,
            max_wait=self.MaxWaitTime
        ))): return False
        frmLogin = \
            self.driver.find_element_by_css_selector("[name=myForm]")
        txtUsername = \
            frmLogin.find_element_by_xpath('(//*[@id="username"])[2]')
        txtPassword = frmLogin.find_element_by_id("password")
        txtUsername.clear()
        txtPassword.clear()
        txtUsername.send_keys(AccountInfo.USERNAME)
        txtPassword.send_keys(AccountInfo.PASSWORD)
        btnProfileSubmit_button =     \
            frmLogin.find_element_by_xpath('//*[@id="btnLogin"]')
        btnProfileSubmit_button.click()

        if(not(SeleniumAssist.WaitForPage(
            wait_obj=self.Wait,
            pageurl=urlAccountsPage,
            max_wait=self.MaxWaitTime
        ))): return False

        print("Login successful")
        return True

    def SelectAccount(self):
        '''
        :return: bool, true is account was selected correctly, false otherwise
        '''
        if(not(SeleniumAssist.IsElementVisible(
            wait_obj=self.Wait,
            locator=(By.XPATH, '// *[ @ id = "demo"] / div[1] / div[1]'),
            max_wait=self.MaxWaitTime
        ))): return False
        accounts = self.driver.find_elements_by_class_name("account-list-item")
        if len(accounts) == 0:
            print("Accounts are not visible ")
            return False
        print("ACCOUNTS")
        for idx, acc in zip(range(1,len(accounts)+1),accounts):
            print (idx, " ) ",acc.text)

        account_selected =(input(
            "Choose account from the accounts listed below by entered its number: "))
        try:
            account_selected = int(account_selected)
        except ValueError:
            print("You did not enter a correct value.")
            return False

        if(int(account_selected) not in range(1,len(accounts)+1)):
            print("One of the accounts listed was not selected.")
            return False
        else:
            AccountWrapper = \
                self.driver.find_element_by_xpath(
                    '//*[@id="demo"]/div[' + str(account_selected) + ']'
                )
            btnSubmit = AccountWrapper.find_element_by_tag_name('a')
            self.driver.execute_script("$(arguments[0]).click();", btnSubmit)

        if (not (SeleniumAssist.WaitForPage(
            wait_obj=self.Wait,
            pageurl=urlAccountDetailsPage,
            max_wait=self.MaxWaitTime
        ))): return False

        return True

    def _LogOut(self):
        '''
        :return: bool, True if log out was successful, False otherwise
        '''

        if self.driver.current_url == urlHomePage:
            print("You are already logged out.")
            return True
        elif self.driver.current_url == urlAccountsPage:
            if(not(SeleniumAssist.IsElementVisible(
                wait_obj = self.Wait,
                element_class_name = 'account-head.account-info',
                max_wait = self.MaxWaitTime
            ))): return False
            AccountInfoWrapper = self.driver.find_element_by_class_name(
                "account-head.account-info'"
            )
            btnLogOut = AccountInfoWrapper.find_element_by_xpath(
                "//a[text()='LogOut']"
            )
            btnLogOut.click()
        else:
            if (not (SeleniumAssist.IsElementVisible(
                    wait_obj=self.Wait,
                    locator=(By.CLASS_NAME,'navbar-heading'),
                    max_wait=self.MaxWaitTime
            ))): return False
            NavigationHeading = self.driver.find_element_by_class_name(
                "navbar-heading"
            )
            btnLogOut = NavigationHeading.find_element_by_xpath(
                "//a[text()='Logout']"
            )
            btnLogOut.click()

        if (not (SeleniumAssist.WaitForPage(
                wait_obj=self.Wait,
                pageurl=urlHomePage,
                max_wait=self.MaxWaitTime
        ))): return False

        print("Log out successful")
        return True

    def _TearDown(self):
        '''
        Description: closes driver
        :return: None
        '''
        print("closing driver")
        self.driver.quit()
        

class UsagePage(SetUp):
    '''
    Description/purpose:        ....
    Attributes:
        __init__:               Inherits the base class's constructor
        _Login:                 ...
        SetDatet:               ...
        GetData:                ...
        _LogOut:                Inherits the base class's Logout method
        _TearDown:               Inherits the base class's constructor
    '''

    def __init__(self):
        super(UsagePage, self).__init__()

    def _Login(self):
        return super(UsagePage, self)._Login()

    def SelectAccount(self):
        return super(UsagePage, self).SelectAccount()

    def openUsagePage(self):
        self.driver.get(urlUsagePage)
        if(not(SeleniumAssist.WaitForPage(
                wait_obj=self.Wait,
                pageurl=urlUsagePage,
                max_wait=self.MaxWaitTime
        ))):    return False
        if (not (SeleniumAssist.IsElementVisible(
                wait_obj=self.Wait,
                locator=(By.CLASS_NAME, 'highcharts-container'),
                max_wait=self.MaxWaitTime
        ))): return False

        btnHourly = \
            self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Hourly Usage')]"
            )
        self.driver.execute_script("$(arguments[0]).click();", btnHourly)

        if (not (SeleniumAssist.IsElementVisible(
                wait_obj=self.Wait,
                locator=(By.CLASS_NAME,'highcharts-container'),
                max_wait=self.MaxWaitTime
        ))): return False

        return True

    def SetDate(self, requested_date):
        '''
        Description:   ...
        :param requested_date:
                        type: datetime,
                        Description: this is the requested date to set
                                      for the Calendardatepicker date
                                      value
        :return:
                        type: bool
                        Description: if True setting the requested date
                                      was successful and False otherwise
        '''
        if (not (SeleniumAssist.WaitForPage(
                wait_obj=self.Wait,
                pageurl=urlUsagePage,
                max_wait=self.MaxWaitTime
        ))):
            print("failed to open usage page")
            return False
        if(not(SeleniumAssist.IsElementVisible(
            wait_obj=self.Wait,
            locator=(By.XPATH,'//*[@id="UsageChartStartDate"]/span/i'),
            max_wait=self.MaxWaitTime
        ))):
            print("failed to select calandar date picker icon")
            return False

        self.driver.get_screenshot_as_file("settingDate.png")

        btnCalendar = self.driver.find_element_by_xpath(
                            '//*[@id="UsageChartStartDate"]/span/i'
                          )
        self.driver.execute_script("$(arguments[0]).click();",
                                   btnCalendar)

        if (not (SeleniumAssist.IsElementVisible(
                wait_obj=self.Wait,
                locator=(
                        By.CSS_SELECTOR,
                        'body > div.datepicker.datepicker-dropdown.dropdown-menu'),
                max_wait=self.MaxWaitTime
        ))):
            print("Failed to select datepicker")
            return false

        btnDatePickerSwitch = \
            self.driver.find_element_by_class_name("datepicker-switch")
        CurrentMonth = \
            (btnDatePickerSwitch.text)[:(btnDatePickerSwitch.text).find(' ')]
        RequestedMonth = \
            calendar.month_name[requested_date.month]

        if(CurrentMonth != RequestedMonth):
            self.driver.execute_script(
                "$(arguments[0]).click();", btnDatePickerSwitch
            )
            dtpMonthCalendar = self.driver.find_element_by_css_selector(
                'body > div.datepicker.datepicker-dropdown.dropdown-menu'
            )
            TargetMonth = dtpMonthCalendar.find_elements_by_tag_name("span")[requested_date.month-1]
            TargetMonth.click()

        dtpMonthCalendar = self.driver.find_element_by_css_selector(
                            'body > div.datepicker.datepicker-dropdown.dropdown-menu'
                        )
        TargetDate = dtpMonthCalendar.find_element_by_xpath(
                            "//td[text()='" + str(requested_date.day) +
                            "'][@class='day']"
                        )
        TargetDate.click()
        btnApply = self.driver.find_element_by_name("Apply")
        btnApply.click()
        time.sleep(15)
        ChartSubTitle = self.driver.find_element_by_class_name("highcharts-subtitle")
        ChartDate = ChartSubTitle.find_element_by_css_selector("tspan:nth-child(2)").text
        return(True if str(ChartDate) == requested_date.strftime("%m/%d/%Y") else False)

    def GetData(self, date):
        '''
        Description:    ...
        :param date:
            type:           datetime
            description:    requested date
        :return:
            type:           dictionary
            description:    keys are the hours and their value is the
                            kWh usage
        '''

        if(not(UsagePage.SetDate(self, date))):
            print("Date couldn't be set")
            return

        '''
          [A] GET DIFFERENCE BETWEEN EACH GRIDLINE
          [B] GET EACH CHART BAR'S HEIGHT
          [C] GET THE X-AXIS VALUES
          [D] COMPILE DATA 
        '''
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        SVG = soup.find('svg')
        ################################################################
        #[A] GET THE HEIGHT DIFFERENCE BETWEEN EACH GRID LINE)
        Heights = []
        gElements = SVG.find_all('g')
        for path in gElements[2]:
            Height = path['d'][1:((path['d'])).find('L')]
            if (not(Height == "" or Height is None)):
                Height = list(filter(None, Height.split(" ")))
                Heights.append(float(str(Height[1])))
        Heights = sorted(list(set(Heights)))
        DeltaHeight = \
            [round(j, 0)-round(i, 0) for i, j in zip(Heights[:-1], Heights[1:])]
        DeltaHeight = round((statistics.mean(DeltaHeight)), 0)
        ################################################################
        #[B]    -   GET EACH CHART BAR'S HEIGHT
        ChartBars = (SVG.find_all('g')[6])
        kWhData = []
        for bar in ChartBars:
            kWhData.append(round(((float(bar['height']))/DeltaHeight), 1))
        ################################################################
        # [C]    -   GET THE X-AXIS VALUES
        X_Axis_Elements = SVG.find_all("g", {"class": "highcharts-axis-labels highcharts-xaxis-labels"})
        X_Axis = []
        [X_Axis.append(x.text) for x in X_Axis_Elements[0]]
        print(len(X_Axis),X_Axis)
        temp = []*((len(X_Axis))*2)
        for index, interval in zip(range(len(X_Axis)), X_Axis):
            start_index = (X_Axis[index]).find("-")
            if ((index+1 >= len(X_Axis)) and (len(kWhData) > len(X_Axis))):
                filler = (X_Axis[index][start_index+1:-2]) \
                         + "-" + str((int(X_Axis[index][start_index+1:-2])+1)) + \
                         (X_Axis[index][-2:])
                temp.append(interval)
                temp.append(filler)
            else:
                end_index =(X_Axis[index+1]).find("-")
                temp.append(interval)
                filler = (X_Axis[index][start_index + 1:-2]) + "-" \
                         + (X_Axis[index + 1][:end_index]) \
                         + (X_Axis[index][-2:])
                temp.append(filler)
        X_Axis = temp
        ################################################################
        #[E]    -   Compile chart data
        ChartData = {}
        for (x, y) in zip(X_Axis, kWhData):
            ChartData[x] = y
        # or return dict([(x,y) for (x,y) in zip(X_Axis, kWhData)])

        return ChartData

    def EmailData(self,data):
        '''
        Legend
            High Usage -> Red
            Low Usage  -> Bue
            High Temp  -> Yellow
            Low Temp   -> Red

           Usage  Temperature       Color
            High	High   -> 	  Orange (neutral)
            High	Low	   ->     Red (Over usage)
            Low	    High   ->     Green (Under usage)
            Low	    Low	   ->     Purple (neutral)
        '''
        ################################################################
        #Create Email Object
        TO = "franktallerine@gmail.com"
        SUBJECT = "Electrical Usage Update"
        TEXT = "Below is information on your usage during the period ."
        Emailer = EmailAssist.HTMLEmailer(TO)
        Emailer.SetUp()
        HTML = ""
        ################################################################
        # Generate color lists and html legends
        UsageSpectrum = ColorAssist.GenerateColorList("Blue", "Red", 10)
        TempSpectrum = ColorAssist.GenerateColorList("Red", "Yellow", 10)
        htmlUsageSpectrum = self.htmlLegend(UsageSpectrum)
        htmlTempSpectrum = self.htmlLegend(TempSpectrum)
        ################################################################
        #Generate data table html
        hours = list(data[next(iter(data))].keys())
        htmlTables = self.htmlTableTemplate(hours, data, TempSpectrum, UsageSpectrum)
        HTML = htmlTempSpectrum + htmlUsageSpectrum + htmlTables
        Emailer.SendMessage(SUBJECT,TEXT,HTML)

    def htmlLegend(self, Spectrum):
        html = ""
        html += "<table><tbody><tr><td> Low kWh Usage </td>" \
                            + ("<td></td>") * 8 \
                            + "<td> High kWh Usage </td></tr><tr>"
        html += ''.join(
            [("<td bgcolor=" + str(item) + "></td>") for item in
             Spectrum]
        )
        html  += "</tr></tbody></table>"
        return html

    def htmlTables(self, hours, data, TempSpectrum, UsageSpectrum):
        tables = {'Usage': "", 'Temp': "", 'UsageTemp': ""}
        # Get temperature and usage data
        TempDict = self.get_Temperature_Data(data)
        UsageDict = self.get_Usage_Data(data)
        hourlyUsage = dict((hour, []) for hour in hours)
        hourlyTemp = dict((hour, []) for hour in hours)
        formatter = '%Y-%#m-%#d'
        htmlTop = ""

        htmlTop += "<table><tr><th>Hour</th>"
        for hour in hours:
            formattedHour = self.get_DayTimeHour(hour)
            htmlTop += "<th>"+str(hour)+"</th>"
        htmlTop += "<th>Average</th></tr><tbody>"
        for table in tables:  tables[table] += htmlTop

        for date in data:
            formattedDate = date.strftime(formatter)
            for table in tables:  tables[table] \
                += "<tr><td>"+str(formattedDate)+"</td>"

            for hour in hours:
                formattedHour = self.get_DayTimeHour(hour)
                NormilzedTempNum = int(
                    MathAssist.NormalizeNumber(
                        float(TempDict[date]['Temperatures'][formattedHour]),
                        float(TempDict[date]['min']),
                        float(TempDict[date]['max'])
                    ))
                NormilzedUsageNum = int(
                    MathAssist.NormalizeNumber(
                        (data[date][hour]),
                        UsageDict[date]['min'],
                        UsageDict[date]['max'],
                        range(0, 10)
                    ))

                normTempColor = TempSpectrum[NormilzedTempNum]
                normUsageColor = UsageSpectrum[NormilzedUsageNum]
                MixedColor = ColorAssist.HalfWayColor(normTempColor,
                                                      normUsageColor)

                tables['UsageTemp'] += (
                    '<td align="center" bgcolor=" {} "> {} </td>').\
                    format(MixedColor,data[date][hour])
                tables['Temp'] += (
                    '<td align="center" bgcolor=" {} "> {} </td>'). \
                    format(normTempColor, TempDict[date]['Temperatures'][formattedHour])
                tables['Usage'] += (
                    '<td align="center" bgcolor=" {} "> {} </td>').\
                    format(normUsageColor, data[date][hour])

                hourlyTemp[hour].append(float(
                    TempDict[date]['Temperatures'][formattedHour]))
                hourlyUsage[hour].append(float(data[date][hour]))

            AverageUsage = round(statistics.mean(data[date].values()),2)
            temps = TempDict[date]['Temperatures'].values()
            temps = [float(temp) for temp in temps]
            AverageTemp = round(statistics.mean(temps),2)

            tables['UsageTemp'] += '<td align="center" > {} </td></tr>'.format(AverageUsage)
            tables['Temp'] += '<td align="center" > {} </td></tr>'.format(AverageTemp)
            tables['Usage'] += '<td align="center" > {} </td></tr>'.format(AverageUsage)

        for table in tables:  tables[table]  += "<tr><td>Average</td>"

        for hour in hours: 
            tables['UsageTemp'] += \
                ("<td>{}</td>").format(statistics.mean(hourlyUsage[hour]))
            tables['Temp'] += \
                ("<td>{}</td>").format(statistics.mean(hourlyTemp[hour]) )
            tables['Usage'] += \
                ("<td>{}</td>").format(statistics.mean((hourlyUsage[hour])))

        for table in tables:  tables[table] += "</tbody></table>"

        html = "".join(tables.values())
        return html

    def get_DayTimeHour(self,hour):
        DateTimehour = hour[:hour.index("-")]
        if (hour[-2:] == "PM"):
            if hour[:2] == str(12):
                DateTimehour = datetime.time(hour=(12))
            else:
                DateTimehour = datetime.time(hour=(int(DateTimehour) + 12))
        else:
            if hour[:2] == str(12):
                DateTimehour = datetime.time(hour=(0))
            else:
                DateTimehour = datetime.time(hour=int(DateTimehour))
        return DateTimehour

    def get_Temperature_Data(self, data):
        formatter = '%Y-%#m-%#d'
        WeatherScraper = WeatherScrape.SetUp(self.driver)
        data_metrics = {}
        for day in data:
            formattedDate = day.strftime(formatter)
            DaysData = WeatherScraper.getHistoricalDateData(formattedDate)
            data_metrics[day] = {}
            data_metrics[day]['Temperatures'] = \
                {hour:DaysData[hour]['Temperature'] for hour in DaysData}
            data_metrics[day]['min'] = min((data_metrics[day]['Temperatures']).values())
            data_metrics[day]['max'] = max((data_metrics[day]['Temperatures']).values())
        return data_metrics

    def get_Usage_Data(self, data):
        kWhs = {day:{} for day in data}
        for day in data:
            kWhs[day] = {}
            kWhs[day]['min'] = min(data[day].values())
            kWhs[day]['max'] = max(data[day].values())
        print(kWhs)
        return kWhs

    def _LogOut(self):
        super(UsagePage, self)._LogOut()

    def _TearDown(self):
        super(UsagePage, self)._TearDown()

if __name__ == '__main__':
    #Create date variable
    start_date = datetime.date(2018, 7, 23)
    end_date = datetime.date(2018, 7, 25)

    delta_days = end_date - start_date
    dates = []
    for date in range(delta_days.days+1):
        dates.append(start_date+datetime.timedelta(date))

    #Test 2
    test2 = UsagePage()
    test2._Login()
    builtins.input = lambda _: str(2)
    test2.SelectAccount()
    test2.openUsagePage()
    data  = collections.OrderedDict()
    for date in dates:
        data[date] = test2.GetData(date=date)
    print(data)
    test2.EmailData(data)
    test2._LogOut()
    test2._TearDown()