from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
import os

load_dotenv(override=True)  # take environment variables from .env.

# The following variables from your .env file are used in this notebook
endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
credential = (
    AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY", ""))
    if len(os.getenv("AZURE_SEARCH_ADMIN_KEY", "")) > 0
    else DefaultAzureCredential()
)
index_name = os.getenv("AZURE_SEARCH_INDEX", "vectest")
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_key = (
    os.getenv("AZURE_OPENAI_KEY", "")
    if len(os.getenv("AZURE_OPENAI_KEY", "")) > 0
    else None
)
azure_openai_embedding_deployment = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large"
)
azure_openai_embedding_dimensions = int(
    os.getenv("AZURE_OPENAI_EMBEDDING_DIMENSIONS", 1024)
)
embedding_model_name = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "aoai-text-embedding-3-large"
)
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import json

openai_credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    openai_credential, "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    # azure_deployment=azure_openai_embedding_deployment,
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_endpoint,
    api_key=azure_openai_key,
    azure_ad_token_provider=token_provider if not azure_openai_key else None,
)

# Generate Document Embeddings using OpenAI Ada 002
# Read the text-sample.json
path = os.path.join("./", "data.json")
with open(path, "r", encoding="utf-8") as file:
    input_data = json.load(file)

print(type(input_data))  # 確認用: データ型を表示（期待される型は 'dict'）
# print(input_data)  # 確認用: データ内容を表示


# ベクトル化したいフィールドを文字列に結合
texts = []
for person_key, person_data in input_data.items():
    # すべてのフィールドを文字列として結合
    combined_text = " ".join(
        [
            str(person_data["age"]),
            person_data["gender"],
            str(person_data["height"]),
            str(person_data["weight"]),
            person_data["disease"],
            person_data["medicines"],
            person_data["diet"],
            person_data["exercise"],
            person_data["sleep"],
            person_data["alcohol"],
            person_data["smoking"],
            person_data["blood_pressure"],
            person_data["blood_sugar_levels"],
            person_data["cho_levels"],
            person_data["stress"],
            person_data["mood"],
        ]
        + person_data["symptoms"]
    )  # symptomsはリストなので結合する
    texts.append(combined_text)

print(texts)

# 埋め込みモデル名
embedding_model_name = "aoai-text-embedding-3-large"

# テキストデータの埋め込みを生成
embeddings = []
for text in texts:
    response = client.embeddings.create(
        input=text,
        model=embedding_model_name,
    )
    embeddings.append(response.data[0].embedding)

# 各データ項目に埋め込みベクトルを追加
for i, (person_key, person_data) in enumerate(input_data.items()):
    person_data["combined_vector"] = embeddings[i]

# print(embeddings)
# 結果を表示または保存
# print(json.dumps(input_data, indent=4))
