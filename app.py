import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from flask import Flask, request, render_template

# ===== to set a web server =====
app = Flask(__name__)
@app.route("/askPrice/<search_keywords>") #http://127.0.0.1:5000/askPrice
#@app.route("/askPrice", methods = ["GET", "POST"])


# ===== to show the lowest price result =====
def f_lowest_price(search_keywords):
#     if request.method == "POST":
#         location = request.form.get("location")
#         return f"You are looking for {location}'s pricing"
#     return render_template("form.html")
# if __name__ == '__main__':
#     app.run()
    # return "Which building's pricing are you looking for?".format(request.form['location'])
    # <form action="{{url_for("f_lowest_price")}}" method="POST">
    #     <input type="text" class="form-control" placeholder="location" name="location"></input>
    # </form>

    url = f"https://www.house730.com/buy/?key={search_keywords}"


    response = requests.get(url)
    properties = BeautifulSoup(response.text, "html.parser")

    house_items = properties.select(".house-item")

    # to scrape the data and save
    sale_data = []
    for house_item in house_items:
        # sq_ft = re.findall("(\d+)(?=呎|sq)", house_item.select(".house-content>p:nth-child(3)")[0].text.strip())[0]
        sq_ft = house_item.select(".house-content>p:nth-child(3)")[0].text.strip()
        sq_ft = re.findall("(\d+)(?=呎|sq)", sq_ft)[0]
        price_per_sq_ft = re.findall("\$\d+", house_item.select(".house-content>p:nth-child(3)")[0].text.strip())[0]
        house_item_link = house_item.select(".house-content .title>a")[0]['href']

        sale_data.append([sq_ft, price_per_sq_ft, house_item_link])

    # to show in a table daily (a function to be a dataframe, class constructor)
    sale_data_df = pd.DataFrame(sale_data,
                                columns=["Area", "Price per sq.ft.", "Link"]
                                )

    # to save the data daily (a function to export a csv)
    sale_data_df.to_csv("sale_data.csv")

    # to query the cheapest flat
    lowest_price = sale_data_df[sale_data_df["Price per sq.ft."] == sale_data_df["Price per sq.ft."].min()]
    first_row = lowest_price.iloc[0]

    # sale_data_df.sort_values("Price per sq.ft.").iloc[0]

    out_link = "https://www.house730.com" + first_row['Link']
    return f"Result: </br> Area: {first_row['Area']} sq.ft. </br> Price: {first_row['Price per sq.ft.']} !!! </br> Go > <a href=\"{out_link}\"> Have a Look</a>"

