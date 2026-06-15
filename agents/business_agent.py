from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def generate_business_model(startup_idea, market_analysis, competitor_analysis):
    """
    Generates a business model for the selected startup idea.

    Parameters:
    startup_idea (str): Selected startup idea
    market_analysis (str): Market research report
    competitor_analysis (str): Competitor analysis report

    Returns:
    str: Business model report
    """

    template = """
    You are a startup business strategist.

    Startup Idea:
    {startup_idea}

    Market Analysis:
    {market_analysis}

    Competitor Analysis:
    {competitor_analysis}

    Provide ONLY:

    1. Revenue Model
    - How will the startup make money?

    2. Pricing Strategy
    - Suggested pricing model

    3. Monetization Plan
    - Key revenue channels

    4. Go-To-Market Strategy
    - How to acquire first customers

    Rules:
    - Keep response under 100 words
    - Use short bullet points
    - Be concise
    """

    prompt_template = PromptTemplate(
        input_variables=[
            "startup_idea",
            "market_analysis",
            "competitor_analysis"
        ],
        template=template
    )

    formatted_prompt = prompt_template.format(
        startup_idea=startup_idea,
        market_analysis=market_analysis,
        competitor_analysis=competitor_analysis
    )

    response = llm.invoke(formatted_prompt)

    return response.content