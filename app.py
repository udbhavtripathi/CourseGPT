

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import concurrent.futures
# from course_maker import course_maker
from helper_functions.course_maker_multi import course_maker
from dotenv import load_dotenv
from helper_functions.course_JSON import course_save_JSON
import json

load_dotenv()

# Define custom CSS styles
main_bg_color = "#f8f9fa"
main_text_color = "#1c6dad"
header_bg_color = "#1c6dad"
header_text_color = "#ffffff"
button_bg_color = "#1c6dad"
button_text_color = "#ffffff"

# Apply custom styles
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {main_bg_color};
        color: {main_text_color};
    }}
    .css-1aumxhk {{
        background-color: {header_bg_color} !important;
    }}
    .css-1aumxhk > h1 {{
        color: {header_text_color};
    }}
    .stButton button {{
        background-color: {button_bg_color} !important;
        color: {button_text_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Course Maker App")
    #1
    topic_name = st.text_input("Enter the topic name:")
    #2
    num_days = st.number_input("In how many days you wish to complete the course", step=1)
    #3
    application = st.text_input("Which field do you wish the apply the learnings from this course")
    
    #4
    level_options = ['Beginner', 'Intermediate', 'Advanced']
    level_dropdown = st.selectbox('Level of course', level_options)
    print("level_dropdown", level_dropdown)
    if st.button("Generate Course"):
        with st.spinner("Generating course..."):
            module_output, subtopic_outputs_list, contents_output_list, *module_points = course_maker(

                topic_name, num_days, application, level_dropdown)
            
            course_full_v2 = course_save_JSON(module_output, subtopic_outputs_list, contents_output_list, *module_points)
        
            #save json data
            with open("course_full_v2.json", "w") as file:
                file.write(course_full_v2)

            
            # read in json format
            with open("course_full_v2.json") as json_file:
                course_data = json.load(json_file)

        
        # Iterate through the nested dictionaries
            for module_number, subtopics in course_data.items():
                for subtopic_data in subtopics:
                    module_heading = subtopic_data["Module_heading"]
                    subtopic_output = subtopic_data["subtopic_output"]
                    content_output = subtopic_data["content_output"]
                    
                    st.write(f"**Module Number:** {module_number}")
                    st.write(f"**Module Heading:** {module_heading}")
                    st.write(f"**Subtopic:** {subtopic_output}")
                    st.write(f"Content: {content_output}")
                    st.write("\n")




if __name__ == "__main__":
    main()



