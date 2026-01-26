from core.entrypoint import run_ai_core

if __name__ == "__main__":
    text_query = "Bonjour, j'ai fait une chute et j'ai très mal au poignet, fracture possible."
    text_context = "Appel entrant - accidents de la vie. Client demande quoi faire."
    embedding768 = [0.0] * 768  # mock embedding for now (works for pipeline test)

    decision = run_ai_core(text_query, text_context, embedding768)
    print(decision)