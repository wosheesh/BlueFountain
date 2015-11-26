from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from BeautifulSoup import BeautifulSoup
import re
import time
import pickle

COUNTRY_OPTION = "Bulgaria"
COURSE_OPTION = "MBA"

alumni_list = []


# returns the id name of a HTML element with id ending with endStringOfControlId
def get_xpath_string_for_element_ends_with(element, end_string):
    return "//*[substring(@" + element + ", string-length(@" + element + ")- string-length(\"" + end_string + "\") + 1 )=\"" + end_string + "\"]"


# selects and option from a list
def click_option_from_list(list_name, option_name):
    for option in list_name.find_elements_by_tag_name('option'):
        if option.text == option_name:
            option.click()  # select() in earlier versions of webdriver
            return True
    return False


# LOAD LOGIN ------------------------------------------------------------------
def load_index(url):

    global driver

    # replace with your firefox profile
    fp = webdriver.FirefoxProfile('/Users/wmaterka/Library/Application Support/Firefox/Profiles/7xp1ls6v.blu')
    # enter your url here

    # Initialise webdriver and open the login page TEST URL

    print("opening Firefox as %s \naccessing %s" % (fp.path, url))
    driver = webdriver.Firefox(fp)
    driver.get(url)

    # html_source = driver.page_source

    # write the 1st index file
    # print("saving the index file")
    # output_file = open('./HTML/output/index.html', 'w+')
    # output_file.write(html_source.encode("utf-8"))


# PERFORM THE DB SEARCH ------------------------------------------------------------------
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
def scrape_alumni_page(html):

    soup = BeautifulSoup(html)

    rows = soup.find("table", id=re.compile(r"spGridAttendees$")).find("tbody").findAll("tbody")

    alumni_single_page_list = []

    for row in rows:
        print "----------- PROFILE ------------------"

        an_alumni = {}

        tds = row.findAll("td")
        for count, td in enumerate(tds):

            if count == 2:
                an_alumni["Name"] = td.find("span").contents[0].strip()
                print "NAME: " + an_alumni["Name"]

            if count == 4:
                an_alumni["Graduation"] = td.find("span").contents[0].strip()
                print "GRADUATION: " + an_alumni["Graduation"]

            if count == 5:
                an_alumni["e-mail"] = td.find("input")["onclick"]
                an_alumni["e-mail"] = re.search(r"'mailto:(.*?)'", an_alumni["e-mail"]).group(1)
                print "EMAIL: " + an_alumni["e-mail"]

            if count == 7:
                an_alumni["Position"] = td.string.strip()
                print "POSITION: " + an_alumni["Position"]

            if count == 9:
                an_alumni["Company"] = td.string.strip()
                print "COMPANY: " + an_alumni["Company"]

            if count == 11:
                an_alumni["City"] = td.string.strip()
                print "CITY: " + an_alumni["City"]

            if count == 13:
                an_alumni["Country"] = td.string.strip()
                print "COUNTRY: " + an_alumni["Country"]

        alumni_single_page_list.append(an_alumni)

    return alumni_single_page_list


# returns a driver element if there's another page or false if it was the last one
def loop_alumni_pages(page):

    # check if this is the last page in the list
    soup = BeautifulSoup(page)
    page_links = soup.find("tr", {"class": "GridViewPaging"}).find("td").findChildren()

    for count, page_link in enumerate(page_links):
        # check if it's a span
        if page_link.name == "span":
            print "span found at: %d" % count

            # if it is span check if this is the last page_link
            # if it isn't the last page_link return the next link url
            if count < len(page_links) - 1:
                print "this isn't the last link on the list"
                next_link = page_links[count+1]

                # extract the script from the link
                # next_link_script = re.search(r"javascript:(.*?)$", next_link["href"]).group(1)
                # print "the next link text is:"
                # print next_link_script
                # return next_link_text

                # extract the text in the <a> tag
                next_link_text = next_link.contents
                print "the content of the <a> tag for next page is: " + next_link_text[0]
                return next_link_text[0]

            else:
                print "this was the last page in search results"
                return False


# START MAIN ------------------------------------------------------------------
# TODO: create a loop to rotate through search pages results
# TODO: save alumni to a file

url_local = "file:///Users/wmaterka/Documents/Code/Python/BlueFountain/HTML/output/end page.html"
url_live = "https://iconnect.insead.edu/Search/Pages/Default.aspx"

load_index(url_live)
search_for_alumni()

# scraping the 1st search result page
print "scraping the 1st search result page"
html = driver.page_source
alumni_list.extend(scrape_alumni_page(html))
print alumni_list

count = 0
while True:
    next_move = loop_alumni_pages(html)
    print count, next_move
    if next_move:
        print "clicking the next page number: " + next_move
        driver.find_element_by_link_text(next_move).click()

        print "page loading"
        time.sleep(13)

        print "scraping the 2nd search result page"
        html = driver.page_source
        alumni_list.extend(scrape_alumni_page(html))
    else:
        print "Finished scraping"
        print "saving file"
        output = open("alumnis.pkl", "wb")
        print alumni_list
        pickle.dump(alumni_list, output)
        output.close()
        break
