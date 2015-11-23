from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
import BeautifulSoup

COUNTRY_OPTION = "United Kingdom"
COURSE_OPTION = "MBA"


# returns the id name of a HTML element with id ending with endStringOfControlId
def get_xpath_string_for_id_ends_with(end_string):
    return "//*[substring(@id, string-length(@id)- string-length(\"" + end_string + "\") + 1 )=\"" + end_string + "\"]"


# selects and option from a list
def click_option_from_list(list_name, option_name):
    for option in list_name.find_elements_by_tag_name('option'):
        if option.text == option_name:
            option.click()  # select() in earlier versions of webdriver
            return True
    return False


# START MAIN ------------------------------------------------------------------

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


def search_for_alumni():
    # looking for country of residence --------------------------------------------
    print("locating the Country Residence option")
    country_select = driver.find_element_by_xpath(get_xpath_string_for_id_ends_with("ddlCountryResidence"))
    print("selecting %s as the country of residence" % COUNTRY_OPTION)
    click_option_from_list(country_select, COUNTRY_OPTION)

    # looking for a specific course -----------------------------------------------
    print("locating the Course list")
    course_select = driver.find_element_by_xpath(get_xpath_string_for_id_ends_with("ddlCourse"))
    print("selecting %s course" % COURSE_OPTION)
    click_option_from_list(course_select, COURSE_OPTION)

    # click the search button -----------------------------------------------
    #  ctl00$SPWebPartManager1$g_e010aaa7_e55e_45f3_858e_3ff3648af2ce$ctl00$btnSearch_MiddleTdBGImage

    print("Clicking the search button")
    search_button = driver.find_element_by_xpath(get_xpath_string_for_id_ends_with("btnSearch_MiddleTdBGImage"))
    search_button.click()


# TODO: scraping an alumni list page
def scrape_alumni():
    url = "/Users/wmaterka/Documents/Code/Python/BlueFountain/HTML/output/Alumni Search Search Results.html"

# MAIN
load_index()
search_for_alumni()

# TODO: save alumni to a file
# TODO: create a loop to rotate through search pages results
