def get_mock_ideas(domain):
    dom = domain.strip() or "Technology"
    return f"""1.  {dom} PathFinder
2.  Core{dom.replace(" ", "")} AI
3.  Flow{dom.replace(" ", "")} Assistant
4.  Smart{dom} Automation
5.  Nova{dom.replace(" ", "")} Ops"""

def get_mock_market(selected_idea):
    return f"""1. Target Audience (max 4 lines)
- Early adopters and professionals looking to automate tasks related to {selected_idea}.
- Small and medium businesses seeking to improve operational speed and eliminate manual tasks.

2. Market Demand (max 4 lines)
- High demand for niche, purpose-built tools that solve specific operational overhead.
- Decreases manual labor costs and reduces human errors.

3. Industry Trends (max 4 lines)
- Rising adoption of specialized, task-focused vertical solutions.
- Increased integration of web-based assistants into standard day-to-day work systems.

4. Potential Customers (5 bullet points)
* Freelancers and individual consultants
* Small-to-medium enterprise operations teams
* Corporate departmental managers
* Technology integration specialists
* Early-stage start-up founders"""

def get_mock_competitors(selected_idea):
    return f"""1. Top 3 Competitors:
* Large legacy industry suites (heavy, expensive, slow)
* Generic spreadsheet-based trackers (manual, high friction)
* Point-solution plugins (limited scale, poor integration)

2. Market Gap:
* Current platforms lack context-aware intelligence tailored to {selected_idea}, requiring manual configuration.

3. Business Opportunity:
* Deliver a pre-configured, verticalized tool that works out-of-the-box with minimal integration time."""

def get_mock_business(selected_idea):
    return f"""1. Revenue Model
* Monthly/Annual SaaS Subscription.

2. Pricing Strategy
* Freemium tier for individuals, $29/mo professional tier, custom seat-based pricing for enterprises.

3. Monetization Plan
* B2B subscriptions, premium template access, and paid API transaction credits.

4. Go-To-Market Strategy
* Inbound content marketing, listing on developer product directories, and warm outbound sales to team leads."""

def get_mock_pitch(selected_idea):
    return f"""1. Problem
* Legacy workflows are slow, manual, and prone to costly human errors.

2. Solution
* An automated, context-aware intelligence platform powered by {selected_idea}.

3. Value Proposition
* Cuts task completion time by 80% and eliminates configuration friction.

4. Elevator Pitch
* For teams struggling with manual overhead, {selected_idea} is the out-of-the-box solution that automates key operations instantly."""

