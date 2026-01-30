from fastapi import APIRouter
from app.schemas.ai import PromptInput, PromptOutput
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import json
import base64
from pathlib import Path
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv() 
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL=os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_MODEL=os.getenv("OPENROUTER_MODEL")


router = APIRouter(prefix="/ai", tags=["ai"])


def encode_image_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')


@router.get("/")
def test():
    url = f"{OPENROUTER_BASE_URL}"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Read and encode the PDF
    pdf_path = r"C:\Users\boisn\Documents\Vsc\Hitema_master\FastAPI\Projets\Projet_fast_api\cv-summarizer\app\routers\test.jpg"
    base64_pdf = encode_image_to_base64(pdf_path)
    data_url = f"data:image/jpeg;base64,{base64_pdf}"
    messages = [
        {
            "role": "kevin",
            "content": [
                {
                    "type": "text",
                    "text": "What are the main points in this document?"
                },
                {
                    "type": "image",
                    "image": {
                        "filename": "test.jpg",
                        "file_data": data_url
                    }
                },
            ]
        }
    ]
    # Optional: Configure PDF processing engine
    # PDF parsing will still work even if the plugin is not explicitly set
    plugins = [
        {
            "id": "file-parser",
            "jpg": {
                "engine": "jpg-text"  # defaults to "mistral-ocr". See Pricing above
            }
        }
    ]
    payload = {
        # "model": "google/gemma-3-27b-it",
        # "model": "allenai/molmo-2-8b:free",
        "model": f"{OPENROUTER_MODEL}",
        "messages": messages,
        "plugins": plugins
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    


# @router.post("/")
# def get_answer(prompt: PromptInput, file: UploadFile = File(...)):
#     client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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",
#     )

#     completion = client.chat.completions.create(
#         extra_headers={
#         },
#         # model="upstage/solar-pro-3:free",
#           model= "nvidia/nemotron-nano-12b-v2-vl:free",
        
# messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "What are the main points in this document?"
#             },
#             {
#                 "type": "file",
#                 "file": {
#                     "filename": "document.pdf",
#                     "file_data": "https://image2url.com/r2/default/documents/1769781967116-d939a10e-d0b4-40a5-b780-09c2604c51c1.pdf"
#                 }
#             },
#         ]
#     }
# ]
#     )    
    
#     response = PromptOutput(
#         response=completion.choices[0].message.content.encode("utf-8")
#     )
#     return response




        # from fastapi import APIRouter
        # from app.schemas.ai import PromptInput, PromptOutput
        # from openai import OpenAI


        # router = APIRouter(prefix="/ai", tags=["ai"])

        # @router.post("/")
        # def get_answer(prompt: PromptInput):
        #     client = OpenAI(
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key="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",
        #     )

        #     completion = client.chat.completions.create(
        #         extra_headers={
        #         },
        #         model="upstage/solar-pro-3:free",
        #         messages=[
        #             {
        #             "role": "user",
        #             "content": prompt.prompt
        #             }
        #         ]
        #     )    
            
        #     response = PromptOutput(
        #         response=completion.choices[0].message.content.encode("utf-8")
        #     )
        #     return response

