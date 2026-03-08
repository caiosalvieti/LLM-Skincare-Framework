from fastapi import FastAPI
from pydantic import BaseModel
from evaluation import calculate_score

app = FastAPI(title="Moltbook-Clone Evaluation API")

# Modelo de dados que o FastAPI vai esperar receber
class EvaluationRequest(BaseModel):
    response_text: str
    tau_threshold: int = 50

@app.post("/evaluate")
async def evaluate_interaction(request: EvaluationRequest):
    """
    Endpoint que recebe a resposta do modelo (R) e retorna o Score(R).
    O front-end fará o parse desta saída JSON para renderizar o feed em tempo real[cite: 39].
    """
    score = calculate_score(request.response_text, request.tau_threshold)
    
    return {
        "status": "success",
        "response_length": len(request.response_text),
        "calculated_score": score
    }