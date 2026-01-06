"""
This is an example of how to use LangChain with OpenAI.

To run this code, you will need to install the following packages:
pip install langchain langchain-openai
"""

import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# It is recommended to set your OpenAI API key as an environment variable.
# You can also pass it directly to the OpenAI constructor: OpenAI(openai_api_key="YOUR_API_KEY")
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

try:
    # Make sure the OPENAI_API_KEY environment variable is set.
    api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    print("Error: The OPENAI_API_KEY environment variable is not set.")
    print("Please set it to your OpenAI API key.")
    exit()

# 1. Initialize the LLM
# By default, it uses the "davinci-002" model. You can choose others.
# For example, to use "gpt-3.5-turbo", you would need to use ChatOpenAI instead.
llm = OpenAI(temperature=0.9)

# 2. Create a Prompt Template
# The template will be filled with the variable 'product'
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

# 3. Create a Chain
# The chain links the LLM and the prompt.
chain = LLMChain(llm=llm, prompt=prompt)

# 4. Run the Chain
# We pass the input variable 'product' to the chain.
product_idea = "colorful socks"
response = chain.invoke(product_idea)

print(f"Product Idea: {product_idea}")
print(f"Suggested Company Name: {response['text'].strip()}")

# --- Example with a different input ---
product_idea_2 = "home-baked cookies"
response_2 = chain.invoke(product_idea_2)

print(f"\nProduct Idea: {product_idea_2}")
print(f"Suggested Company Name: {response_2['text'].strip()}")
