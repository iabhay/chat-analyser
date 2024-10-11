import streamlit as st
import preprocessor, stats
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Chat Analyser")
st.sidebar.header("By Abhay")
st.sidebar.text("Instructions:-\n1.Export any chat from your whatsapp.\n2.Upload that txt file below and run analysis.")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overview")

    selected_user = st.sidebar.selectbox("Select User",user_list)
        ##TOTAL ANALYSIS
    if st.sidebar.button("Run Analysis"):
        mess, words, media_files, links_count = stats.fetch_stats(selected_user, df)
        st.title("Stats here -> ")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(mess)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(media_files)
        with col4:
            st.header("Total Links")
            st.title(links_count)


        #monthly timeline
        st.title("Monthly Timeline")
        timeline = stats.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'red')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = stats.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # ACTIVITY MAP
        st.title("USER ACTIVITY")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day: ")
            busy_day = stats.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month: ")
            busy_month = stats.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        #Heatmap
        st.title("HeatMap")
        user_heatmap = stats.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        ## busy user
        if selected_user == "Overview":
            st.title("Chatters")
            busy, new_df = stats.most_busy_users(df)
            fig, ax = plt.subplots()
            ax.patch.set_facecolor('white')
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(busy.index, busy.values, color = 'red', edgecolor = 'darkblue')
                plt.xticks(rotation="vertical")
                ax.tick_params(axis='x', colors='black')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        ## wordcloud
        st.title("WORDCLOUD")
        wc_df = stats.wc_maker(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)

        #MOST COMMON WORDS
        st.title("MOST COMMON WORDS")
        common_df = stats.common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_df[0], common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        # st.dataframe(common_df)

        #EMOJI
        st.title("EMOJI COUNTER")
        emoji_df = stats.emojis_helper(selected_user, df)
        col1, col2 =st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct = "%0.2f")
            st.pyplot(fig)
