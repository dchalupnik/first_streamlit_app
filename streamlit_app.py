import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')


streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Bllueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocker Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show )

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('Please select a fruit to get information')
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      streamlit.write(fruityvice_response.status_code)
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
    
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_rows)

fruit_to_add  = streamlit.text_input('What fruit would you like to add?')
try:
  if fruit_to_add:
    my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values('{fruit_to_add}')")
except snowflake.connector.errors.ProgrammingError:
  pass
