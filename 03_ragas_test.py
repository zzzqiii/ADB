import os
from datasets import load_dataset
from ragas import EvaluationDataset
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings
import json
from datasets import load_from_disk
import pandas as pd
from datasets import Dataset
# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "mykey"
os.environ["RAGAS_APP_TOKEN"] = "mykey"

# 加载数据集
with open('for_ragas_all.json', 'r') as file:
    dataset = json.load(file)

eval_dataset = Dataset.from_dict(dataset)

batch_size = 250  # 每个批次的大小
num_batches = len(eval_dataset) // batch_size + 1
batches = [eval_dataset.select(range(i * batch_size, min((i + 1) * batch_size, len(eval_dataset)))) for i in range(num_batches)]


evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="deepseek-chat", openai_api_base='https://api.deepseek.com', max_tokens=8192))
evaluator_embeddings = LangchainEmbeddingsWrapper(DashScopeEmbeddings(model="text-embedding-v3"))

# 选择评估指标
metrics = [
    ContextRecall(),
    ContextPrecision(),
    Faithfulness(),
    AnswerRelevancy(),
]


output_dir = "ragas_results"
os.makedirs(output_dir, exist_ok=True)


for batch_idx, batch in enumerate(batches):
    print(f"Evaluating batch {batch_idx + 1}/{num_batches}...")
    batch_results = evaluate(dataset=batch, llm=evaluator_llm, embeddings=evaluator_embeddings, metrics=metrics)
    batch_df = batch_results.to_pandas()
    output_file = os.path.join(output_dir, f"batch_{batch_idx + 1}.csv")
    batch_df.to_csv(output_file, index=False)
    print(f'Batch {batch_idx + 1} results: {batch_results}')

    print(f"Batch {batch_idx + 1} results saved to {output_file}")