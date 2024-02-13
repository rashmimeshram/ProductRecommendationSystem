"""
    This python script scraps the product details from flipkart's website, which includes the
    product specifications and customers' reviews for each product. This data is stored in a
    .csv file and is used for product recommendation application that uses machine learning (NLP)
    to recommend product to the user as per his/her needs based on customer reviews analysis.
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------------------------------------------------
# STEP 1 : Scrapping the Product Details  ...

# Initializing a List to store the product details
product_data = []
for i in range(1, 101):
    url = ("https://www.flipkart.com/search?q=laptop+under+under+150000&otracker=search&otracker1=search&marketplace"
           "=FLIPKART&as-show=on&as=off&p%5B%5D=facets.price_range.from%3D20000&p%5B%5D=facets.price_range.to%3DMax&p"
           "%5B%5D=facets.rating%255B%255D%3D1%25E2%2598%2585%2B%2526%2Babove&page=") + str(i)
    r = requests.get(url)

    print("\nFetching the URL ...")

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="_1YokD2 _3Mn1Gg")

    print(f"\nScrapping the data from page {i} ...")

    if box is not None:
        for products_list_element in box.find_all("div", class_="_13oc-S"):
            product_name = products_list_element.find("div", class_="_4rR01T")
            product_price = products_list_element.find("div", class_="_30jeq3 _1_WHN1")
            product_rating = products_list_element.find("div", class_="_3LWZlK")
            product_description = products_list_element.find("ul", class_="_1xgFaf")
            product_url_link = products_list_element.find_all("a", class_="_1fQZEK", href=True)
            product_url = product_url_link[0]['href']
            try:
                if product_name is not None or product_description is not None or product_price is not None or product_rating is not None:
                    filtered_price = ''
                    for l in str(product_price.text):
                        for letter in l:
                            if letter != 'â' or letter != '‚' or letter != '¹':
                                filtered_price += letter
                    product_data.append([product_name.text, filtered_price, product_rating.text,
                                         product_description.text, product_url])
            except Exception as e:
                pass

print("\nCollecting scrapped data ...")
print("\nRe-Structured the data ...")

dataset = pd.DataFrame(data=product_data, columns=["Product", "Price", "Rating", "Description", "Url"])
dataset.to_csv("datasets/flipkart_laptop_data.csv", index=False)

print("\nData dumped in CSV ...")


# ---------------------------------------------------------------------------------------------------------------------
# STEP 2 : Cleaning the Product Details data and constructing
#          the URL/Link for Product Reviews ...

df = pd.read_csv("datasets/flipkart_laptop_data.csv")

# Blank list to store the product-review urls/links
review_urls = []

# Cleaning Data
df['Price'] = df['Price'].str.replace('₹', '')
df['Price'] = df['Price'].str.replace(',', '')
df['Price'] = df['Price'].astype(float)
df['Url'] = 'https://www.flipkart.com' + df['Url']

# Construct the product-review links from product links
for link in df['Url']:
    url = link.split('/p/')
    review_link = url[0] + '/product-reviews/' + url[1]
    review_urls.append(review_link)

# Store the list as column in the DataFrame
df['Review Url'] = review_urls

# Save to csv
df.to_csv("datasets/flipkart_laptop_cleaned_data.csv", index=False)

print(df.info())


# ---------------------------------------------------------------------------------------------------------------------
# STEP 3 : Scrapping the product's specifications and
#          storing them in the dataframe ...

# Load the dataframe from csv file
df = pd.read_csv("datasets/flipkart_laptop_cleaned_data.csv")
print('DataFrame "flipkart_laptop_cleaned_data.csv"  Loaded ...')

all_product_specs = []
count = 0

for url in df.Url:
    count += 1

    # Open the URL page
    r = requests.get(url)

    # Create soup of the page
    soup = BeautifulSoup(r.text, "lxml")

    # find the specifications content from the product page
    box = soup.find("div", class_="_1UhVsV")

    # Create a blank dictionary to store
    specifications = {}
    tables = []
    if box is not None:
        for specs in box.find_all("table", class_="_14cfVK"):
            key = specs.find_all("tr", class_="_1s_Smc row")  # _1hKmbr col col-3-12
            value = specs.find_all("td", class_="URwL2w col col-9-12")
            tables.append(key)

        # [0] : General Specifications
        # [1] : Processor & Memory Features
        # [2] : Operating System
        # [3] : Port & Slot Features
        # [4] : Display & Audio Features
        # [5] : Connectivity Features
        # [6] : Dimensions
        # [7] : Warranty

        for itr in range(len(tables)):
            for x in tables[itr]:
                k = x.find("td", class_="_1hKmbr col col-3-12")
                v = x.find("td", class_="URwL2w col col-9-12")
                specifications[k.text] = v.text

    all_product_specs.append(specifications)
    print(f"\nScraping from url {count} ...")

df1 = pd.DataFrame.from_records(all_product_specs)

# join both the dataframes
df2 = pd.concat([df, df1], axis=1)
df2.to_csv("datasets/flipkart_laptop_specs_data.csv", index=False)


# ---------------------------------------------------------------------------------------------------------------------
# STEP 4 : Scrapping the Product Reviews and
#          storing them in the dataframe ...

product_review_data = []
df = pd.read_csv("datasets/flipkart_laptop_cleaned_data.csv")
pr_id = 0

for review_url in df['Review Url']:
    print(f'SCRAPPING PRODUCT REVIEWS FOR {pr_id + 1}st PRODUCT ... \n')
    pr_id += 1
    r = requests.get(str(review_url))

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="_1YokD2 _3Mn1Gg col-9-12")
    # print(box)
    if box is not None:
        for product_review_element in box.find_all("div", class_="col _2wzgFH K0kLPL"): # col _2wzgFH K0kLPL
            if product_review_element is not None:
                review_title = product_review_element.find("p", class_="_2-N8zT") # _2-N8zT
                customer_rating = product_review_element.find("div", class_="_3LWZlK _1BLPMq")
                review_details = product_review_element.find("div", class_="t-ZTKy")
                upvote = product_review_element.find("div", class_="_1LmwT9")
                downvote = product_review_element.find("div", class_="_1LmwT9 pkR4jH")
                if customer_rating is not None:
                    product_review_data.append([pr_id, review_title.text, customer_rating.text, review_details.text[:-9],
                                                upvote.text, downvote.text])
                else:
                    product_review_data.append([pr_id, review_title.text, '', review_details.text, upvote.text,
                                                downvote.text])

dataset = pd.DataFrame(data=product_review_data, columns=["Product ID", "Title", "rating", "detail_review", "upvote", "downvote"])
dataset.to_csv("datasets/flipkart_laptop_review_data.csv", index=False)


# ------------- END OF PROGRAM -------------

"""
    The dataframes are stored in .csv for each step performed.
    'flipkart_laptop_specs_data.csv' --> LaptopSpecs Table
    'flipkart_laptop_review_data.csv' --> LaptopReview Table
"""
