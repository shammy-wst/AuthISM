import asyncio
from services.llm_service import LLMService

async def test_simple_generation():
    print("\n=== Testing Simple Generation ===")
    llm_service = LLMService()
    
    prompt = "Dis bonjour en français"
    print(f"\nPrompt: {prompt}")
    
    try:
        response = await llm_service.generate_response(prompt)
        print(f"\nResponse: {response}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

async def test_streaming():
    print("\n=== Testing Streaming ===")
    llm_service = LLMService()
    
    prompt = "Compte jusqu'à 5 en français"
    print(f"\nPrompt: {prompt}")
    
    try:
        async for chunk in llm_service.generate_stream(prompt):
            print(chunk, end="", flush=True)
        print("\nStreaming completed")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

async def run_tests():
    await test_simple_generation()
    print("\n" + "="*50 + "\n")
    await test_streaming()

if __name__ == "__main__":
    asyncio.run(run_tests()) 