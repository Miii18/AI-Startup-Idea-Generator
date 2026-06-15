from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Initialize the Gemini model with a temperature setting of 0.7 for creative yet focused responses
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def analyze_market(selected_idea):
    """
    Analyzes the market for a selected startup idea.
    
    Parameters:
    selected_idea (str): The specific startup concept chosen by the user.
    
    Returns:
    str: A structured analysis text containing Target Audience, Market Demand, 
         Industry Trends, and Potential Customers.
    """
    # 1. Define the PromptTemplate structure for the market research analysis
    template = """
    You are a market research analyst.

    Analyze the startup idea:

    "{selected_idea}"

    Provide ONLY:

    1. Target Audience (max 4 lines)
    
    2. Market Demand (max 4 lines)
    
    3. Industry Trends (max 4 lines)
    
    4. Potential Customers (5 bullet points)

    Keep the entire response under 100 words.
    """ 
    
    # 2. Instantiate the PromptTemplate class from LangChain
    prompt_template = PromptTemplate(
        input_variables=["selected_idea"],
        template=template
    )
    
    # 3. Format the template dynamically by inserting the user's selected idea
    formatted_prompt = prompt_template.format(selected_idea=selected_idea)
    
    # 4. Send the formatted prompt to the Gemini API via the LangChain wrapper
    response = llm.invoke(formatted_prompt)
    
    # 5. Extract and return the generated text content from the model response
    return response.content
