
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import concurrent.futures
import multiprocessing

def generate_subtopics(subtopic_chain, level_dropdown,module):
    return subtopic_chain.predict(module=module, level_dropdown=level_dropdown)

def generate_contents_and_scripts(content_chain, subtopic,level_dropdown,num_days):
    content_output = content_chain.predict(subtopic=subtopic, num_days=num_days, level_dropdown=level_dropdown)

    return content_output

def course_maker(topic_name, num_days, application, level_dropdown):
    llm = ChatOpenAI(temperature=0.9, request_timeout=300)

    module_prompt = PromptTemplate(
        input_variables=["topic", "application"],
        template="Give me the heading of 2 module names for the course in {topic}. The learner wants to apply the learning in {application}. Please don't write any description; I only want the headings.",
    )

    module_chain = LLMChain(llm=llm, prompt=module_prompt)

    module_output = module_chain.predict(topic=topic_name, application=application)

    module_points = module_output.split('\n')
    print("Modules created:", module_points)

    subtopic_prompt = PromptTemplate(
        input_variables=["module", "level_dropdown"],
        template="Give me the heading of 2 subtopics to teach in {module}. The course should be of {level_dropdown} level so give me the subtopics keeping in mind the same",
    )

    subtopic_chain = LLMChain(llm=llm, prompt=subtopic_prompt)

    subtopic_outputs_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_subtopics, subtopic_chain,  level_dropdown,module) for module in module_points]
        for future in concurrent.futures.as_completed(futures):
            subtopic_output = future.result()
            subtopic_outputs_list.append(subtopic_output)

    print("Subtopics created:", subtopic_outputs_list)

    content_prompt = PromptTemplate(
        input_variables=["subtopic", "num_days", "level_dropdown"],
        template="Give me a detailed description of this {subtopic}. The contents should be {num_days} long. The level of contents should be {level_dropdown}. Write in bulleted form and make sure to use examples as well.",
    )


    content_chain = LLMChain(llm=llm, prompt=content_prompt)


    contents_output_list = []


    with multiprocessing.Pool() as pool:
        results = []
        for subtopics in subtopic_outputs_list:
            subtopic_points = subtopics.split('\n')
            for subtopic in subtopic_points:
                results.append(pool.apply_async(generate_contents_and_scripts, (content_chain, subtopic,level_dropdown,num_days)))
        
        for result in results:
            content_output = result.get()
            contents_output_list.append(content_output)
 



    return module_output, subtopic_outputs_list, contents_output_list, *module_points
