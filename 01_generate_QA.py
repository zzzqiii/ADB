import streamlit as st
import requests
import tempfile
import os
import json
import math
from openai import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from typing import List
import random

client = OpenAI(
    api_key="mykey",
    base_url="https://api.deepseek.com",
)

# Document loaders mapping
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (UnstructuredEmailLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}
def read_pdf(file_path):
    doc = fitz.open(file_path) 
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_completion(prompt, model="deepseek-chat"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"调用API时发生错误: {e}")
        return None

def generate_qa_pairs(text_chunks, num_chunks=10):
    qa_pairs = []
    selected_chunks = random.sample(text_chunks, min(len(text_chunks), num_chunks))
    # progress_bar = st.progress(0)
    for i, chunk in enumerate(selected_chunks):
        prompt = f"""
            Below is a section of a detailed scientific paper:

            {chunk}

            Your task is to formulate 1 sophisticated Q&A pair that delves into the underlying scientific principles and knowledge presented in this section.

            Ensure the question and answer are diverse, avoiding any duplication.   The question should encourage deeper exploration and a nuanced understanding of the section's findings.   The answer must be directly based on the given text, ensuring accuracy and consistency in the information provided.   Avoid introducing any information not present in the text.

            The question can cover, but is not limited to, the following topics:
            1.   The mechanisms behind the formation of harmful algal blooms (HABs).
            2.   The environmental factors that promote or inhibit HAB formation.
            3.   The ecological impact of HABs on marine ecosystems.
            4.   The effects of HABs on biodiversity, including fish kills and toxin accumulation.
            5.   The relationship between nutrient pollution and the development of HABs.
            6.   The role of temperature, pH, and other abiotic factors in influencing HAB dynamics.
            7.   Possible mitigation strategies for controlling or preventing HAB outbreaks.

            Please format your response as follows:
            1.   The question should cover the key concepts and details in the section.
            2.   The answer should be **directly based on the given text**, ensuring **accuracy** and **consistency**.
            3.   Use "Q:" to mark the start of the question.
            4.   Use "A:" to mark the start of the answer, with clear paragraphs to improve readability.
            5.   Ensure that the Q&A pair is separated by two blank lines for readability.

            Please generate a Q&A pair based on this section of the paper.
            """

        response = get_completion(prompt)
        if response:
            try:
                parts = response.split("A:", 1)
                if len(parts) == 2:
                    question = parts[0].replace("Q:", "").strip()
                    answer = parts[1].strip()
                    qa_pairs.append({"question": question, "answer": answer, 'chunk': chunk})
                    print({"i": i, "question": question})
                else:
                    # st.warning(f"无法解析响应: {response}")
                    print(f"无法解析响应: {response}")
            except Exception as e:
                # st.warning(f"处理响应时出错: {str(e)}")
                print(f"处理响应时出错: {str(e)}")
        
        # progress = (i + 1) / len(text_chunks)
        # progress_bar.progress(progress)
    
    return qa_pairs

def load_single_document(file_path: str) -> List[Document]:
    """加载单个文档"""
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()
    raise ValueError(f"Unsupported file extension '{ext}'")

def process_file(uploaded_file):
    """处理上传的文件并生成文本块"""
    try:
        documents = load_single_document(uploaded_file)
        if not documents:
            print("文件处理失败，请检查文件格式是否正确。")
            return []

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        text_chunks = text_splitter.split_documents(documents)
        return text_chunks
    except Exception as e:
        print(f"处理文件时发生错误: {e}")
        return []


def save_qa_pairs_as_json(qa_pairs, output_file):
    """保存生成的 Q&A 对为 JSON 文件"""
    """下载生成的问答对为JSON文件"""
    if qa_pairs:
        json_data = {"qa_pairs": []}
        
        for qa in qa_pairs:
            # 如果 QA 对的 "chunk" 是一个 Document 对象，提取其中的文本内容
            chunk_content = qa.get("chunk")
            if isinstance(chunk_content, Document):
                chunk_content = chunk_content.page_content  # 获取文档中的文本内容

            json_data["qa_pairs"].append({
                "question": qa.get("question"),
                "answer": qa.get("answer"),
                "chunk": chunk_content  # 将文本内容存储到 JSON 中
            })
        
        # Pretty print the JSON data for better readability
        json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
        
        # Save to a JSON file
        with open(output_file, "w", encoding="utf8") as f:
            f.write(json_str)
        print(f"生成的QA对已保存为 {output_file}")



def generate_qa_for_directory(directory, folder_name):
    """批量处理给定文件夹中的所有文件"""
    all_qa_pairs = []
    i = 0
    # 遍历指定文件夹
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        
        if not file_path.lower().endswith(('.pdf', '.txt', '.docx')):  # 检查文件扩展名
            continue

        print(f"正在处理文件: {file_name}")
        
        # 读取文件并生成文本块
        text_chunks = process_file(file_path)
        qa_pairs = generate_qa_pairs(text_chunks, num_chunks=5)
        save_qa_pairs_as_json(qa_pairs, output_file=os.path.join(directory, f'paper{i}_qa_pair.json'))
        all_qa_pairs.extend(qa_pairs)
        i += 1

    # 保存该文件夹下的 Q&A 对为独立的 JSON 文件
    folder_qa_json = f"{folder_name}_qa_pairs.json"
    save_qa_pairs_as_json(all_qa_pairs, output_file=os.path.join(directory, folder_qa_json))
    print(f"所有问答对已合并并保存为 {directory}/{folder_qa_json}")


def merge_qa_json_files(base_directory):
    all_qa_pairs = []

    for folder_name in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder_name)

        if os.path.isdir(folder_path):
            qa_json_file = os.path.join(folder_path, f"{folder_name}_qa_pairs.json")
            
            if os.path.exists(qa_json_file):
                with open(qa_json_file, 'r', encoding="utf8") as f:
                    data = json.load(f)
                    all_qa_pairs.extend(data.get("qa_pairs", []))
    
    merged_json_file = os.path.join(base_directory, "all_qa_pairs.json")
    with open(merged_json_file, "w", encoding="utf8") as f:
        json.dump({"qa_pairs": all_qa_pairs}, f, ensure_ascii=False, indent=4)

    print(f"所有问答对已合并并保存为 {merged_json_file}")

def main():
    base_directory = 'reviews'  # 根目录
    for i in range(0, 12):
        print(f'processing fold {i}')
        folder_name = str(i)
        generate_qa_for_directory(os.path.join(base_directory, folder_name), folder_name)
    merge_qa_json_files(base_directory)


if __name__ == "__main__":
    main()
