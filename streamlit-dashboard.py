import psycopg2
import requests
import json
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image

icon = Image.open(r"c:\Users\Lenovo\Downloads\download.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "auto")

st.title(":rainbow[Phonepe Pulse Data Visualization and Exploration]")


SELECT = option_menu(
    menu_title = None,
    options = ["Home","Top Charts","Explore Data"],
    icons =["house","bar-chart","toggles"],
    default_index=1,
    orientation="vertical",
    styles={"container": { "background-color": "white"},
        "icon": {"color": "violet", "font-size": "20px"},

        "nav-link": {"font-size": "15px", "text-align": "left", "margin": "1px", "--hover-color": "#F0F2F6"},
        "nav-link-selected": {"background-color": "#262730"}})
if SELECT=="Home":  
     col1,col2 = st.columns(2)
     with col1:
       st.video(r"c:\Users\Lenovo\Downloads\phone.mp4")
     with col2:
        st.subheader("PhonePe")
        st.image(Image.open(r"c:\Users\Lenovo\Downloads\download.png"),width = 200)
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")


if SELECT == "Top Charts":
    st.subheader(":blue[Top chart]")
    Type = st.selectbox(":orange[select]", ("selectone","Transactions", "Users"))

    if Type == "Transactions":
        column1,column2= st.columns([2,2],gap="small")
        with column1:
            Year = st.slider(":blue[Year]:", min_value=2018, max_value=2022)
            st.write('- Year -  2018 to 2023')
            Quarter = st.slider(":blue[Quarter]:", min_value=1, max_value=4)
            st.write('- Quarter - Q1 (Jan to Mar), Q2 (Apr to June), Q3 (July to Sep), Q4 (Oct to Dec)')
        with  column2:
            st.subheader(":blue[view transactions  related details]:")
            st.subheader(":red[Transaction]")
            st.write(' - top 10 states wise transtion_amount and transaction_count')
            st.write(' - top 10 districts wise transtion_amount and transaction_count')
            st.write(' - top 10 pincodes wise transtion_amount and transaction_count')
        col1,col2,col3 = st.columns([1,1,1],gap="small")

        kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432,database='phonepe_project')
        dinesh = kumar.cursor()
        with col1:
            st.markdown("### :blue[State]")
            dinesh.execute(f"select state, sum(transaction_count) as total_transactions_Count, sum(transaction_amount) as total_amount from aggregated_transaction where year = {Year} and quarter = {Quarter} group by state order by total_amount desc limit 10")
            df = pd.DataFrame(dinesh.fetchall(), columns=['state', 'total_transactions_count','total_amount'])
            fig = px.pie(df, values='total_amount',
                             names='state',
                             title='Top 10 state Vs total_amount',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['total_transactions_count'],
                             hole=0.2,
                             labels={'total_transactions_Count':'total_transactions_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=10)
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.markdown("### :blue[District]")
            dinesh.execute(f"select district , sum(Transaction_count) as total_count, sum(Transaction_amount) as total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by district order by total_amount desc limit 10")
            df = pd.DataFrame(dinesh.fetchall(), columns=['district', 'trans_count','total_amount'])

            fig = px.pie(df, values='total_amount',
                             names='district',
                             title='Top 10 district Vs total_amount',
                             color_discrete_sequence=px.colors.sequential.Sunsetdark,
                             hover_data=['trans_count'],
                             hole=0.3,
                             labels={'trans_count':'trans_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        #---transaction types vs total_transactions----#
            kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432,database='phonepe_project')
            dinesh = kumar.cursor() 
            dinesh.execute(f"select transaction_type, sum(transaction_count) as total_transactions, sum(transaction_amount) as total_amount from aggregated_transaction where year= {Year} and quarter = {Quarter} group by transaction_type order by transaction_type")
            df = pd.DataFrame(dinesh.fetchall(), columns=['transaction_type', 'total_transactions','total_amount'])

            fig = px.bar(df,
                     title='transaction types vs total_transactions',
                     x="transaction_type",
                     y="total_transactions",
                     orientation='v',
                     color='total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)


        with col3:
            st.markdown("### :blue[Pincode]")
            dinesh.execute(f"select District_Pincode, sum(Transaction_count) as total_transaction_count, sum(Transaction_amount) as total_amount from top_transaction where year = {Year} and quarter = {Quarter} group by District_Pincode order by total_amount desc limit 10")
            df = pd.DataFrame(dinesh.fetchall(), columns=['District_Pincode', 'Transaction_count','total_amount'])
            fig = px.pie(df, values='total_amount',
                             names='District_Pincode',
                             title='Top 10 Pincode Vs total_amount',
                             color_discrete_sequence=px.colors.sequential.Blugrn,
                             hover_data=['Transaction_count'],
                             hole=0.3,
                             labels={'Transaction_count':'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    if Type=="Users":

        kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432,database='phonepe_project')
        dinesh = kumar.cursor()
        column1,column2= st.columns([2,2],gap="small")
        with column1:
            Year = st.slider(":rainbow[Year]:", min_value=2018, max_value=2022)
            st.write('- Year -  2018 to 2023')
            Quarter = st.slider(":rainbow[Quarter]:", min_value=1, max_value=4)
            st.write('- Quarter - Q1 (Jan to Mar), Q2 (Apr to June), Q3 (July to Sep), Q4 (Oct to Dec)')
        with  column2:
            st.subheader(":rainbow[view Users  related details]:")
            st.subheader(":red[Transaction]")
            st.write(' - top 10 districts wise  Total_Users')
            st.write(' - top 10 pincodes wise Total_Users')
            st.write(' - top 10 states wise Total_Users and Total_Appopens')
        col1,col2,col3= st.columns([2,2,2],gap="small")


        with col1:
            st.markdown("### :red[District]")
            dinesh.execute(f"select District, sum(Registered_User) as total_users, sum(app_opens) as total_app_opens from map_user where year = {Year} and quarter = {Quarter} group by District order by total_users desc limit 10")
            df = pd.DataFrame(dinesh.fetchall(), columns=['District', 'total_users','total_app_opens'])
            df['total_users']= df['total_users'].astype(float)
            fig = px.bar(df,
                         title='Top 10 District Vs total_users',
                         x="District",
                         y="total_users",
                         orientation='v',
                         color='total_app_opens',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("### :red[District_Pincode]")
            dinesh.execute(f"select District_Pincode, sum(Registered_User) as total_users from top_user where year = {Year} and quarter = {Quarter} group by District_Pincode order by total_users desc limit 10")
            df = pd.DataFrame(dinesh.fetchall(), columns=['District_Pincode', 'total_users'])
            fig = px.pie(df,
                         values='total_users',
                         names='District_Pincode',
                         title='Top 10 District_Pincode Vs total_users',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['total_users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


        with col3:
            st.markdown("### :red[State]")
            dinesh.execute(f"select State, sum(Registered_User) as total_users, sum(app_opens) as total_app_opens from map_user where year = {Year} and quarter = {Quarter} group by State order by total_users desc limit 10")
            df = pd.DataFrame(dinesh.fetchall(), columns=['State', 'total_users','total_app_opens'])
            fig = px.pie(df, values='total_users',
                             names='State',
                             title='Top 10 State Vs total_users',

                             color_discrete_sequence=px.colors.sequential.Agsunset)

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432,database='phonepe_project')
    dinesh = kumar.cursor()

    dinesh.execute("select * from aggregated_transaction;")
    kumar.commit()
    t1=dinesh.fetchall()
    aggregated_trans=pd.DataFrame(t1, columns=['state', 'year', 'quarter', 'transaction_type', 'transaction_count', 'transaction_amount'])





    dinesh.execute("select * from map_transaction;")
    kumar.commit()
    t3=dinesh.fetchall()
    map_trans=pd.DataFrame(t3, columns=['state', 'year', 'quarter', 'district', 'transaction_count', 'transaction_amount'])




    dinesh.execute("select * from top_transaction;")
    kumar.commit()
    t5=dinesh.fetchall()
    top_trans=pd.DataFrame(t5, columns=['state', 'year', 'quarter', 'pincode', 'trans_count', 'trans_amount'])



if SELECT== "Explore Data":
        st.subheader(":red[Explore Data]")
        Type = st.selectbox(":orange[select]", ("selectone","Transactions", "Users"," Data Visualization"))
        if Type == "Transactions":
            column1,column2= st.columns([1,1],gap="small")
            with column1:
                Year = st.slider(":orange[Year]:", min_value=2018, max_value=2022)
                st.write('- Year -  2018 to 2023')
                Quarter = st.slider(":orange[Quarter]:", min_value=1, max_value=4)
                st.write('- Quarter - Q1 (Jan to Mar), Q2 (Apr to June), Q3 (July to Sep), Q4 (Oct to Dec)')
            with  column2:

                kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432,database='phonepe_project')
                dinesh = kumar.cursor()
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data1 = json.loads(response.content)


                dinesh.execute(f"select state, sum(trans_amount) as total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(dinesh.fetchall(),columns= ['state', 'total_amount'])
                df2 = pd.read_csv(r'c:\Users\Lenovo\Downloads\Statenames.csv')
                df1['state'] = df2["state"]

                fig = px.choropleth(df1,geojson=  data1,
                            featureidkey='properties.ST_NM',
                            locations='state',
                            color='total_amount',
                            title="Allover_india_transaction_amount_statewise",
                            color_continuous_scale='aggrnyl')

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(width=400, height=400)
                fig.update_layout(title_font=dict(size=15), title_font_color='#1E8449',title_x=0.15)
                st.plotly_chart(fig,use_container_width=True)

                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data = json.loads(response.content)


                dinesh.execute(f"select State, sum(transaction_count) as total_transactions from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(dinesh.fetchall(),columns= ['state', 'total_transactions'])
                df2 = pd.read_csv(r'c:\Users\Lenovo\Downloads\Statenames.csv')
                df1['state']= df2["state"]

                fig = px.choropleth(df1,geojson=data,
                            featureidkey='properties.ST_NM',
                            locations='state',
                            color='total_transactions',
                            title="Allover_india_total_transaction_count_statewise",
                            color_continuous_scale='blues',
                            )

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(width=400, height=400)
                fig.update_layout(title_font=dict(size=15), title_font_color='#2E86C1',title_x=0.15)   
                st.plotly_chart(fig,use_container_width=True)
            with column1:
                st.subheader(":rainbow[Overall state district wise transactions_count ]")
                selected_state = st.selectbox(":red[select]",
                                    ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                    'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                    'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                    'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                    'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                    'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'))

                dinesh.execute(f"select State, District, year, quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District, Year, Quarter order by State, District")

                df1 = pd.DataFrame(dinesh.fetchall(), columns=['state','district','year','quarter',
                                                                'total_transactions','total_amount'])
                fig = px.bar(df1,
                            title=selected_state,
                            x="district",
                            y="total_transactions",
                            orientation='v',
                            color='total_amount',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig)

        if Type == "Users":
         coln1,coln2=st.columns([1,1],gap="small")
         with coln1:   
            Year = st.slider(":blue[Year]:", min_value=2018, max_value=2022)
            st.write('- Year -  2018 to 2023')
            Quarter = st.slider(":blue[Quarter]:", min_value=1, max_value=4)
            st.write('- Quarter - Q1 (Jan to Mar), Q2 (Apr to June), Q3 (July to Sep), Q4 (Oct to Dec)')
            kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432,database='phonepe_project')
            dinesh = kumar.cursor()       
         with coln2:
                st.subheader(":rainbow[Overall state district wise total_users ]")
                selected_state = st.selectbox(":red[select]",
                                    ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                    'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                    'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                    'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                    'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                    'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'))

                dinesh.execute(f"select state,year,quarter,district,sum(registered_user) as total_Users, sum(app_opens) as total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by state, district,year,quarter order by state,district")

                df = pd.DataFrame(dinesh.fetchall(), columns=['state','year', 'quarter', 'district', 'total_Users','total_Appopens'])
                fig = px.bar(df,
                            title=selected_state,
                            x="district",
                            y="total_Users",
                            orientation='v',
                            color='total_Users',
                            color_continuous_scale=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig) 
        kumar = psycopg2.connect(host='localhost', user='postgres', password='SQLpriya', port=5432, database='phonepe_project')
        dinesh = kumar.cursor()

        dinesh.execute("select * from top_user;")
        kumar.commit()
        table6=dinesh.fetchall()
        top_user=pd.DataFrame(table6, columns=['state', 'year', 'quarter', 'pincode', 'registered_users']) 

        dinesh.execute("select * from map_user;")
        kumar.commit()
        table4=dinesh.fetchall()
        map_user=pd.DataFrame(table4, columns=['state', 'year', 'quarter', 'district', 'registered_users', 'app_opens'])

        dinesh.execute("select * from aggregated_transaction;")
        kumar.commit()
        table1=dinesh.fetchall()
        aggregated_trans=pd.DataFrame(table1, columns=['state', 'year', 'quarter', 'transaction_type', 'transaction_count', 'transaction_amount'])

        dinesh.execute("select * from aggregated_user;")
        kumar.commit()
        table2=dinesh.fetchall()
        aggregated_user=pd.DataFrame(table2, columns=['state', 'year', 'quarter', 'brands', 'transaction_count', 'percentage'])

        dinesh.execute("select * from map_transaction;")
        kumar.commit()
        table3=dinesh.fetchall()
        map_trans=pd.DataFrame(table3, columns=['state', 'year', 'quarter', 'district', 'transaction_count', 'transaction_amount'])

        def number1(): 
                    din=top_user[['state','registered_users']]
                    ch1= din.groupby('state')['registered_users'].sum()
                    ch2=ch1.sort_values()
                    ch3=ch2.head(10)
                    ch4 = pd.DataFrame(ch3).reset_index()
                    fig= px.pie(ch4, values='registered_users', names='state',
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, title = 'lowest ten registred_users state ')
                    fig.update_layout(width=600, height=600)
                    fig.update_layout(title_font=dict(size=25), title_font_color='#5D9A96', title_x=0.1)
                    st.plotly_chart(fig) 
        def number2():
            m1=map_user[["state",'app_opens']]
            m2=m1.groupby('state')['app_opens'].sum()
            m3 = pd.DataFrame(m2).reset_index()
            m4=m3.sort_values(by='app_opens')
            m5=m4.tail(10)
            fig=px.pie(m5, names='state', values='app_opens',color_discrete_sequence=px.colors.sequential.speed, hole = 0.4, title= 'top 10 States wise AppOpens')
            fig.update_layout(width=600, height=600)
            fig.update_layout(title_font=dict(size=33), title_font_color='#C12EBA', title_x=0.2)
            st.plotly_chart(fig)

        def number3():
            agg1 = aggregated_trans[['state','transaction_count']]
            agg2 = agg1.groupby('state')['transaction_count'].sum()
            agg3 = agg2.sort_values()
            agg = agg3.tail(10)
            fig = px.bar(agg, x=agg.index, y='transaction_count', title = 'top 10 state with transaction_count',color='transaction_count')
            fig.update_layout(width=600, height=400)
            st.plotly_chart(fig) 

        def number4():
            agg1 = aggregated_trans[['transaction_type','transaction_count']]
            agg2 = agg1.groupby('transaction_type')['transaction_count'].sum()
            agg3 = agg2.sort_values()
            fig = px.bar(agg3, x=agg3.index, y='transaction_count', title = 'transaction_type vs transaction_count')
            fig.update_layout(width=600, height=400)
            fig.update_traces(marker_color = '#D35400' )
            st.plotly_chart(fig,use_container_width=False)

        def number5():
            agg1=aggregated_user[['brands','transaction_count']]
            brand1 =agg1.groupby('brands')['transaction_count'].sum()
            bt = pd.DataFrame(brand1).reset_index()
            best=bt.tail(10)
            fig= px.pie(best, values='transaction_count', names='brands',hole=0.3,
                        color_discrete_sequence=px.colors.sequential.Blugrn, title = 'Brands of moblies used')
            fig.update_layout(width=400, height=600)
            fig.update_layout(title_font=dict(size=30), title_font_color='#6AC12E' )
            st.plotly_chart(fig)

        def number6():
            m1 = map_trans[['district', 'transaction_amount']]
            m2 = m1.groupby('district')['transaction_amount'].sum()
            m3 = m2.sort_values()
            m4=m3.tail(10).reset_index()
            fig = px.histogram(m4, x='district', y='transaction_amount', color='transaction_amount', title = 'districts wise  ten highest transactions_amount',color_discrete_sequence=px.colors.sequential.solar)
            fig.update_layout(width=500, height=500)
            fig.update_layout(title_font=dict(size=20), title_font_color='#5499C7')
            st.plotly_chart(fig)



if Type==" Data Visualization":
            col1,col2=st.columns([1,1],gap="small")
            with col1:
             q=st.selectbox('**Select**', ('select one','Lowest ten registred_users state','Top 10 State wise app_opening','Top 10 state with transaction_count','Transaction type wise transaction count',\
                                            'Brand of mobiles used wies transaction count','District wise highest transaction_amount'))

            with col2: 
             if q=='Lowest ten registred_users state':
                number1()
             elif q=='Top 10 State wise app_opening':
                number2()
             elif q=='Top 10 state with transaction_count':
                number3()
             elif q=='Transaction type wise transaction count':
                number4()
             elif q=='Brand of mobiles used wies transaction count':
                number5()
             elif q=='District wise highest transaction_amount':
                number6()
