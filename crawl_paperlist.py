import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# change driver path according to your configuration
#path = "/snap/bin/chromium.chromedriver"
#driver = webdriver.Chrome(path)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://openreview.net/group?id=NeurIPS.cc/2022/Conference')
#driver.get('https://openreview.net/group?id=ICLR.cc/2022/Conference')
#driver = webdriver.Chrome()


cond = EC.presence_of_element_located((By.XPATH, '//*[@id="accepted-papers"]/nav/ul/li[13]/a'))
WebDriverWait(driver, 60).until(cond)

with open('NeurIPS_paper_list.tsv', 'w', encoding='utf8') as f:
    f.write('\t'.join(['paper_id', 'title', 'link', 'keywords', 'abstract'])+'\n')

for page in tqdm(range(1, 68)):
    text = ''
    #elems = driver.find_elements_by_xpath('//*[@id="accepted-papers"]/ul/li')
    elems = driver.find_elements("xpath", '//*[@id="accepted-papers"]/ul/li')
    for i, elem in enumerate(elems):
        try:
            # parse title
            title = elem.find_element("xpath", './h4/a[1]')
            link = title.get_attribute('href')
            paper_id = link.split('=')[-1]
            title = title.text.strip().replace('\t', ' ').replace('\n', ' ')
            # show details
            elem.find_element("xpath", './a').click()
            time.sleep(0.2)
            # parse keywords & abstract
            #items = elem.find_elements_by_xpath('.//li')
            items = driver.find_elements("xpath", './/li')
            keyword = ''.join([x.text for x in items if 'Keywords' in x.text])
            abstract = ''.join([x.text for x in items if 'Abstract' in x.text])
            keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ').replace('Keywords: ', '')
            abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
            text += paper_id+'\t'+title+'\t'+link+'\t'+keyword+'\t'+abstract+'\n'
        except Exception as e:
            print(f'page {page}, # {i}:', e)
            continue

    with open('NeurIPS_paper_list.tsv', 'a', encoding='utf8') as f:
        f.write(text)

    # next page
    try:
        driver.find_element("xpath", '//*[@id="accepted-papers"]/nav/ul/li[13]/a').click()
        time.sleep(2) # NOTE: increase sleep time if needed
    except:
        print('no next page, exit.')
        break
