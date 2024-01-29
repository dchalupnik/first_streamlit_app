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
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_list():
  with my_cnx.cursor() as myc_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if fruit_choice:
      streamlit.dataframe(get_fruitvice_data(fruit_choice))
  else:
      streamlit.error('Please select a fruit to get information')
except URLError as e:
  streamlit.error()

streamlit.header("The fruit list contains:")
if streamlit.button('Get Fruit Load List'):
    streamlit.dataframe(get_fruit_list())




fruit_to_add  = streamlit.text_input('What fruit would you like to add?')
try:
  if fruit_to_add:
    with my_cnx.cursor() as myc_cur:
      my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values('{fruit_to_add}')")
except snowflake.connector.errors.ProgrammingError:
  pass
