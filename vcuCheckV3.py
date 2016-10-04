from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import smtplib

yunm = "first last"
semid = "Fall 2016"
termid = "201710" # The Year Term you can find it on the class page
subid = "INFO"
subidn = "350"
#courseid = "22004"
courseid = "13436" #find the course id on the actual class page


def sendEmail():
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("vcuclasschecker", "vcusefisk123") #"email","pass" (no @gmail)
	SUBJECT = "" + semid +" Semester Class Registration"
        MSG = "" + yunm + ",\n We were able to successfully on registering " + subid +" " + subidn + " for the " + semid +" semester.\n"
        message = 'Subject: %s\n\n%s' % (SUBJECT, MSG)
	server.sendmail("vcuclasschecker@gmail.com", "vcuclasschecker@gmail.com", message)
        

# start selenium instance and navigate to login
driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get('https://ssb.vcu.edu/proddad/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu')
print "Launching Web Browser"
# login
eid = driver.find_element_by_name('sid')
pas = driver.find_element_by_name('PIN')
eid.send_keys('') #EID
pas.send_keys('') #PASS
pas.send_keys(Keys.RETURN)
print "Logging into VCU"
# navigate to page 
#driver.find_element_by_xpath("/html/body/div[@class='pagebodydiv']/table[@class='menuplaintable']/tbody/tr[3]/td[@class='mpdefault'][2]/a[@class='submenulinktext2 ']").click()
try:
	driver.find_element_by_partial_link_text('Student').click()
	pass
except:
	driver.find_element_by_partial_link_text('Student').click()
	pass

driver.find_element_by_partial_link_text('Regist').click()
driver.find_element_by_partial_link_text('Look').click()

# select Semester
termList = Select(driver.find_element_by_id('term_input_id'))
termList.select_by_visible_text(semid)
driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()
print "Selecting Semester"
# Advanced Search
driver.find_element_by_xpath("//input[@type='submit' and @value='Advanced Search']").click()

#Searches Advanced
subj = Select(driver.find_element_by_css_selector('select#subj_id'))
subj.select_by_value(subid)
cos = driver.find_element_by_name('sel_crse')
cos.send_keys(subidn) #classid
driver.find_element_by_xpath("//input[@type='submit' and @value='Section Search']").click()
print "On the class page now"

# Check to see if you can sign up at all via checkbox

try:
	checkbox = driver.find_element_by_xpath("//input[@name='sel_crn' and @value='" + courseid + " " + termid + "']")
	if(checkbox.is_selected()):
		pass
	else:
		checkbox.click()
		driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
                print "Found the class! Registering!"
		sendEmail()
		driver.close()
        
except:
        print "No Classes Found"
        driver.close()




