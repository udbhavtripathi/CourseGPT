

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
import os
import pickle as pk


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
        text-align: center;
        margin-bottom: 1rem;
    }}
    .stButton button {{
        background-color: {button_bg_color} !important;
        color: {button_text_color} !important;
        margin-top: 1rem;
    }}
    .output {{
        margin-top: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Course GPT")
    st.write("Create a personalized mini-course based on your particular application")

    # load_dotenv()

    # # Get user input for the API key
    # api_key = st.text_input("Enter your API key:")

    # # Update the .env file with the provided API key
    # if api_key:
    #     with open('.env', 'w') as env_file:
    #         env_file.write(f'OPENAI_API_KEY={api_key}\n')
    #     st.success("Success")

    # # Reload environment variables after updating .env file
    # load_dotenv()

    # # Access the API key using os.getenv("API_KEY")
    # api_key_from_env = os.getenv("OPENAI_API_KEY")




    # Get user input for the API key
    api_key = st.text_input("Enter your API key:")

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API key set successfully")




    #1
    topic_name = st.text_input("Enter the topic name:")
    #2
    num_modules = st.number_input("Enter number of modules you want to generate:", step =1)
    #3
    num_subtopics = st.number_input("Enter number of chapters you want to generate in each module:", step=1)
    #4
    application = st.text_input("Which application of the course you are partcularly interested in?")
    #5
    level_options = ['Beginner', 'Intermediate', 'Advanced']
    level_dropdown = st.selectbox('Level of course', level_options)
  


    if st.button("Generate Course"):
        with st.spinner("Generating course..."):

            retry = True
            while retry == True:
                try:
                    module_output, subtopic_outputs_list, contents_output_list, *module_points = course_maker(
                        topic_name, application, num_modules,level_dropdown,num_subtopics)
                    
                    
                    # check if the number of modules created is correct
                    if len(module_points) != num_modules:
                        retry = True
                        continue
                    
                    
                    # save course contents
                    course_full_v2 = course_save_JSON(module_output, subtopic_outputs_list, contents_output_list, *module_points)
        
                    
                    retry = False  # Break out of the loop if no index error occurs
                    break
                except IndexError as e:
                    # If an index error occurs, retry by continuing the loop
                    pass
                except pickle.PicklingError as e:
                    pass

            
            
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
                    
                    # st.write(f"**Module Number:** {module_number}")
                    st.write(f"**Module Heading:** {module_heading}")
                    st.write(f"**Subtopic:** {subtopic_output}")
                    st.write(f"Content: {content_output}")
                    st.write("\n")



if __name__ == "__main__":
    main()


