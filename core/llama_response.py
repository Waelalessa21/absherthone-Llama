import asyncio
import json
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from utils.prompt import PROMPT_TEMPLATE
from utils.spell_correction import correct_spelling
from utils.translation import translate_to_arabic

async def analyze_chunk(user_input, chat_history):
    corrected_input = correct_spelling(user_input)
    recent_history = "\n\n".join(chat_history[-4:])
    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(history=recent_history, message=corrected_input)
    model = Ollama(model="llama3.2")
    response = await asyncio.to_thread(model.invoke, prompt)
    try:
        data = json.loads(response)
        classification = data.get("classification", "Unknown")
        notification_en = data.get("notification", "Unable to generate notification.")
        notification_ar = translate_to_arabic(notification_en)
        risk_score = float(data.get("risk_score", 0.5))
        risk_score = max(0.0, min(risk_score, 1.0))
    except json.JSONDecodeError:
        classification = "Unknown"
        notification_en = "⚠️ The model returned an invalid response."
        notification_ar = translate_to_arabic(notification_en)
        risk_score = 0.5
    except Exception:
        classification = "Unknown"
        notification_en = "⚠️ Could not classify the message."
        notification_ar = translate_to_arabic(notification_en)
        risk_score = 0.5
    return {
        "classification": classification.capitalize(),
        "risk_score": risk_score,
        "notification_en": notification_en,
        "notification_ar": notification_ar
    }
