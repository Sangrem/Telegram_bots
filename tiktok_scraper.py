from selenium import webdriver
import time

data = []
driver = webdriver.Chrome()

def is_exist(login):
    for person in data:
        if person['name'] == login:
            return True
    return False

def parse(main_url):
    global data, driver
    driver.get(main_url)
    driver.execute_script("window.scrollTo(0, 9999)")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 9999)")
    elements = driver.find_elements_by_css_selector('a')
    page_urls = [element.get_attribute('href') for element in elements]
    for url in page_urls:
        try:
            if "@" in url:
                driver.get(url)
        except:
            pass
        try:
                    name = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div/header/div[1]/div[2]/h2').text
                    if not is_exist(name):
                        following = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div/header/h2[1]/div[1]/strong').text
                        followers = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div/header/h2[1]/div[2]/strong').text
                        likes = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div/header/h2[1]/div[3]/strong').text
                        data.append({'name': name, 'following': following, 'followers': followers, 'likes': likes, 'url': url})
                        print("[+] " + name)
        except:
            pass               

f = open("result.txt","w+")
for i in range(len(data)):
     f.write('\nName: {} \nFollowing: {} \nFollowers: {} \nLikes: {} \nURL: {}\n=============================================='.format(
         data[i]['name'], data[i]['following'], data[i]['followers'], data[i]['likes'], data[i]['url']
     ))
f.close()