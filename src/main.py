import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from tools.generate_cases import tool_generate_cases_full
from tools.save_cases import tool_save_cases_by_id
from tools.save_cases_gherkin import tool_save_cases_gherkin_by_id
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv() 

token_counter = TokenCountingHandler()  # verbose=True si quieres logs por llamada
cb_manager = CallbackManager([token_counter])

agent = FunctionAgent(
    tools=[tool_generate_cases_full, tool_save_cases_by_id, tool_save_cases_gherkin_by_id],
    llm=OpenAI(model="gpt-4.1"),
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
    headers = {
        "Content-Type": "application/json", 
        "Authorization": "Bearer token", 
        "sessionId": "01", 
        "dateTime": "2025-03-18T17:27:16.262130-04:00"
    }
    body = {
        "products": [
            {
                "number": "4230196605",
                "productLine": "CuentaAhorro",
                "currency": "DOP"
            }
        ],
        "clients": [
            {
                "contactWays": {
                    "contactWay": {
                        "value": "8092123412"
                    }
                }
            }
        ]
    }

    endpoint = "https://ms-cons-cta-mio-ache-ws-dev.apps.az-aro-dev.banreservas.com/api/v1/ms-consulta-cuenta-mio-ache-ws"
    method = "POST"
    # Nombres para prefijo: CP [suite] - [microservicio] - <caso>
    suite_name = "Consulta Cuenta Mio"
    microservice_name = "ms-cons-cta-mio-ache-ws"

    prompt = f"""
        1) CALL tool_generate_cases_full(
        endpoint_template="{endpoint}",
        method="{method}",
        headers={headers},
        body={body},
        query=None,
        path=None,
        base_case_name="POST - Camino feliz",
        negative_status=400,
        mutate_headers=False,
        suite_name="{suite_name}",
        microservice_name="{microservice_name}"
        )

        2) Con el objeto devuelto, CALL tool_save_cases_by_id(
        cases_id=<cases_id>,
        json_path="api_test_cases.json",
        csv_path="api_test_cases.csv",
        output_dir=<cases_id>
        )

        3) CALL tool_save_cases_gherkin_by_id(
        cases_id=<cases_id>,
        feature_path="api_test_cases.feature",
        feature_name="Casos de API - BDD",
        output_dir=<cases_id>
        )

        Responde SOLO con:
        - total: <número devuelto>
        - id: <cases_id>
        - json: <cases_id>/api_test_cases.json
        - csv: <cases_id>/api_test_cases.csv
        - feature: <cases_id>/api_test_cases.feature
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
