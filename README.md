python 3.6+

1 - Instalar PIP3:

    sudo apt-get update
    sudo apt-get install -y python3-pip

2 - No diretorio do Projeto: Executar requirements ou instalar dependencias:

    Executar requirements:
        pip3 install -r requirements.txt

    Instalar dependencias (FastAPI e Uvicorn):
        pip3 install fastapi
        pip3 install uvicorn
        pip3 install -U python-dotenv

3 - Rodar backend:

    python3 app/server.py

Especificações da API validar farmula proposicional:

    Endpoint: http://localhost:3000/logica/v1/validaFormula
    Modelo Request: {"formula": String}
    Modelo Response: {error: String, formula : String, resultado : Bool}

    No Request:
        Máximo de 10 símbolos proposicionais
        Símbolos proposicionais aceitos: P, Q, R, S, P1, Q1, R1, S1, ... P99, Q99, R99, S99,
        Conectivos: v, ^, ->, <->, ~

    No Response:
        formula-> formula enviada.
        resultado-> true se formula valida e false se não.
        error-> caractere errado ou motivo do erro.
            Ex:"Numero de parenteses abertos:7 diferente do numero de fechados:8", "->)", "#"
            *Sujeito a alteração*

    Link da Collection do Postman para teste da API: https://www.getpostman.com/collections/ef0260391428b67f5403
