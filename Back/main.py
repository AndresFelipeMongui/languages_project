from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from database import executions

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():

    return {
        "message": "MathLite API funcionando correctamente"
    }


@app.post("/execute")
def execute_code(request: CodeRequest):

    try:

        lexer = Lexer(request.code)

        tokens = lexer.tokenize()

        parser = Parser(tokens)

        ast = parser.parse()

        interpreter = Interpreter()

        interpreter.visit(ast)

        response_data = {

            "tokens": [
                str(t)
                for t in tokens
            ],

            "ast": ast.to_dict(),

            "output": interpreter.output,

            "errors": lexer.errors,

            "symbol_table":
                interpreter.get_symbol_table()
        }

        return JSONResponse(
            content=jsonable_encoder(response_data)
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.post("/save")
def save_execution(request: CodeRequest):

    try:

        lexer = Lexer(request.code)

        tokens = lexer.tokenize()

        parser = Parser(tokens)

        ast = parser.parse()

        interpreter = Interpreter()

        interpreter.visit(ast)

        execution_data = {

            "code": request.code,

            "tokens": [
                str(t)
                for t in tokens
            ],

            "ast": ast.to_dict(),

            "output": interpreter.output,

            "errors": lexer.errors,

            "symbol_table":
                interpreter.get_symbol_table(),

            "created_at":
                str(datetime.now())
        }

        executions.insert_one(
            jsonable_encoder(execution_data)
        )

        return {
            "message":
                "Ejecución guardada correctamente"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.get("/history")
def get_history():

    history = []

    for execution in executions.find():

        execution["_id"] = str(
            execution["_id"]
        )

        history.append(execution)

    return history