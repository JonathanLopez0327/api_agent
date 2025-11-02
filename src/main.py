import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from tools.generate_cases import tool_generate_cases_full
from tools.save_cases import tool_save_cases_by_id
from tools.save_cases_gherkin import tool_save_cases_gherkin_by_id
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler


token_counter = TokenCountingHandler()  # verbose=True si quieres logs por llamada
cb_manager = CallbackManager([token_counter])

llm = Ollama(
    model="gpt-oss:20b",
    request_timeout=360.0,
    context_window=8000,
    callback_manager=cb_manager,          # <- IMPORTANTE: conéctalo al LLM
)

agent = FunctionAgent(
    tools=[tool_generate_cases_full, tool_save_cases_by_id, tool_save_cases_gherkin_by_id],
    llm=llm,
    callback_manager=cb_manager,
    system_prompt=(
        "Eres un asistente de QA que genera y guarda casos de prueba de API.\n"
        "Flujo OBLIGATORIO:\n"
        "1) Llama a `tool_generate_cases_full` con los argumentos EXACTOS.\n"
        "   Esta herramienta devuelve SOLO un objeto pequeño: {cases_id, total, examples}.\n"
        "2) Llama a `tool_save_cases_by_id` con el cases_id devuelto y las rutas de salida (JSON/CSV).\n"
        "3) Llama a `tool_save_cases_gherkin_by_id` con el mismo cases_id para guardar un .feature en formato BDD Gherkin.\n"
        "Nunca pegues la lista completa de 'cases' en un tool-call. Usa SIEMPRE 'cases_id'."
    )
)

async def main():
    headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}
    body = {
        "businessSearches": [{
            "name": "Software Sushi",
            "expectations": {
                "businessName": "Software Sushi",
                "businessStreet": "4566 San Mellina Dr",
                "businessCity": "Coconut Creek",
                "businessState": "FL",
                "businessZip": "33073",
                "businessCountry": "US"
            }
        }]
    }
    endpoint = "https://api.mi-banco/transacciones/crear"
    method = "POST"

    prompt = f"""
        1) CALL tool_generate_cases_full(
        endpoint_template="{endpoint}",
        method="{method}",
        headers={headers},
        body={body},
        query=None,
        path=None,
        base_case_name="POST - Happy Path",
        negative_status=400,
        mutate_headers=False
        )

        2) Con el objeto devuelto, CALL tool_save_cases_by_id(
        cases_id=<cases_id>,
        json_path="api_test_cases.json",
        csv_path="api_test_cases.csv"
        )

        3) CALL tool_save_cases_gherkin_by_id(
        cases_id=<cases_id>,
        feature_path="api_test_cases.feature",
        feature_name="Casos de API - BDD"
        )

        Responde SOLO con:
        - total: <número devuelto>
        - id: <cases_id>
        - json: api_test_cases.json
        - csv: api_test_cases.csv
        - feature: api_test_cases.feature
    """

    resp = await agent.run(prompt)
    print(str(resp))

    # 4) lee métricas
    print("Prompt tokens:", token_counter.prompt_llm_token_count)
    print("Completion tokens:", token_counter.completion_llm_token_count)
    print("Total LLM tokens:", token_counter.total_llm_token_count)

    # Si usas embeddings:
    print("Embedding tokens:", token_counter.total_embedding_token_count)

if __name__ == "__main__":
    asyncio.run(main())
