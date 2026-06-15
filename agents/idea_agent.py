from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

def generate_startup_idea(domain):

    prompt = f"""
    You are a startup idea generator.

    Generate 5 innovative startup ideas.

    Rules:
    - Return exactly 5 ideas
    - Number them from 1 to 5
    - No explanations
    - Only startup names
    - Maximum 10 words

    Domain:
    {domain}
    """

    response = llm.invoke(prompt)

    return response.content