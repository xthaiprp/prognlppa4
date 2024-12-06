import pandas as pd
import streamlit as st
import openai
import json

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = '''You are given a role as a Japanese high school teacher teaching students in the given JLPT level. 
            You will have to choose words that are suitable for students in the given JLPT level from the given text. 
            List the words in a JSON array with the following fields beginning with **.

            **Words - words in their original form followed by their pronunciation in ONLY kana characters in parentheses.
            **Part of Speech - part of speeches of the words in [Noun, Pronoun, Verb, Adjective, Adverb].
            **Translation - the appropriate translation of the words in English.
            **JLPT - JLPT level of the words in the given JLPT level.
            **Example sentence - usage of the words in a Japanese sentence followed by the English translation in parentheses.

            Do not say anything until you are given the text. Show the array at once without any opening or closing texts.
            '''

st.title(":red[JLPT N5-N1] From Text :jp:")

jlpt_explanation = """JLPT, or the Japanese-Language Proficiency Test, 
                    is a Japanese language proficiency exam for students who learn Japanese as a foreign language.
                    There are 5 levels of proficiency that exam takers can attain. 
                    \nRanking from the easiest to the hardest, the levels include: 
                    \n[:red[JLPT N5], :orange[JLPT N4], :green[JLPT N3], :blue[JLPT N2], and :violet[JLPT N1]]
                    """

with st.expander('What is JLPT? (click to see explanation)'):
    st.write(jlpt_explanation)

st.divider()

jlpt_level = st.select_slider("What level are you studying for?", options=["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"])

st.divider()

st.markdown('To make your studying even more _interesting_, type in a Japanese text into the box down below to receive a list of vocabs that is suitable (or challenging) for your studying level.')

user_input = st.text_area("Enter a Japanese text down below:", "Your text here")

if st.button("Submit", type='primary'):
    messages_so_far = [
        {"role": "user", "content": jlpt_level},
        {"role": "system", "content": prompt}, 
        {"role": "user", "content": user_input}
        ]
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
    word_list = response.choices[0].message.content
    
    json_dict = json.loads(word_list)
    final_dataframe = pd.DataFrame.from_dict(json_dict)
    st.table(final_dataframe)
