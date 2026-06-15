from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Initialize Gemini LLM with a temperature of 0.7
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def generate_pitch(startup_idea, market_analysis, competitor_analysis, business_model):
    """
    Generates a pitch deck summary for the selected startup idea based on previous agent reports.
    
    Parameters:
    startup_idea (str): Selected startup idea.
    market_analysis (str): Market research report.
    competitor_analysis (str): Competitor analysis report.
    business_model (str): Business and monetization report.
    
    Returns:
    str: A concise pitch summary.
    """
    # 1. Define the PromptTemplate containing four input placeholders
    template = """
    You are an experienced venture capitalist and pitch advisor.

    Formulate a startup pitch deck summary based on the following:
    - Startup Idea: {startup_idea}
    - Market Analysis: {market_analysis}
    - Competitor Analysis: {competitor_analysis}
    - Business Model: {business_model}

    Provide ONLY:
    1. Problem
    - What key problem is being solved?
    
    2. Solution
    - How does this startup solve that problem?
    
    3. Value Proposition
    - What is the unique value proposition?
    
    4. Elevator Pitch
    - A compelling 1-2 sentence pitch summarizing the company.

    Rules:
    - Keep response under 80 words.
    - Use short bullet points.
    - Be concise.
    """
    
    # 2. Instantiate PromptTemplate from LangChain
    prompt_template = PromptTemplate(
        input_variables=[
            "startup_idea",
            "market_analysis",
            "competitor_analysis",
            "business_model"
        ],
        template=template
    )
    
    # 3. Format the template dynamically with all four context blocks
    formatted_prompt = prompt_template.format(
        startup_idea=startup_idea,
        market_analysis=market_analysis,
        competitor_analysis=competitor_analysis,
        business_model=business_model
    )
    
    # 4. Invoke the model by sending the formatted prompt to the Gemini API
    response = llm.invoke(formatted_prompt)
    
    # 5. Extract and return the generated content string from the response
    return response.content
