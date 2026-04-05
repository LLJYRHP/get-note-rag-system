from src.api.get_api import GetNoteAPI

def test_api():
    try:
        api = GetNoteAPI()
        results = api.search_notes("健康管理", top_k=1)
        print("API Test Success!")
        print("Results:", results)
    except Exception as e:
        print("API Test Failed:", e)

if __name__ == "__main__":
    test_api()
