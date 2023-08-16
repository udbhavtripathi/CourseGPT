import json

def course_save_JSON(module_output, subtopic_outputs_list, contents_output_list, *module_points):

    # Create a dictionary to store the data
    course_data = {}

    for i, module in enumerate(module_points):
        # Store module output
        module_output = module

        # Get corresponding subtopics
        subtopics = subtopic_outputs_list[i].split('\n')

        module_data = []
        for j, subtopic in enumerate(subtopics):
            # Store subtopic output
            subtopic_output = subtopic

            # Get corresponding content 
            content_output = contents_output_list[i*len(subtopics) + j]
    


            # Create a dictionary for subtopic and content and scripts
            subtopic_data = {
                "Module_heading": module_output,
                "subtopic_output": subtopic_output,
                "content_output": content_output,
               
            }

            # Append subtopic data to module data
            module_data.append(subtopic_data)

        # Add module data to course_data
        course_data[i + 1] = module_data 

            # Save the data as JSON
        json_data = json.dumps(course_data, indent=4)

    

    return json_data

