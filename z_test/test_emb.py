# pip install -U pymilvus
# pip install -U langchain_ollama
import os
import time

from z_utils.get_text_chunk import run_js_script
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

load_dotenv()


def emb_chunks(embed, chunk_list):
    def process_chunk(i, chunk):
        temp = {}
        vec = embed.embed_query(chunk)
        temp['id'] = str(i)
        temp['text'] = chunk
        temp['vector'] = vec
        return temp

    start_time = time.time()  # 记录开始时间
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(lambda x: process_chunk(*x), enumerate(chunk_list)),
                            total=len(chunk_list), desc="embedding......"))
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    print(f"embedding完成，耗时: {elapsed_time:.2f}秒\n")
    return results


if __name__ == '__main__':
    embed = OllamaEmbeddings(
        model=os.getenv('EMB_MODEL'),
        base_url=os.getenv('EMB_BASE_URL'),
    )
    md_path = r'C:\Users\liuch\Documents\img20240708_16193473_latex.md'
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
    output = run_js_script('../z_test/chunk.js', md_path)

    emb_ans = emb_chunks(embed, output[:2])

    print(emb_ans)
