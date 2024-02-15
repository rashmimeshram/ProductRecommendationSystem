from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)


# load data from .csv using pandas
def load_data():
    df = pd.read_csv("product_spec_data.csv")
    df = df.sort_values(by=["prs"], ascending=False)
    laptop_data = []

    for l in range(len(df)):

        # Handling the nan values in the Laptop Specs DataFrame
        if not pd.isna(df.iloc[l]["Processor Name"]):
            processor_brand = df.iloc[l]["Processor Name"]
        else:
            processor_brand = ''

        if not pd.isna(df.iloc[l]["Processor Generation"]):
            processor_generation = df.iloc[l]["Processor Generation"]
        else:
            processor_generation = ''

        if not pd.isna(df.iloc[l]["SSD Capacity"]):
            ssd_capacity =  str(df.iloc[l]["SSD Capacity"]) + ' SSD'
        else:
            ssd_capacity = '-'

        if not pd.isna(df.iloc[l]["Graphic Processor"]):
            graphic_processor = df.iloc[l]["Graphic Processor"]
        else:
            graphic_processor = '-'

        if not pd.isna(df.iloc[l]["Refresh Rate"]):
            refresh_rate = df.iloc[l]["Refresh Rate"]
        else:
            refresh_rate = '-'

        if not pd.isna(df.iloc[l]["prs"]):
            prs = format(df.iloc[l]["prs"] * 100, ".2f")
            int_prs = df.iloc[l]["prs"]
        else:
            prs = 0
            int_prs = 0

        laptop_data.append(
            ['/static/images/generic-laptop.jpg',
             str(df.iloc[l]["Product"]),
             int(df.iloc[l]["Price"]),
             str(processor_brand) + " " + str(processor_generation),
             str(df.iloc[l]["RAM"]) + " " + str(df.iloc[l]["RAM Type"]) + ' RAM',
             ssd_capacity,
             str(graphic_processor),
             str(df.iloc[l]["Screen Size"]) + " (" + str(df.iloc[l]["Screen Resolution"]) + ")",
             refresh_rate,
             str(df.iloc[l]["Operating System"]),
             prs,
             df.iloc[l]["Url"],
             df.iloc[l]["Type"],
             int_prs]
        )

    return laptop_data


@app.route("/", methods=['GET', 'POST'])
def home():
    # Flipkart Laptops' data (flipkart_laptop_cleaned_data.csv)
    data = load_data()
    # print(data)

    # data = [['/static/images/laptop.jpg', 'MackBook Air 3', 200000, 'A16 Bionic Chip', '8 GB RAM', '512 GB SSD',
    #          'NVIDIA GeForce RTX 2040', '13.6 Inch (2560 x 1664 Pixel)', '90 Hz refresh rate', 'Mac OS', 94],
    #         ['/static/images/hp-laptop.jpg', 'HP Elitebook Pro', 110000, 'Intel Core i5 12gen', '16 GB RAM',
    #          '512 GB SSD', 'Intel Integrated Iris Xe', '14 Inch (1920 x 1080 Pixels)', '60 Hz refresh rate',
    #          'Windows 11', 72],
    #         ['/static/images/msi-laptop.jpeg', 'MSI Katana', 80000, 'AMD Ryzen 6700H', '16 GB RAM', '1 TB SSD',
    #          'AMD Radeon AMD', '15.6 Inch (1920 x 1080 Pixels)', '144 Hz refresh rate', 'Windows 11', 80],
    #         ['/static/images/acer-laptop.jpg', 'ACER Aspire 7', 45000, 'Intel Core i5 11gen', '16 GB RAM', '512 GB SSD',
    #          'NA', '15.6 Inch (1920 x 1080 Pixels)', '120 Hz refresh rate', 'Windows 11', 88],
    #         ['/static/images/lenevo-laptop.jpg', 'LENOVO notebook 5', 67000, 'AMD Ryzen 4500P', '8 GB RAM', '1 TB HDD',
    #          'NVIDIA GTX MX400', '15.6 Inch (1920 x 1080 Pixels)', '60 Hz refresh rate', 'DOS', 54],
    #         ['/static/images/asus-laptop.jpg', 'ASUS ROG Zephyrus', 140000, 'AMD Ryzen 7600H', '16 GB RAM',
    #          '512 GB SSD', 'NVIDIA GeForce RTX 3060', '14 Inch (1920 x 1080 Pixels)', '144 Hz refresh rate',
    #          'Windows 11', 89],
    #         # {'7': ['MackBook Air 3']},
    #         # {'8': ['MackBook Air 3']}
    #         ]
    return render_template('layout.html', data=data)


@app.route('/result', methods=['POST'])
def process_input():

    # Laptop Data
    data = load_data()


    # data = [['/static/images/laptop.jpg', 'MackBook Air 3', 200000, 'A16 Bionic Chip', '8 GB RAM', '512 GB SSD',
    #          'NVIDIA GeForce RTX 2040', '13.6 Inch (2560 x 1664 Pixel)', '90 Hz refresh rate', 'Mac OS', 94],
    #         ['/static/images/hp-laptop.jpg', 'HP Elitebook Pro', 110000, 'Intel Core i5 12gen', '16 GB RAM',
    #          '512 GB SSD', 'Intel Integrated Iris Xe', '14 Inch (1920 x 1080 Pixels)', '60 Hz refresh rate',
    #          'Windows 11', 72],
    #         ['/static/images/msi-laptop.jpeg', 'MSI Katana', 80000, 'AMD Ryzen 6700H', '16 GB RAM', '1 TB SSD',
    #          'AMD Radeon AMD', '15.6 Inch (1920 x 1080 Pixels)', '144 Hz refresh rate', 'Windows 11', 80],
    #         ['/static/images/acer-laptop.jpg', 'ACER Aspire 7', 45000, 'Intel Core i5 11gen', '16 GB RAM', '512 GB SSD',
    #          'NA', '15.6 Inch (1920 x 1080 Pixels)', '120 Hz refresh rate', 'Windows 11', 88],
    #         ['/static/images/lenevo-laptop.jpg', 'LENOVO notebook 5', 67000, 'AMD Ryzen 4500P', '8 GB RAM', '1 TB HDD',
    #          'NVIDIA GTX MX400', '15.6 Inch (1920 x 1080 Pixels)', '60 Hz refresh rate', 'DOS', 54],
    #         ['/static/images/asus-laptop.jpg', 'ASUS ROG Zephyrus', 140000, 'AMD Ryzen 7600H', '16 GB RAM',
    #          '512 GB SSD', 'NVIDIA GeForce RTX 3060', '14 Inch (1920 x 1080 Pixels)', '144 Hz refresh rate',
    #          'Windows 11', 89],
    #         # {'7': ['MackBook Air 3']},
    #         # {'8': ['MackBook Air 3']}
    #         ]

    # inputs from ajax
    min_budget = int(request.form.get('min_budget'))
    max_budget = int(request.form.get('max_budget'))
    laptop_type = request.form.get('laptop_type')

    # Processing the inputs from AJAX
    print(f"min-budget: {min_budget}\n"
          f"max-budget: {max_budget}\n"
          f"laptop-type: {laptop_type}")

    filtered_laptops = []

    for laptop in data:
        if min_budget <= laptop[2] <= max_budget and laptop_type == laptop[12] and laptop[13] >= 0.6:
            filtered_laptops.append(laptop)

    return jsonify({'data': filtered_laptops})


@app.template_filter()
def numFormat(value):
    """
        Custom JINJA2 filter for adding "," seperator to numeric values.
    """
    return format(int(value), ',d')


if __name__ == '__main__':
    app.run(debug=True)
