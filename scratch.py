import pandas as pd
import urllib.request
import pprint as pp
from urllib.request import urlopen
from bs4 import BeautifulSoup
from IPython.display import display

# List of sku numbers to run
sku_list = [
'Add sku list'

]


# Setting up the user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)

# Setting up a dataframe
data_dict = {'Sku': [],   
            'Product_Title': [],
            'Marketing_Copy': [],
            'Bullet1': [], 
            'Bullet2': [], 
            'Bullet3': [], 
            'Bullet4': [], 
            'Bullet5': [], 
            'Bullet6' : [], 
            'Bullet7': [], 
                 }

# main_df = pd.DataFrame.from_dict(mc_dict)
dict_list= []

for sku in sku_list:
     # Adding the sku to the mc_dict Sku column
    data_dict['Sku'].append(sku)
    
    try:
        # Extracting the page source for the sku from Signature Hardwares website and creating a soup object
        page = urlopen('https://www.jonesstephens.com/{}'.format(sku))
        soup = BeautifulSoup(page, 'lxml')
        
        # Extracting Product Title
        # try:
        title = soup.find("div", {"class": "product-name"})
        title = title.text
        data_dict['Product_Title'].append(title.strip())

        # Extracting Marketing Copy
        mc_title = soup.find("div", {"class": "custom-tab"})
        mc_title = mc_title.text
        data_dict['Marketing_Copy'].append(mc_title.strip())

        # Extracting all specs into dictionaries and adding them to dict_list
        whole_div = soup.find("div", {"class": "productTabs-body"})
        keys = whole_div.find_all("span", {"class": "label"})
        values = whole_div.find_all("span", {"class": "value"})
        
        d = {'Sku': []}
        d['Sku'].append(sku)
        
        try:
            for key, value in zip(keys, values):
                d[key.text] = value.text
            dict_list.append(d)
            
        except:
            dict_list.append('NULL')
        pp.pprint(dict_list)
        
        # Extracting Bullets
        bullet_div = soup.find("div", {"class": "full-description plumbing-full-description"})
        ul = bullet_div.find("ul")
        lis = ul.find_all('li')
        li_list = []
        for li in lis:
            li = str(li.text).strip()
            li_list.append(li)
        
        try:
            data_dict['Bullet1'].append(li_list[0])
        except:
            data_dict['Bullet1'].append('NULL')

        try:
            data_dict['Bullet2'].append(li_list[1])
        except:
            data_dict['Bullet2'].append('NULL')

        try:
            data_dict['Bullet3'].append(li_list[2])
        except:
            data_dict['Bullet3'].append('NULL')

        try:
            data_dict['Bullet4'].append(li_list[3])
        except:
            data_dict['Bullet4'].append('NULL')

        try:
            data_dict['Bullet5'].append(li_list[4])
        except:
            data_dict['Bullet5'].append('NULL')

        try:
            data_dict['Bullet6'].append(li_list[5])
        except:
            data_dict['Bullet6'].append('NULL')

        try:
            data_dict['Bullet7'].append(li_list[6])
        except:
            data_dict['Bullet7'].append('NULL')
    except:
        data_dict['Bullet1'].append('NULL')
        data_dict['Bullet2'].append('NULL')
        data_dict['Bullet3'].append('NULL')
        data_dict['Bullet4'].append('NULL')
        data_dict['Bullet5'].append('NULL')
        data_dict['Bullet6'].append('NULL')
        data_dict['Bullet7'].append('NULL')

# Creating dataframes from the dict_list and mc_dict dictionaries
build_df = pd.DataFrame.from_dict(data_dict).fillna('NULL')
main_df = pd.DataFrame.from_dict(dict_list).fillna('NULL')

# Changing the Sku column from main_df from list to a string format
sku_col = main_df['Sku']
new_col = []
for sku in sku_col:
    sku = str(sku)[2:8]
    new_col.append(sku)

main_df['Sku'] = new_col
main_df.set_index('Sku', inplace=True)

# Creating and printing the final dataframe
final_df = pd.merge(main_df, build_df, how='left', left_on='Sku', right_on='Sku')
final_df = final_df.fillna('NULL')
final_df.set_index('Sku', inplace=True)
display(final_df.head())

#  Writing the dataframe to an excel worksheet
final_df.to_excel('Jones_Stephens_Data.xlsx', sheet_name='Data')

print('Run Complete!')

    