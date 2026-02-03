from autogen import AssistantAgent,UserProxyAgent,config_list_from_json

#Import openapi key
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

assistant = AssistantAgent(name="assistant",llm_config={"config_list":config_list})

user_proxy = UserProxyAgent(name="user_proxy",code_execution_config={"work_dir":"coding"})


user_proxy.initiate_chat(assistant,message="use streamlit to create stock pricing app that contain NVDA AAPL TSLA stock pricing and trading volume")