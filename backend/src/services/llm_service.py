import json
import asyncio
from typing import AsyncGenerator
import subprocess

class LLMService:
    def __init__(self):
        self.model = "llama2"
        self.system_prompt = (
            "Tu es un assistant francophone. "
            "Tu DOIS TOUJOURS répondre en français uniquement. "
            "Ne réponds JAMAIS en anglais. "
            "Si tu as envie d'utiliser des expressions en anglais comme '*smile*', "
            "utilise plutôt leur équivalent en français comme '*sourit*'."
        )
        
    async def generate_response(self, prompt: str) -> str:
        """Génère une réponse en utilisant directement la commande ollama"""
        try:
            print(f"Using model: {self.model}")
            print(f"Prompt: {prompt}")
            
            # Combiner le prompt système avec la question
            full_prompt = f"{self.system_prompt}\n\nQuestion: {prompt}\nRéponse:"
            print(f"Full prompt: {full_prompt}")
            
            # Exécuter la commande
            process = await asyncio.create_subprocess_exec(
                'ollama', 'run', self.model, full_prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                print(f"Error (stderr): {stderr.decode()}")
                raise Exception(f"Command failed with return code {process.returncode}")
                
            response = stdout.decode().strip()
            print(f"Raw response: {response}")
            return response

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Génère une réponse en streaming via la commande ollama"""
        try:
            full_prompt = f"{self.system_prompt}\n\nQuestion: {prompt}\nRéponse:"
            
            process = await asyncio.create_subprocess_exec(
                'ollama', 'run', self.model, full_prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                yield line.decode().strip()
                
            await process.wait()
            if process.returncode != 0:
                stderr = await process.stderr.read()
                raise Exception(f"Stream failed: {stderr.decode()}")

        except Exception as e:
            print(f"Error in stream generation: {str(e)}")
            raise

    def format_chat_prompt(self, messages: list) -> str:
        """Formate l'historique des messages en un prompt cohérent"""
        formatted_messages = []
        formatted_messages.append(self.system_prompt)
        for msg in messages:
            role = "Assistant" if msg["role"] == "assistant" else "Humain"
            formatted_messages.append(f"{role}: {msg['content']}")
        return "\n".join(formatted_messages)