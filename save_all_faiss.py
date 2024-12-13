import gemini.save_csv_to_faiss as gemini
import azure_open_ai.save_csv_to_faiss as azure_open_ai
import datetime



data_path = "./data/User.csv"
print(f'[{datetime.datetime.now()}] 儲存Gemini FAISS中...')
gemini.save_faiss_index(data_path, "./faiss/gemini_faiss_index_User")
print(f'[{datetime.datetime.now()}] 儲存Azure FAISS中...')
azure_open_ai.save_faiss_index(data_path, "./faiss/azure_faiss_index_User")
print(f'[{datetime.datetime.now()}] 完成FAISS')


