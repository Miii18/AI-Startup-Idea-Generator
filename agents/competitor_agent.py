from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Initialize the Gemini model with a temperature of 0.7
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def analyze_competitors(selected_idea):
    """
    Performs competitive analysis for the selected startup idea.
    
    Parameters:
    selected_idea (str): The specific startup concept.
    
    Returns:
    str: A concise competitive analysis report.
    """
    # 1. Define the PromptTemplate structure with rules for formatting, brevity, and layout
    template = """
    You are a competitive intelligence analyst.

    Analyze the startup idea:
    "{selected_idea}"

    Provide ONLY:
    1. Top 3 Competitors:
       - List 3 direct or indirect competitors.
       
    2. Market Gap:
       - What are these competitors missing?
       
    3. Business Opportunity:
       - How can this startup capitalize on that gap?

    Rules:
    - Keep the entire response under 80 words.
    - Use concise bullet points.
    """
    
    # 2. Instantiate the PromptTemplate class from LangChain
    prompt_template = PromptTemplate(
        input_variables=["selected_idea"],
        template=template
    )
    
    # 3. Format the template dynamically by inserting the user's selected idea
    formatted_prompt = prompt_template.format(selected_idea=selected_idea)
    
    # 4. Send the formatted prompt to the Gemini API via LangChain
    response = llm.invoke(formatted_prompt)
    
    # 5. Extract and return the generated content string from the response
    return response.content
