#Coursify is a personal project that creates a prompted chatbot that outputs information on Georgia Tech Computer Science courses.
#The inspiration for this project came from the tutorial off DeepLearning.AI which helped figure out the project's components and create a
#spinoff for a computer science course chatbot specific to my college, Georgia Tech.
import os
import openai
import tiktoken
import json 
#openai.api_key  = "OPENAI API KEY"

#completion method to declare the model's attrbutes such as temperature and token
def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]

#instructions on what the chatbot's purpose is and how to split off topics
delimiter = "####"
system_message = f"""
You will be provided with Georgia Tech computer science course queries. 
The course query will be delimited with 
{delimiter} characters.
Output a python list of objects, where each object has 
the following format:
    'Language': <one of Java, 
    C and Assembly, 
    Python, 
    MySQL, 
    HTML and CSS>,
OR
    'courses': <a list of courses that must 
    be found in the allowed courses below>

Where the languages and courses must be found in 
the course query.
If a course is mentioned, it must be associated with 
the correct language in the allowed courses list below.
If no courses or languages are found, output an 
empty list.

Allowed courses: 

Java:
CS 1331
CS 1332

C and Assembly:
CS 2110
CS 2200

Python:
CS 1301

MySQL:
CS 4400

HTML and CSS:
CS 1301

Only output the list of objects, with nothing else.
"""
user_message_1 = f"""
 tell me about the CS 2110 and CS 1331 courses """
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message_1}{delimiter}"},  
] 
firstResponse = get_completion_from_messages(messages)
#print(firstResponse)


# course information that was personally fed into the model
courses = {
    "CS 1331": {
        "course number": "CS 1331",
        "language": "Java",
        "name": "Intro to Object Oriented Programming",
        "credits": "3",
        "lab": "no lab",
    },
    "CS 1332": {
        "course number": "CS 1332",
        "language": "Java",
        "name": "Data Structures & Algorithms",
        "credits": "3",
        "lab": "no lab",
    },
    "CS 2110": {
        "course number": "CS 2110",
        "language": "C and Assembly",
        "name": "Computer Organization & Programming",
        "credits": "4",
        "lab": "yes",
    },
    "CS 2200": {
        "course number": "CS 2200",
        "language": "C and Assembly",
        "name": "Computer Systems and Networks",
        "credits": "4",
        "lab": "yes",
    },
    "CS 1301": {
        "course number": "CS 1301",
        "language": "Python",
        "name": "Introduction to Computing",
        "credits": "3",
        "lab": "no lab",
    },
    "CS 4400": {
        "course number": "CS 4400",
        "language": "MySQL",
        "name": "Introduction to Database Systems",
        "credits": "3",
        "lab": "no lab",
    }
}


#helper methods
def courseName (name):
    return courses.get(name, None)

def coursesByLanguage (language):
    return [course for course in courses.values() if course["language"] == language]


#print(courseName("CS 1331"))
#print(coursesByLanguage("C and Assembly"))
#print(user_message_1)
#print(firstResponse)

#turns the output into JSON format
def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None   
    

courseLanguageList = read_string_to_list(firstResponse)
#print(courseLanguageList)

#generates the output string 
def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "courses" in data:
                courseList = data["courses"]
                for name in courseList:
                    course = courseName(name)
                    if course:
                        output_string += json.dumps(course, indent=4) + "\n"
                    else:
                        print(f"Error: Course '{name}' not found")
            elif "language" in data:
                languageName = data["language"]
                language_courses = coursesByLanguage(languageName)
                for course in language_courses:
                    output_string += json.dumps(course, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string 

courseInfo = generate_output_string(courseLanguageList)
#print(courseInfo)

#chatbot prompting and inquiring
system_message = f"""
You are a computer catalog assistant for 
Georgia Tech computer science courses. 
Respond in a friendly and helpful tone, 
with very concise answers. 
Make sure to ask the user relevant follow up questions.
"""
#user inquiry
user_message_1 = f"""
tell me about the CS 2110 and CS 1331 courses."""
messages =  [  
{'role':'system',
 'content': system_message},   
{'role':'user',
 'content': user_message_1},  
{'role':'assistant',
 'content': f"""Relevant course information:\n\
 {courseInfo}"""},   
]
final_response = get_completion_from_messages(messages)
print(final_response)