from dotenv import load_dotenv
import time
import re

load_dotenv()

from agents.idea_agent import generate_startup_idea
from agents.market_agent import analyze_market
from agents.competitor_agent import analyze_competitors
from agents.business_agent import generate_business_model
from agents.pitch_agent import generate_pitch
from agents.fallback import get_mock_ideas, get_mock_market, get_mock_competitors, get_mock_business, get_mock_pitch

# Global flag to track if we should run in demo/mock mode
demo_mode = False

def invoke_with_retry(func, *args, **kwargs):
    """
    Invokes the specified LLM agent function, automatically retrying 
    if a rate limit (HTTP 429 / ResourceExhausted) error is encountered.
    """
    max_attempts = 4
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            is_rate_limit = any(term in error_msg.lower() for term in [
                "429", "resourceexhausted", "resource_exhausted", "exhausted", "quota", "rate limit", "limit exceeded"
            ])
            if is_rate_limit and attempt < max_attempts - 1:
                # Default delay to wait is 32 seconds
                delay = 32
                # Attempt to extract the dynamic retry delay from the Google API error message
                delay_match = re.search(r"retryDelay':\s*'(\d+)s?'", error_msg)
                if delay_match:
                    delay = int(delay_match.group(1)) + 1
                
                print(f"\n[WARNING] API Rate Limit Hit. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                raise e

print("=" * 50)
print("     AI Startup Idea Generator")
print("=" * 50)

# Step 1: Get startup domain
domain = input("\nEnter startup domain: ")

# Step 2: Generate startup ideas
try:
    ideas = invoke_with_retry(generate_startup_idea, domain)
except Exception as e:
    print("\n[WARNING] Gemini API is fully exhausted or rate-limited. Activating local demo mode...")
    demo_mode = True
    ideas = get_mock_ideas(domain)

print("\nGenerated Startup Ideas:\n")
print(ideas)

# Step 3: Convert ideas into a list
idea_list = ideas.split("\n")

clean_ideas = []
for idea in idea_list:
    idea_stripped = idea.strip()
    if idea_stripped:
        # Match lines starting with numbers (e.g. 1. or 1)) or bullets (e.g. - or *)
        if re.match(r"^\d+[\.\)]", idea_stripped) or re.match(r"^[-*]\s+", idea_stripped):
            clean_ideas.append(idea_stripped)
# Fallback: if no structured lists found, capture any non-empty lines
if not clean_ideas:
    clean_ideas = [line.strip() for line in idea_list if line.strip()]

# Prevent hanging if no ideas were returned/parsed
if not clean_ideas:
    print("\n[ERROR] Error: No ideas could be generated or parsed. Please verify your API Key and connection.")
    exit(1)

# Step 4: User selects idea
while True:
    try:
        choice = int(input(f"\nSelect an idea number (1-{len(clean_ideas)}): "))

        if 1 <= choice <= len(clean_ideas):
            break

        print(f"Please enter a valid number between 1 and {len(clean_ideas)}.")

    except ValueError:
        print("Please enter numbers only.")

# Step 5: Extract selected idea and clean leading numbering/bullets
selected_idea = clean_ideas[choice - 1]
# Strip leading digit lists (e.g., "1. Idea" -> "Idea", "1) Idea" -> "Idea")
selected_idea = re.sub(r"^\d+[\.\)]\s*", "", selected_idea)
# Strip leading bullets (e.g., "- Idea" -> "Idea")
selected_idea = re.sub(r"^[-*]\s*", "", selected_idea)
selected_idea = selected_idea.strip()

print("\n" + "=" * 50)
print("SELECTED STARTUP IDEA")
print("=" * 50)
print(selected_idea)

# Step 6: Market Analysis
print("\n" + "=" * 50)
print("MARKET ANALYSIS")
print("=" * 50)

if demo_mode:
    market_report = get_mock_market(selected_idea)
else:
    try:
        # Add a tiny proactive sleep to avoid hitting rate limits too quickly
        time.sleep(2)
        market_report = invoke_with_retry(analyze_market, selected_idea)
    except Exception:
        print("\n[WARNING] API Rate Limit exceeded. Switching to local demo mode...")
        demo_mode = True
        market_report = get_mock_market(selected_idea)

print(market_report)

# Step 7: Competitor Analysis
print("\n" + "=" * 50)
print("COMPETITOR ANALYSIS")
print("=" * 50)

if demo_mode:
    competitor_report = get_mock_competitors(selected_idea)
else:
    try:
        # Add a tiny proactive sleep to avoid hitting rate limits too quickly
        time.sleep(2)
        competitor_report = invoke_with_retry(analyze_competitors, selected_idea)
    except Exception:
        print("\n[WARNING] API Rate Limit exceeded. Switching to local demo mode...")
        demo_mode = True
        competitor_report = get_mock_competitors(selected_idea)

print(competitor_report)

# Step 8: Business Model
print("\n" + "=" * 50)
print("BUSINESS MODEL")
print("=" * 50)

if demo_mode:
    business_report = get_mock_business(selected_idea)
else:
    try:
        # Add a tiny proactive sleep to avoid hitting rate limits too quickly
        time.sleep(2)
        business_report = invoke_with_retry(
            generate_business_model,
            selected_idea,
            market_report,
            competitor_report
        )
    except Exception:
        print("\n[WARNING] API Rate Limit exceeded. Switching to local demo mode...")
        demo_mode = True
        business_report = get_mock_business(selected_idea)

print(business_report)

# Step 9: Pitch Deck
print("\n" + "=" * 50)
print("PITCH DECK")
print("=" * 50)

if demo_mode:
    pitch_report = get_mock_pitch(selected_idea)
else:
    try:
        # Add a tiny proactive sleep to avoid hitting rate limits too quickly
        time.sleep(2)
        pitch_report = invoke_with_retry(
            generate_pitch,
            selected_idea,
            market_report,
            competitor_report,
            business_report
        )
    except Exception:
        print("\n[WARNING] API Rate Limit exceeded. Switching to local demo mode...")
        demo_mode = True
        pitch_report = get_mock_pitch(selected_idea)

print(pitch_report)

print("\n" + "=" * 50)
print("REPORT GENERATED SUCCESSFULLY")
print("=" * 50)