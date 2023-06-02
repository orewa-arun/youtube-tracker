import numpy as np
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scrapper import scrape_stats_count
import time

from dotenv import dotenv_values

mdb_link = dotenv_values(".env")["MONGO_SERVER_PATH"]

# Connect to MongoDB
client = MongoClient(mdb_link)
db = client["youtube"]
collection = db["views"]

start_time = datetime.now() + timedelta(seconds=5)
end_time = start_time + timedelta(minutes=30)

link = st.text_input('Link of the youtube video')
period = number = st.number_input('Enter the frequency time period in mins')


def add_data(link, times, views, likes):
    v, l = scrape_stats_count(link)
    times.append(datetime.now())
    views.append(v)
    likes.append(l)

    # Update a single document
    query = {"link": link}  # Specify the criteria to match the document
    updated_views = {"$set": {"views": views}}  # Specify the new values
    updated_timestamps = {"$set": {"timestamps": times}}
    updated_likes = {"$set": {"likes": likes}}
    collection.update_one(query, updated_views)
    collection.update_one(query, updated_likes)
    collection.update_one(query, updated_timestamps)


def getdiffArray(arr):
    d1 = arr.copy()
    d2 = arr.copy()
    d1.pop(0)
    d2.pop()

    d = np.subtract(np.array(d1).astype(
        float), np.array(d2).astype(float))

    return d


if link and period:

    cursorlength = len(list(collection.find(
        {"link": link})))

    if cursorlength == 0:
        timestamps = []
        views = []
        likes = []

        store_obj = {
            "link": link,
            "timestamps": timestamps,
            "views": views,
            "likes": likes
        }
        collection.insert_one(store_obj)

    cursor = collection.find({"link": link})

    st.write("Note :you can track youtube video ", link,
             " with a period of ", period, " only for 1 hour")

    placeholder = st.empty()

    while True:

        times = cursor[0]["timestamps"]
        views = cursor[0]["views"]
        likes = cursor[0]["likes"]

        add_data(link, times, views, likes)

        with placeholder.container():
            st.markdown("##live feed of video")

            fig_col1, fig_col2 = st.columns(2)

            with fig_col1:
                st.markdown("### ViewCount Chart")
                fig, ax = plt.subplots()
                ax.plot(times, views)
                ax.set_xlabel("Time")
                ax.set_ylabel("Views")
                plt.xticks(rotation=45)
                st.write(fig)
                plt.close()

            with fig_col2:
                st.markdown("### LikeCount Chart")
                fig, ax = plt.subplots()
                ax.plot(times, likes)
                ax.set_xlabel("Time")
                ax.set_ylabel("Likes")
                plt.xticks(rotation=45)
                st.write(fig)
                plt.close()

            ratefig_col1, ratefig_col2 = st.columns(2)

            viewsd = getdiffArray(views)
            likesd = getdiffArray(likes)
            timesd = np.array(times.copy()[1:])
            # print(len(views), len(viewsd), len(times), len(timesd))
            # print(viewsd, timesd, likesd)

            with ratefig_col1:
                st.markdown("### ViewCount Rate Chart")
                fig, ax = plt.subplots()
                ax.plot(timesd, viewsd)
                ax.set_xlabel("Time")
                ax.set_ylabel("Views difference")
                plt.xticks(rotation=45)
                st.write(fig)
                plt.close()

            with ratefig_col2:
                st.markdown("### LikeCount Rate Chart")
                fig, ax = plt.subplots()
                ax.plot(timesd, likesd)
                ax.set_xlabel("Time")
                ax.set_ylabel("Likes difference")
                plt.xticks(rotation=45)
                st.write(fig)
                plt.close()

            time.sleep(period*60)
            plt.close()


client.close()
