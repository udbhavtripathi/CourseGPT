
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import concurrent.futures
import multiprocessing

# def generate_subtopics(subtopic_chain, level_dropdown,module,num_subtopics ):
#     return subtopic_chain.predict(module=module, level_dropdown=level_dropdown, num_subtopics = num_subtopics)

# def generate_contents_and_scripts(content_chain, subtopic,level_dropdown):
#     content_output = content_chain.predict(subtopic=subtopic, level_dropdown=level_dropdown)

#     return content_output

# def course_maker(topic_name, application,num_modules, level_dropdown,num_subtopics):
#     # llm = ChatOpenAI(temperature=0.9, request_timeout=300)
#     llm = OpenAI(model_name = "gpt-3.5-turbo")

#     module_prompt = PromptTemplate(
#         input_variables=["topic", "application","num_modules",],
#         template="Give me the heading of {num_modules} module names for the course in {topic}. The learner wants to apply the learning in {application}. Please don't write any description; I only want the headings.",
#     )

#     module_chain = LLMChain(llm=llm, prompt=module_prompt)

#     module_output = module_chain.predict(topic=topic_name, application=application,num_modules = num_modules)

#     module_points = module_output.split('\n')
#     print("Modules created:", module_points)

    
    
#     subtopic_prompt = PromptTemplate(
#     input_variables=["module", "level_dropdown", "num_subtopics"],
#     template="Give me the heading of {num_subtopics} subtopic(s) to teach in the '{module}' module. The course should be of {level_dropdown} level, so provide the subtopics accordingly.",)


#     subtopic_chain = LLMChain(llm=llm, prompt=subtopic_prompt)

#     subtopic_outputs_list = []
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(generate_subtopics, subtopic_chain,  level_dropdown,module,num_subtopics) for module in module_points]
#         for future in concurrent.futures.as_completed(futures):
#             subtopic_output = future.result()
#             subtopic_outputs_list.append(subtopic_output)

#     print("Subtopics created:", subtopic_outputs_list)

#     content_prompt = PromptTemplate(
#         input_variables=["subtopic", "level_dropdown"],
#         template="Give me a detailed description of this {subtopic}. The level of contents should be {level_dropdown}. Write in essay form with detailed description of the topics and make sure to use examples as well.",
#     )


#     content_chain = LLMChain(llm=llm, prompt=content_prompt)


#     contents_output_list = []


#     with multiprocessing.Pool() as pool:
#         results = []
#         for subtopics in subtopic_outputs_list:
#             subtopic_points = subtopics.split('\n')
#             for subtopic in subtopic_points:
#                 results.append(pool.apply_async(generate_contents_and_scripts, (content_chain, subtopic,level_dropdown)))
        
#         for result in results:
#             content_output = result.get()
#             contents_output_list.append(content_output)
 



#     return module_output, subtopic_outputs_list, contents_output_list, *module_points























def generate_subtopics(subtopic_chain, level_dropdown,module,num_subtopics ):
    return subtopic_chain.predict(module=module, level_dropdown=level_dropdown, num_subtopics = num_subtopics)

def generate_contents_and_scripts(content_chain, subtopic,level_dropdown):
    content_output = content_chain.predict(subtopic=subtopic, level_dropdown=level_dropdown)

    return content_output

def course_maker(topic_name, application,num_modules, level_dropdown,num_subtopics):
    llm = ChatOpenAI(temperature=0.9, request_timeout=300)
    # llm = OpenAI(model_name = "gpt-3.5-turbo")

    module_prompt = PromptTemplate(
        input_variables=["topic", "application", "num_modules"],
        template="You're structuring a course on '{topic}' with an emphasis on its application in '{application}'. Please provide {num_modules} module name(s) that would be suitable for this course. Remember to give {num_modules} headings without any detailed descriptions, while keeping in mind the specified number of modules.")


    module_chain = LLMChain(llm=llm, prompt=module_prompt)

    module_output = module_chain.predict(topic=topic_name, application=application,num_modules = num_modules)

    module_points = module_output.split('\n')
    print("Modules created:", module_points)

    
    
    subtopic_prompt = PromptTemplate(
    input_variables=["module", "level_dropdown", "num_subtopics"],
    template="You are creating a course module on '{module}' at the '{level_dropdown}' level. Please provide {num_subtopics} subtopics that you would include in this module. Make sure to give concise and relevant headings for each subtopic, focusing on the specified number of {num_subtopics} subtopics only. Avoid exceeding the requested number.")


    subtopic_chain = LLMChain(llm=llm, prompt=subtopic_prompt)

    subtopic_outputs_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_subtopics, subtopic_chain,  level_dropdown,module,num_subtopics) for module in module_points]
        for future in concurrent.futures.as_completed(futures):
            subtopic_output = future.result()
            subtopic_outputs_list.append(subtopic_output)

    print("Subtopics created:", subtopic_outputs_list)

    content_prompt = PromptTemplate(
        input_variables=["subtopic", "level_dropdown"],
        template="You're developing content for the '{subtopic}' section, aimed at the '{level_dropdown}' level. Write a comprehensive essay-style description of this subtopic, ensuring a deep exploration of the subject. Incorporate illustrative examples to enhance understanding.")


    content_chain = LLMChain(llm=llm, prompt=content_prompt)


    contents_output_list = []


    with multiprocessing.Pool() as pool:
        results = []
        for subtopics in subtopic_outputs_list:
            subtopic_points = subtopics.split('\n')
            for subtopic in subtopic_points:
                results.append(pool.apply_async(generate_contents_and_scripts, (content_chain, subtopic,level_dropdown)))
        
        for result in results:
            content_output = result.get()
            contents_output_list.append(content_output)
 



    return module_output, subtopic_outputs_list, contents_output_list, *module_points
