import numpy as np
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scrapper import scrape_view_count
import time

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["youtube"]
collection = db["views"]

start_time = datetime.now() + timedelta(seconds=5)
end_time = start_time + timedelta(minutes=30)

link = st.text_input('Link of the youtube video')
period = number = st.number_input('Enter the frequency time period in mins')
print(period, period*60)

st.write(period)


def add_data(link, times, views):
    v = scrape_view_count(link)
    times.append(datetime.now())
    views.append(v)

    # Update a single document
    query = {"link": link}  # Specify the criteria to match the document
    updated_views = {"$set": {"views": views}}  # Specify the new values
    updated_timestamps = {"$set": {"timestamps": times}}
    collection.update_one(query, updated_views)
    collection.update_one(query, updated_timestamps)


if link:
    timestamps = []
    views = []

    view = {
        "link": link,
        "timestamps": timestamps,
        "views": views
    }
    collection.insert_one(view)

    st.write("link of the video", link)
    cursor = collection.find(
        {"link": link})

    placeholder = st.empty()

    while True:

        times = cursor[0]["timestamps"]
        views = cursor[0]["views"]

        add_data(link, times, views)

        with placeholder.container():
            st.markdown("##live feed of views")

            fig, ax = plt.subplots()
            ax.plot(times, views)
            ax.set_xlabel("Time")
            ax.set_ylabel("Views")
            plt.xticks(rotation=45)

            st.write(fig)
            time.sleep(period*60)
            plt.close()

client.close()
