from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
from BeautifulSoup import BeautifulSoup
import urllib2
import re

COUNTRY_OPTION = "United Kingdom"
COURSE_OPTION = "MBA"


# returns the id name of a HTML element with id ending with endStringOfControlId
def get_xpath_string_for_element_ends_with(element, end_string):
    return("//*[substring(@\"" + element + "\", string-length(@\"" +
           element + "\")- string-length(\"" + end_string + "\") + 1 )=\"" + end_string + "\"]")


# selects and option from a list
def click_option_from_list(list_name, option_name):
    for option in list_name.find_elements_by_tag_name('option'):
        if option.text == option_name:
            option.click()  # select() in earlier versions of webdriver
            return True
    return False


# LOAD INDEX ------------------------------------------------------------------
def load_index():
    global driver

    # replace with your firefox profile
    fp = webdriver.FirefoxProfile('/Users/wmaterka/Library/Application Support/Firefox/Profiles/7xp1ls6v.blu')
    # enter your url here

    # Initialise webdriver and open the login page TEST URL
    url = "https://iconnect.insead.edu/Search/Pages/Default.aspx"

    print("opening Firefox as %s and accessing %s" % (fp.path, url))
    driver = webdriver.Firefox(fp)
    driver.get(url)

    html_source = driver.page_source

    # write the 1st index file
    print("saving the index file")
    output_file = open('./HTML/output/index.html', 'w+')
    output_file.write(html_source.encode("utf-8"))


# PERFORM 1st SEARCH ------------------------------------------------------------------
def search_for_alumni():
    # looking for country of residence
    print("locating the Country Residence option")
    country_select = driver.find_element_by_xpath(get_xpath_string_for_element_ends_with("id", "ddlCountryResidence"))
    print("selecting %s as the country of residence" % COUNTRY_OPTION)
    click_option_from_list(country_select, COUNTRY_OPTION)

    # looking for a specific course
    print("locating the Course list")
    course_select = driver.find_element_by_xpath(get_xpath_string_for_element_ends_with("id", "ddlCourse"))
    print("selecting %s course" % COURSE_OPTION)
    click_option_from_list(course_select, COURSE_OPTION)

    # click the search button
    print("Clicking the search button")
    search_button = driver.find_element_by_xpath(get_xpath_string_for_element_ends_with("id",
                                                                                        "btnSearch_MiddleTdBGImage"))
    search_button.click()


# SCRAPE THE ALUMNI SINGLE PAGE SEARCH RESULTS ------------------------------------------------------------------
# TODO: scraping an alumni single list page
def scrape_alumni_page(url):
    # initialise the file
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())

    rows = soup.find("table", id=re.compile(r"spGridAttendees$")).find("tbody").findAll("tbody")
    for row in rows:
        print "----------- PROFILE ------------------"

        tds = row.findAll("td")
        for count, td in enumerate(tds):
            print count, td

            # scrape NAME
            if count == 2:
                name = td.find("span").string
                print "NAME: " + name

            if count == 4:
                graduation = td.find("span").string
                print "GRADUATION: " + graduation

            if count == 7:
                position = td.string.strip()
                print "POSITION: " + position

            if count == 9:
                company = td.string.strip()
                print "COMPANY: " + company

            if count == 11:
                city = td.string.strip()
                print "CITY: " + city

            if count





        # Full Name
        # name = row.find('span', id=re.compile(r"lblFullName$"))
        # print "Name: %s" % name.string

        # Class
        # graduation = row.find


# START MAIN ------------------------------------------------------------------
# load_index()
# search_for_alumni()
scrape_alumni_page("file:///Users/wmaterka/Documents/Code/Python/BlueFountain/HTML/output/Alumni Search Search Results.html")

# TODO: save alumni to a file
# TODO: create a loop to rotate through search pages results
