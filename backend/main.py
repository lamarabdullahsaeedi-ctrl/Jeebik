from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from datetime import date



from dotenv import load_dotenv

from google import genai



import calendar

import math

import os

import json

import re





# ============================================================

# ENVIRONMENT

# ============================================================



load_dotenv()



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



client = None



if GEMINI_API_KEY:

    client = genai.Client(api_key=GEMINI_API_KEY)





# ============================================================

# APP

# ============================================================



app = FastAPI(

    title="JEEBIK API",

    description=(

        "Backend API for JEEBIK financial planning "

        "with an AI agent layer"

    ),

    version="2.2.0"

)





# ============================================================

# CORS

# ============================================================



app.add_middleware(

    CORSMiddleware,

    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://jeebik.onrender.com"
],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)





# ============================================================

# REQUEST MODELS

# ============================================================



class PlanRequest(BaseModel):

    goal_name: str

    goal_price: float



    # Demo user financial profile

    balance: float = 10000

    monthly_income: float = 15000

    monthly_spending: float = 4000

    monthly_commitments: float = 3000



    # Existing goal

    other_goal_name: str = "Mauritius Trip"

    other_goal_amount: float = 8000

    other_goal_target_year: int = 2027

    other_goal_target_month: int = 7





class TransactionItem(BaseModel):

    name: str

    amount: float

    date: str

    category: str = "Other"

    type: str = "expense"



class CommitmentDetectionRequest(BaseModel):

    transactions: list[TransactionItem]



class ReplanRequest(BaseModel):

    # Active goal

    goal_name: str

    previous_price: float

    new_price: float



    # Current active JEEBIK plan

    current_progress_amount: float

    current_monthly_allocation: float

    current_target_month: str

    current_target_year: int



    # User financial context

    balance: float = 10000

    monthly_income: float = 15000

    monthly_spending: float = 4000

    monthly_commitments: float = 3000



    # Existing goal that must remain protected

    other_goal_name: str = "Mauritius Trip"

    other_goal_amount: float = 8000

    other_goal_target_year: int = 2027

    other_goal_target_month: int = 7





# ============================================================

# HELPER FUNCTIONS

# ============================================================



def add_months(start_date: date, months: int):

    month_index = start_date.month - 1 + months



    year = (

        start_date.year

        + month_index // 12

    )



    month = (

        month_index % 12

        + 1

    )



    return year, month





def month_name(month_number: int):

    return calendar.month_name[month_number]





def month_number(month_text: str):

    clean_month = month_text.strip().lower()



    for number in range(1, 13):

        if calendar.month_name[number].lower() == clean_month:

            return number



    raise ValueError(

        f"Invalid month name: {month_text}"

    )





def months_until(

    current_year: int,

    current_month: int,

    target_year: int,

    target_month: int

):

    months = (

        (target_year - current_year) * 12

        + (target_month - current_month)

    )



    return max(months, 1)





def round_up_to_50(amount: float):

    if amount <= 0:

        return 0



    return math.ceil(amount / 50) * 50





def calculate_existing_goal_monthly(

    today: date,

    amount: float,

    target_year: int,

    target_month: int

):

    months_left = months_until(

        today.year,

        today.month,

        target_year,

        target_month

    )



    required_monthly = (

        amount

        / months_left

    )



    required_monthly = round_up_to_50(

        required_monthly

    )



    return months_left, required_monthly





def calculate_available_for_planning(

    monthly_income: float,

    monthly_spending: float,

    monthly_commitments: float,

    existing_goal_monthly: float

):

    available = (

        monthly_income

        - monthly_spending

        - monthly_commitments

        - existing_goal_monthly

    )



    return max(available, 0)





# ============================================================

# INITIAL PLANNING AI AGENT

# ============================================================



def run_initial_planning_ai_agent(

    plan: PlanRequest,

    required_other_goal_monthly: float,

    available_for_planning: float,

    recommended_purchase: str,

    recommended_year,

    months_needed,

    monthly_allocation: float,

    safe_to_spend: float,

    goal_status: str

):

    """

    JEEBIK Initial Planning AI Agent.



    The AI understands the user's financial context and interprets

    the validated financial plan.



    The deterministic Financial Planning Engine remains responsible

    for all exact financial calculations and validation.



    Flow:



    User Financial Context

        -> AI understands context

        -> Financial Planning Engine calculates and validates

        -> AI interprets and personalizes

        -> User receives the recommended plan

    """



    if months_needed is None:

        fallback_message = (

            f"JEEBIK analyzed your income, average spending, "

            f"commitments, balance, and your existing "

            f"{plan.other_goal_name} goal. Based on the validated "

            f"financial calculation, there is currently no available "

            f"monthly capacity for {plan.goal_name} without adjusting "

            f"the current financial plan."

        )

    else:

        fallback_message = (

            f"JEEBIK analyzed your income, average spending, "

            f"commitments, balance, and your existing "

            f"{plan.other_goal_name} goal. After protecting your "

            f"existing obligations and goal, the Financial Planning "

            f"Engine validated {recommended_purchase} "

            f"{recommended_year} as a feasible purchase target for "

            f"{plan.goal_name}. The plan uses a virtual monthly "

            f"allocation of SAR {monthly_allocation:,.0f} while "

            f"leaving SAR {safe_to_spend:,.0f} as Safe to Spend."

        )



    if client is None:

        return {

            "status": "fallback",

            "agent": "JEEBIK AI Agent",

            "stage": "initial_planning",

            "action": "financial_context_analyzed",

            "recommended_purchase": recommended_purchase,

            "recommended_year": recommended_year,

            "message": fallback_message,

            "note": (

                "AI API key was not available. "

                "Deterministic JEEBIK explanation used."

            )

        }



    prompt = f"""

You are the JEEBIK AI Financial Agent.



JEEBIK is an AI-powered financial planning layer inside a bank app.



You are currently handling INITIAL GOAL PLANNING.



Your role in this stage is:



Understand Context -> Interpret Validated Plan -> Personalize Explanation.



The user wants to create a new financial goal.



You are given the user's financial context and the results of

JEEBIK's deterministic Financial Planning Engine.



IMPORTANT ARCHITECTURE:



The AI understands and interprets the user's financial context.



The deterministic Financial Planning Engine performs and validates

all exact financial calculations.



You MUST NOT:



- invent financial numbers,

- change any validated number,

- recalculate the plan yourself,

- provide investment advice,

- claim money has been moved,

- claim that virtual allocation means money was transferred,

- ignore the user's existing commitments,

- ignore the user's existing goal.



You SHOULD:



- explain how the user's financial context affects the new goal,

- explain why the validated purchase month is feasible,

- explain the role of spending, commitments, and the existing goal,

- explain the trade-off created by the monthly allocation,

- make the explanation personalized and easy to understand,

- preserve user decision-making.



USER FINANCIAL CONTEXT



Current balance:

SAR {plan.balance:,.0f}



Monthly income:

SAR {plan.monthly_income:,.0f}



Average monthly spending:

SAR {plan.monthly_spending:,.0f}



Monthly commitments:

SAR {plan.monthly_commitments:,.0f}



Existing goal:

{plan.other_goal_name}



Existing goal total:

SAR {plan.other_goal_amount:,.0f}



Existing goal target:

{month_name(plan.other_goal_target_month)} {plan.other_goal_target_year}



Monthly amount required to keep existing goal on track:

SAR {required_other_goal_monthly:,.0f}



Available monthly capacity for new-goal planning:

SAR {available_for_planning:,.0f}





NEW GOAL



Goal:

{plan.goal_name}



Price:

SAR {plan.goal_price:,.0f}





VALIDATED FINANCIAL PLAN



Goal status:

{goal_status}



Recommended purchase month:

{recommended_purchase}



Recommended purchase year:

{recommended_year if recommended_year is not None else "N/A"}



Planning cycles needed:

{months_needed if months_needed is not None else "Not currently feasible"}



Virtual monthly allocation:

SAR {monthly_allocation:,.0f}



Safe to Spend after goal allocation:

SAR {safe_to_spend:,.0f}





Write a concise user-facing explanation in English.



Use 3 to 5 sentences.



The explanation should answer:



1. What financial context JEEBIK considered.

2. Why the recommended purchase timing is feasible.

3. How the existing goal and commitments were protected.

4. What the monthly allocation means for the user's flexibility.



Do not invent any number.



Do not recommend a different month.



Do not make the decision for the user.



Do not say that money was moved or transferred.



The monthly allocation is virtual planning only.

"""



    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=prompt

        )



        ai_text = (response.text or "").strip()



        if not ai_text:

            ai_text = fallback_message



        return {

            "status": "active",

            "agent": "JEEBIK AI Agent",

            "model": "gemini-3.5-flash-lite",

            "stage": "initial_planning",

            "action": "financial_context_analyzed",

            "recommended_purchase": recommended_purchase,

            "recommended_year": recommended_year,

            "message": ai_text

        }



    except Exception as error:

        print(

            "JEEBIK Initial Planning AI fallback:",

            type(error).__name__,

            str(error)

        )



        return {

            "status": "fallback",

            "agent": "JEEBIK AI Agent",

            "stage": "initial_planning",

            "action": "financial_context_analyzed",

            "recommended_purchase": recommended_purchase,

            "recommended_year": recommended_year,

            "message": fallback_message,

            "note": (

                "AI service was unavailable, so JEEBIK continued "

                "using its deterministic Financial Planning Engine."

            )

        }





# ============================================================

# REPLANNING AI AGENT

# ============================================================



def run_jeebik_ai_agent(

    plan: ReplanRequest,

    savings: float,

    preserved_progress_amount: float,

    remaining_amount: float,

    available_for_planning: float,

    required_other_goal_monthly: float,

    option_1: dict,

    option_2: dict

):

    """

    JEEBIK AI Agent responsibilities:



    1. Understand the financial event.

    2. Determine why the event is relevant to the active goal.

    3. Interpret the validated replanning options.

    4. Explain the trade-offs to the user.



    IMPORTANT:



    The AI does NOT calculate or validate financial figures.



    All financial calculations are performed first by JEEBIK's

    deterministic Financial Planning Engine.



    The AI only receives validated numbers and interprets them.

    """



    fallback_message = (

        f"The price of {plan.goal_name} dropped by "

        f"SAR {savings:,.0f}. This change is relevant because it "

        f"reduces the amount still needed for your active goal while "

        f"your existing commitments and {plan.other_goal_name} goal "

        f"remain protected. JEEBIK found two feasible strategies: "

        f"reach the goal earlier, or keep the original target and "

        f"reduce the future monthly allocation."

    )



    if client is None:

        return {

            "status": "fallback",

            "agent": "JEEBIK AI Agent",

            "event_type": "goal_price_change",

            "event_relevant": True,

            "action": "replanning_triggered",

            "message": fallback_message,

            "note": (

                "AI API key was not available. "

                "Deterministic JEEBIK explanation used."

            )

        }



    prompt = f"""

You are the JEEBIK AI Financial Agent.



JEEBIK is an AI-powered financial planning layer inside a bank app.



Your role is:



Monitor -> Understand -> Trigger -> Interpret.



A deterministic Financial Planning Engine has ALREADY calculated

and validated every financial number below.



You MUST NOT:



- invent new financial numbers,

- change any calculated amount,

- provide investment advice,

- choose an option for the user,

- claim money has been moved,

- claim the user must follow one option.



You should:



- identify why the event matters,

- explain that replanning was triggered,

- explain the trade-off between the two validated options,

- preserve user decision-making,

- keep the response concise and clear.



USER FINANCIAL CONTEXT



Monthly income:

SAR {plan.monthly_income:,.0f}



Average monthly spending:

SAR {plan.monthly_spending:,.0f}



Monthly commitments:

SAR {plan.monthly_commitments:,.0f}



Existing protected goal:

{plan.other_goal_name}



Monthly amount required for protected goal:

SAR {required_other_goal_monthly:,.0f}



Available monthly capacity for planning:

SAR {available_for_planning:,.0f}





ACTIVE GOAL



Goal:

{plan.goal_name}



Previous price:

SAR {plan.previous_price:,.0f}



New price:

SAR {plan.new_price:,.0f}



Price decrease:

SAR {savings:,.0f}



Existing virtual progress:

SAR {preserved_progress_amount:,.0f}



Remaining amount after price change:

SAR {remaining_amount:,.0f}





VALIDATED OPTION 1



Name:

{option_1["title"]}



Target:

{option_1["target_month"]} {option_1["target_year"]}



Future monthly allocation:

SAR {option_1["future_monthly_allocation"]:,.0f}



Safe to Spend:

SAR {option_1["safe_to_spend"]:,.0f}





VALIDATED OPTION 2



Name:

{option_2["title"]}



Target:

{option_2["target_month"]} {option_2["target_year"]}



Future monthly allocation:

SAR {option_2["future_monthly_allocation"]:,.0f}



Safe to Spend:

SAR {option_2["safe_to_spend"]:,.0f}





Write a short user-facing explanation in English.



Use 3 to 5 sentences.



Explain:



1. What changed.

2. Why JEEBIK triggered replanning.

3. The trade-off between the two validated options.

4. That the final choice remains with the user.



Do not recommend one option as the correct choice.

"""



    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=prompt

        )



        ai_text = (response.text or "").strip()



        if not ai_text:

            ai_text = fallback_message



        return {

            "status": "active",

            "agent": "JEEBIK AI Agent",

            "model": "gemini-3.5-flash-lite",

            "event_type": "goal_price_change",

            "event_relevant": True,

            "action": "replanning_triggered",

            "message": ai_text

        }



    except Exception as error:

        print(

            "JEEBIK AI Agent fallback:",

            type(error).__name__,

            str(error)

        )



        return {

            "status": "fallback",

            "agent": "JEEBIK AI Agent",

            "event_type": "goal_price_change",

            "event_relevant": True,

            "action": "replanning_triggered",

            "message": fallback_message,

            "note": (

                "AI service was unavailable, so JEEBIK continued "

                "using its deterministic Financial Planning Engine."

            )

        }





# ============================================================
# RECURRING COMMITMENT DETECTION AI AGENT
# ============================================================


def build_fallback_commitment_candidates(transactions):
    """Find repeated expense patterns when Gemini is unavailable."""
    groups = {}

    for transaction in transactions:
        if transaction.type.lower() != "expense":
            continue

        key = (
            transaction.name.strip().lower(),
            round(float(transaction.amount), 2)
        )
        groups.setdefault(key, []).append(transaction)

    candidates = []

    for (_, amount), items in groups.items():
        if len(items) < 3:
            continue

        first = items[0]
        candidates.append({
            "name": first.name,
            "amount": amount,
            "frequency": "Monthly",
            "category": first.category,
            "occurrences": len(items),
            "dates": [item.date for item in items],
            "confidence": "high",
            "reason": (
                f"A payment to {first.name} for SAR {amount:,.0f} "
                f"appears {len(items)} times in the transaction history."
            )
        })

    return candidates


def validate_ai_commitment_candidate(candidate, transactions):
    """Verify Gemini's suggestion against the original bank data."""
    if not isinstance(candidate, dict):
        return None

    candidate_name = str(candidate.get("name", "")).strip()
    if not candidate_name:
        return None

    matching = [
        item for item in transactions
        if item.type.lower() == "expense"
        and item.name.strip().lower() == candidate_name.lower()
    ]

    if len(matching) < 3:
        return None

    amounts = [round(float(item.amount), 2) for item in matching]
    most_common_amount = max(set(amounts), key=amounts.count)
    same_amount_items = [
        item for item in matching
        if round(float(item.amount), 2) == most_common_amount
    ]

    if len(same_amount_items) < 3:
        return None

    first = same_amount_items[0]
    return {
        "name": first.name,
        "amount": most_common_amount,
        "frequency": "Monthly",
        "category": first.category,
        "occurrences": len(same_amount_items),
        "dates": [item.date for item in same_amount_items],
        "confidence": str(candidate.get("confidence", "high")),
        "reason": str(candidate.get(
            "reason",
            f"A recurring payment to {first.name} was detected across multiple months."
        ))
    }


def run_commitment_detection_ai_agent(transactions):
    """
    Transaction History -> Gemini understands the pattern ->
    JEEBIK validates it -> User confirms or rejects it.
    """
    fallback_candidates = build_fallback_commitment_candidates(transactions)

    if client is None:
        return {
            "status": "fallback",
            "agent": "JEEBIK AI Agent",
            "model": None,
            "stage": "commitment_detection",
            "action": "recurring_pattern_detected",
            "candidates": fallback_candidates[:1],
            "note": "Gemini was unavailable, so deterministic pattern detection was used."
        }

    transaction_text = "\n".join(
        f"- {item.date} | {item.name} | SAR {item.amount:,.2f} | "
        f"{item.category} | {item.type}"
        for item in transactions
    )

    prompt = f"""
You are the JEEBIK AI Financial Agent inside a bank app.

Task: identify the strongest potential recurring financial commitment
from the bank transaction history below.

Rules:
- Use only the provided transactions.
- Do not invent names, amounts, dates, or transactions.
- Require at least 3 occurrences.
- Prefer fixed obligations such as education fees, insurance, or utilities
  over optional subscriptions when a stronger obligation exists.
- Do not add anything automatically. The user must confirm it.
- Return at most ONE strongest candidate.

TRANSACTION HISTORY:
{transaction_text}

Return ONLY valid JSON in this exact shape:
{{
  "candidates": [
    {{
      "name": "exact transaction name",
      "confidence": "high",
      "reason": "short user-facing explanation"
    }}
  ]
}}

If none exists, return {{"candidates": []}}.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        raw_text = (response.text or "").strip()
        clean_text = raw_text

        if clean_text.startswith("```"):
            clean_text = clean_text.strip("`").strip()
            if clean_text.lower().startswith("json"):
                clean_text = clean_text[4:].strip()

        parsed = json.loads(clean_text)
        validated_candidates = []

        for candidate in parsed.get("candidates", []):
            validated = validate_ai_commitment_candidate(candidate, transactions)
            if validated:
                validated_candidates.append(validated)

        return {
            "status": "active",
            "agent": "JEEBIK AI Agent",
            "model": "gemini-3.5-flash-lite",
            "stage": "commitment_detection",
            "action": "recurring_pattern_detected",
            "candidates": validated_candidates[:1]
        }

    except Exception as error:
        print(
            "JEEBIK Commitment Detection AI fallback:",
            type(error).__name__,
            str(error)
        )

        return {
            "status": "fallback",
            "agent": "JEEBIK AI Agent",
            "model": "gemini-3.5-flash-lite",
            "stage": "commitment_detection",
            "action": "recurring_pattern_detected",
            "candidates": fallback_candidates[:1],
            "note": "Gemini response could not be validated, so deterministic pattern detection was used."
        }


# ============================================================
# DETECT COMMITMENTS
# ============================================================


@app.post("/detect-commitments")
def detect_commitments(request: CommitmentDetectionRequest):
    ai_result = run_commitment_detection_ai_agent(request.transactions)
    candidates = ai_result.get("candidates", [])

    return {
        "status": "success",
        "detected": len(candidates) > 0,
        "pending_user_confirmation": len(candidates) > 0,
        "candidates": candidates,
        "ai_agent": ai_result,
        "architecture": {
            "bank_data": "Transaction History",
            "ai_agent": "Understand Pattern -> Identify Potential Commitment",
            "validation": "Verify AI suggestion against bank transaction data",
            "user": "Confirm or Reject",
            "financial_planning_engine": "Uses only confirmed commitments"
        }
    }


# ============================================================

# HOME

# ============================================================



@app.get("/")

def home():

    return {

        "status": "success",

        "message": "JEEBIK Backend is running",

        "version": "2.2.0",

        "architecture": {

            "initial_planning": (

                "AI Understands Context -> "

                "Engine Calculates & Validates -> "

                "AI Interprets"

            ),

            "proactive_replanning": (

                "AI Monitor -> Understand -> Trigger -> Interpret"

            ),

            "financial_engine": (

                "Calculate -> Validate"

            ),

            "user": (

                "Final decision"

            )

        },

        "ai_configured": client is not None

    }





# ============================================================

# ANALYZE PLAN

# ============================================================



@app.post("/analyze-plan")

def analyze_plan(plan: PlanRequest):

    today = date.today()



    # --------------------------------------------------------

    # 1. EXISTING GOAL MONTHLY REQUIREMENT

    # --------------------------------------------------------



    (

        months_left_for_other_goal,

        required_other_goal_monthly

    ) = calculate_existing_goal_monthly(

        today,

        plan.other_goal_amount,

        plan.other_goal_target_year,

        plan.other_goal_target_month

    )



    # --------------------------------------------------------

    # 2. MONTHLY FINANCIAL PICTURE

    # --------------------------------------------------------



    available_for_planning = calculate_available_for_planning(

        plan.monthly_income,

        plan.monthly_spending,

        plan.monthly_commitments,

        required_other_goal_monthly

    )



    # --------------------------------------------------------

    # 3. NEW GOAL PLANNING

    # --------------------------------------------------------



    if available_for_planning <= 0:

        months_needed = None

        monthly_allocation = 0



    else:

        months_needed = math.ceil(

            plan.goal_price

            / available_for_planning

        )



        months_needed = max(

            months_needed,

            1

        )



        raw_monthly_allocation = (

            plan.goal_price

            / months_needed

        )



        monthly_allocation = round_up_to_50(

            raw_monthly_allocation

        )



        monthly_allocation = min(

            monthly_allocation,

            available_for_planning,

            plan.goal_price

        )



    # --------------------------------------------------------

    # 4. VIRTUAL GOAL PROGRESS

    # --------------------------------------------------------



    goal_progress_amount = min(

        monthly_allocation,

        plan.goal_price

    )



    if plan.goal_price > 0:

        progress_percentage = (

            goal_progress_amount

            / plan.goal_price

        ) * 100

    else:

        progress_percentage = 0



    progress_percentage = min(

        max(progress_percentage, 0),

        100

    )



    progress_percentage = round(

        progress_percentage,

        1

    )



    # --------------------------------------------------------

    # 5. RECOMMENDED PURCHASE DATE

    # --------------------------------------------------------



    if months_needed is None:

        recommended_purchase = (

            "Not currently feasible"

        )



        recommended_year = None



    else:

        target_year, target_month = add_months(

            today,

            months_needed

        )



        recommended_purchase = month_name(

            target_month

        )



        recommended_year = target_year



    # --------------------------------------------------------

    # 6. SAFE TO SPEND

    # --------------------------------------------------------



    safe_to_spend = (

        available_for_planning

        - monthly_allocation

    )



    safe_to_spend = max(

        safe_to_spend,

        0

    )



    # --------------------------------------------------------

    # 7. GOAL STATUS

    # --------------------------------------------------------



    if months_needed is None:

        goal_status = "Needs Adjustment"

    else:

        goal_status = "On Track"



    # --------------------------------------------------------

    # 8. DETERMINISTIC ENGINE EXPLANATION

    # --------------------------------------------------------



    if months_needed is None:

        explanation = (

            f"Based on your monthly income, spending, "

            f"commitments, and existing goals, there is "

            f"currently no available monthly capacity "

            f"for this new goal."

        )



    else:

        explanation = (

            f"After your average monthly spending of "

            f"SAR {plan.monthly_spending:,.0f}, monthly "

            f"commitments of SAR "

            f"{plan.monthly_commitments:,.0f}, and "

            f"SAR {required_other_goal_monthly:,.0f} "

            f"required each month to keep your "

            f"{plan.other_goal_name} on track, you have "

            f"SAR {available_for_planning:,.0f} available "

            f"for planning. A virtual monthly allocation "

            f"of approximately SAR "

            f"{monthly_allocation:,.0f} allows you to "

            f"reach this goal in {months_needed} month"

            f"{'s' if months_needed != 1 else ''}, "

            f"while leaving approximately "

            f"SAR {safe_to_spend:,.0f} as Safe to Spend."

        )



    # --------------------------------------------------------

    # 9. INITIAL PLANNING AI AGENT

    # --------------------------------------------------------



    ai_agent_result = run_initial_planning_ai_agent(

        plan=plan,

        required_other_goal_monthly=required_other_goal_monthly,

        available_for_planning=available_for_planning,

        recommended_purchase=recommended_purchase,

        recommended_year=recommended_year,

        months_needed=months_needed,

        monthly_allocation=monthly_allocation,

        safe_to_spend=safe_to_spend,

        goal_status=goal_status

    )



    # --------------------------------------------------------

    # 10. RESPONSE

    # --------------------------------------------------------



    return {

        "goal": plan.goal_name,

        "price": plan.goal_price,

        "current_date": today.isoformat(),



        "recommended_purchase":

            recommended_purchase,



        "recommended_year":

            recommended_year,



        "months_needed":

            months_needed,



        "monthly_allocation":

            monthly_allocation,



        "goal_progress_amount":

            goal_progress_amount,



        "progress_percentage":

            progress_percentage,



        "goal_status":

            goal_status,



        "available_for_planning":

            available_for_planning,



        "safe_to_spend":

            safe_to_spend,



        "explanation":

            explanation,



        "ai_agent":

            ai_agent_result,



        "financial_context": {

            "balance":

                plan.balance,



            "monthly_income":

                plan.monthly_income,



            "average_monthly_spending":

                plan.monthly_spending,



            "monthly_commitments":

                plan.monthly_commitments,



            "other_goal_name":

                plan.other_goal_name,



            "other_goal_amount":

                plan.other_goal_amount,



            "other_goal_target":

                f"{month_name(plan.other_goal_target_month)} "

                f"{plan.other_goal_target_year}",



            "months_left_for_other_goal":

                months_left_for_other_goal,



            "required_other_goal_monthly":

                required_other_goal_monthly

        },



        "engine": {

            "type": "deterministic",

            "role": "Calculate -> Validate"

        },



        "architecture": {

            "ai_agent": (

                "Understand Context -> Interpret Validated Plan"

            ),

            "financial_planning_engine": (

                "Calculate -> Validate"

            ),

            "user": (

                "Final Decision"

            )

        }

    }





# ============================================================

# PROACTIVE REPLANNING

# ============================================================



@app.post("/replan")

def replan(plan: ReplanRequest):

    today = date.today()



    # ========================================================

    # 1. PRICE CHANGE EVENT

    # ========================================================



    savings = max(

        plan.previous_price

        - plan.new_price,

        0

    )



    # ========================================================

    # 2. PROTECT EXISTING FINANCIAL CONTEXT

    # ========================================================



    (

        months_left_for_other_goal,

        required_other_goal_monthly

    ) = calculate_existing_goal_monthly(

        today,

        plan.other_goal_amount,

        plan.other_goal_target_year,

        plan.other_goal_target_month

    )



    available_for_planning = calculate_available_for_planning(

        plan.monthly_income,

        plan.monthly_spending,

        plan.monthly_commitments,

        required_other_goal_monthly

    )



    # ========================================================

    # 3. PRESERVE EXISTING VIRTUAL PROGRESS

    # ========================================================



    preserved_progress_amount = min(

        max(plan.current_progress_amount, 0),

        plan.new_price

    )



    remaining_amount = max(

        plan.new_price

        - preserved_progress_amount,

        0

    )



    if plan.new_price > 0:

        updated_progress_percentage = (

            preserved_progress_amount

            / plan.new_price

        ) * 100

    else:

        updated_progress_percentage = 0



    updated_progress_percentage = round(

        min(

            max(updated_progress_percentage, 0),

            100

        ),

        1

    )



    # ========================================================

    # 4. ORIGINAL TARGET DATE

    # ========================================================



    original_target_month_number = month_number(

        plan.current_target_month

    )



    months_to_original_target = months_until(

        today.year,

        today.month,

        plan.current_target_year,

        original_target_month_number

    )



    # ========================================================

    # 5. OPTION 1 — BUY EARLIER

    # ========================================================



    if remaining_amount <= 0:

        earlier_cycles_needed = 0

        earlier_future_allocation = 0



        earlier_target_year = today.year

        earlier_target_month_number = today.month



    elif available_for_planning <= 0:

        earlier_cycles_needed = months_to_original_target

        earlier_future_allocation = 0



        earlier_target_year = (

            plan.current_target_year

        )



        earlier_target_month_number = (

            original_target_month_number

        )



    else:

        earlier_cycles_needed = math.ceil(

            remaining_amount

            / available_for_planning

        )



        earlier_cycles_needed = max(

            earlier_cycles_needed,

            1

        )



        earlier_cycles_needed = min(

            earlier_cycles_needed,

            months_to_original_target

        )



        (

            earlier_target_year,

            earlier_target_month_number

        ) = add_months(

            today,

            earlier_cycles_needed

        )



        earlier_raw_allocation = (

            remaining_amount

            / earlier_cycles_needed

        )



        earlier_future_allocation = round_up_to_50(

            earlier_raw_allocation

        )



        earlier_future_allocation = min(

            earlier_future_allocation,

            available_for_planning,

            remaining_amount

        )



    earlier_safe_to_spend = max(

        available_for_planning

        - earlier_future_allocation,

        0

    )



    earlier_target_month = month_name(

        earlier_target_month_number

    )



    # ========================================================

    # 6. OPTION 2 — KEEP ORIGINAL TARGET

    # ========================================================



    if remaining_amount <= 0:

        reduced_future_allocation = 0



    elif available_for_planning <= 0:

        reduced_future_allocation = 0



    else:

        reduced_raw_allocation = (

            remaining_amount

            / months_to_original_target

        )



        reduced_future_allocation = round_up_to_50(

            reduced_raw_allocation

        )



        reduced_future_allocation = min(

            reduced_future_allocation,

            available_for_planning,

            remaining_amount

        )



    reduced_safe_to_spend = max(

        available_for_planning

        - reduced_future_allocation,

        0

    )



    # ========================================================

    # 7. RELEASED MONTHLY CAPACITY

    # ========================================================



    earlier_released_capacity = max(

        plan.current_monthly_allocation

        - earlier_future_allocation,

        0

    )



    reduced_released_capacity = max(

        plan.current_monthly_allocation

        - reduced_future_allocation,

        0

    )



    # ========================================================

    # 8. TOTAL GOAL ALLOCATIONS

    # ========================================================



    earlier_total_goal_allocations = (

        required_other_goal_monthly

        + earlier_future_allocation

    )



    reduced_total_goal_allocations = (

        required_other_goal_monthly

        + reduced_future_allocation

    )



    # ========================================================

    # 9. GOAL STATUS

    # ========================================================



    if remaining_amount <= 0:

        goal_status = "Goal Covered"



    elif available_for_planning <= 0:

        goal_status = "Needs Adjustment"



    else:

        goal_status = "On Track"



    # ========================================================

    # 10. DETERMINISTIC EXPLANATION

    # ========================================================



    explanation = (

        f"The price of {plan.goal_name} decreased from "

        f"SAR {plan.previous_price:,.0f} to "

        f"SAR {plan.new_price:,.0f}, saving you "

        f"SAR {savings:,.0f}. Your existing virtual "

        f"progress of SAR {preserved_progress_amount:,.0f} "

        f"is preserved, leaving SAR "

        f"{remaining_amount:,.0f} still to plan for. "

        f"JEEBIK recalculated the remaining amount while "

        f"protecting your monthly commitments and your "

        f"{plan.other_goal_name} goal."

    )



    # ========================================================

    # 11. BUILD VALIDATED OPTIONS

    # ========================================================



    option_1 = {

        "id":

            "buy_earlier",



        "title":

            "Buy Earlier",



        "description":

            (

                "Use the lower price to complete "

                "the remaining amount sooner."

            ),



        "target_month":

            earlier_target_month,



        "target_year":

            earlier_target_year,



        "goal_progress_amount":

            preserved_progress_amount,



        "progress_percentage":

            updated_progress_percentage,



        "remaining_amount":

            remaining_amount,



        "future_monthly_allocation":

            earlier_future_allocation,



        "monthly_allocation":

            earlier_future_allocation,



        "released_monthly_capacity":

            earlier_released_capacity,



        "total_goal_allocations":

            earlier_total_goal_allocations,



        "safe_to_spend":

            earlier_safe_to_spend,



        "goal_status":

            goal_status

    }



    option_2 = {

        "id":

            "keep_target_reduce_allocation",



        "title":

            "Keep Target & Reduce Allocation",



        "description":

            (

                "Keep your original target date "

                "and reduce the amount JEEBIK "

                "needs to allocate going forward."

            ),



        "target_month":

            plan.current_target_month,



        "target_year":

            plan.current_target_year,



        "goal_progress_amount":

            preserved_progress_amount,



        "progress_percentage":

            updated_progress_percentage,



        "remaining_amount":

            remaining_amount,



        "future_monthly_allocation":

            reduced_future_allocation,



        "monthly_allocation":

            reduced_future_allocation,



        "released_monthly_capacity":

            reduced_released_capacity,



        "total_goal_allocations":

            reduced_total_goal_allocations,



        "safe_to_spend":

            reduced_safe_to_spend,



        "goal_status":

            goal_status

    }



    # ========================================================

    # 12. JEEBIK AI AGENT

    # ========================================================



    ai_agent_result = run_jeebik_ai_agent(

        plan=plan,

        savings=savings,

        preserved_progress_amount=preserved_progress_amount,

        remaining_amount=remaining_amount,

        available_for_planning=available_for_planning,

        required_other_goal_monthly=required_other_goal_monthly,

        option_1=option_1,

        option_2=option_2

    )



    # ========================================================

    # 13. RESPONSE

    # ========================================================



    return {

        "status":

            "replanned",



        "goal":

            plan.goal_name,



        "previous_price":

            plan.previous_price,



        "new_price":

            plan.new_price,



        "savings":

            savings,



        "current_date":

            today.isoformat(),



        "event": {

            "type":

                "goal_price_change",



            "detected":

                True,



            "meaningful_change":

                savings > 0,



            "replanning_triggered":

                savings > 0

        },



        "previous_plan": {

            "target_month":

                plan.current_target_month,



            "target_year":

                plan.current_target_year,



            "monthly_allocation":

                plan.current_monthly_allocation,



            "progress_amount":

                plan.current_progress_amount

        },



        "updated_goal": {

            "goal_price":

                plan.new_price,



            "goal_progress_amount":

                preserved_progress_amount,



            "progress_percentage":

                updated_progress_percentage,



            "remaining_amount":

                remaining_amount,



            "goal_status":

                goal_status

        },



        "financial_context": {

            "balance":

                plan.balance,



            "monthly_income":

                plan.monthly_income,



            "average_monthly_spending":

                plan.monthly_spending,



            "monthly_commitments":

                plan.monthly_commitments,



            "other_goal_name":

                plan.other_goal_name,



            "other_goal_amount":

                plan.other_goal_amount,



            "other_goal_target":

                f"{month_name(plan.other_goal_target_month)} "

                f"{plan.other_goal_target_year}",



            "months_left_for_other_goal":

                months_left_for_other_goal,



            "required_other_goal_monthly":

                required_other_goal_monthly,



            "available_for_planning":

                available_for_planning

        },



        "options": [

            option_1,

            option_2

        ],



        "explanation":

            explanation,



        "ai_agent":

            ai_agent_result,



        "architecture": {

            "ai_agent":

                "Monitor -> Understand -> Trigger -> Interpret",



            "financial_planning_engine":

                "Calculate -> Validate",



            "user":

                "Final Decision"

        }

    }