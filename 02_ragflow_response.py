from ragflow_sdk import RAGFlow
import json
rag_object = RAGFlow(api_key='mykey', base_url='myurl')


datasets = rag_object.list_datasets(name="0.15.1raptor")
dataset_ids = []
for dataset in datasets:
    dataset_ids.append(dataset.id)


with open('./reviews/all_qa_pairs.json', 'r') as file:
    qa_data = json.load(file)

assistant = rag_object.list_chats(name="MissR")

assistant = assistant[0]

session = assistant.create_session()

# 准备评估结果
questions = []
contexts = []
answers = []
ground_truths = []


i = 0
question_num = len(qa_data['qa_pairs'])
for qa_pair in qa_data['qa_pairs']:
    print(f'question {i}/{question_num}')
    question = qa_pair['question']
    correct_answer = qa_pair['answer']

    questions.append(question)

    cont = ""
    ragflow_answer = ""
    retrieved_chunks = []
    for ans in session.ask(question, stream=True):
        ragflow_answer += ans.content[len(cont):]
        cont = ans.content

        # 收集检索到的上下文
        for chunk in ans.reference:
            retrieved_chunks.append(chunk['content'])

    answers.append(ragflow_answer)
    contexts.append(retrieved_chunks)

    ground_truths.append(correct_answer)
    i += 1

test_data = {
    "user_input": questions,
    "retrieved_contexts": contexts,
    "response": answers,
    "reference": ground_truths
}

json_str = json.dumps(test_data, ensure_ascii=False, indent=4)

output_file = 'for_ragas_all.json'

with open(output_file, "w", encoding="utf8") as f:
    f.write(json_str)
print(f"生成的json文件已保存为 {output_file}")