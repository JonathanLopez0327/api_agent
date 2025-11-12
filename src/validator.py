import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent

from tools.validate_cases import tool_validate_cases_by_id


load_dotenv()


token_counter = TokenCountingHandler()
cb_manager = CallbackManager([token_counter])

validator_agent = FunctionAgent(
    tools=[tool_validate_cases_by_id],
    llm=OpenAI(model="gpt-4.1"),
    callback_manager=cb_manager,
    system_prompt=(
        "Eres un validador de pruebas de API.\n"
        "Flujo OBLIGATORIO:\n"
        "1) Llama a `tool_validate_cases_by_id(cases_id, timeout)` exactamente con los argumentos.\n"
        "2) Devuelve solo el resumen de ejecución (total/passed/failed) y los primeros resultados.\n"
        "El token se lee de variables de entorno (API_TOKEN o BEARER_TOKEN).\n"
    ),
)


async def main():
    cases_id = None
    # Permitir pasar el CASES_ID por variable de entorno o argumento
    cases_id = os.getenv("CASES_ID") or cases_id
    import sys
    if not cases_id and len(sys.argv) > 1:
        cases_id = sys.argv[1]

    if not cases_id:
        print("Falta CASES_ID. Exporta CASES_ID en .env o pásalo como argumento.")
        return

    prompt = f"""
        CALL tool_validate_cases_by_id(
        cases_id="{cases_id}",
        timeout=30.0
        )

        Responde SOLO con:
        - cases_id: <id>
        - total: <n>
        - passed: <n>
        - failed: <n>
        - sample: primeros resultados si existen
    """

    resp = await validator_agent.run(prompt)
    print(str(resp))

    print("Prompt tokens:", token_counter.prompt_llm_token_count)
    print("Completion tokens:", token_counter.completion_llm_token_count)
    print("Total LLM tokens:", token_counter.total_llm_token_count)


if __name__ == "__main__":
    asyncio.run(main())

