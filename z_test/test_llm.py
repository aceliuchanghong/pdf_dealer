from openai import OpenAI
from dotenv import load_dotenv
import os

from z_utils.check_str2json import parse_json_markdown

# way1
# from langchain_openai import ChatOpenAI
# import time
#
# start = time.time()
# llm = ChatOpenAI(
#     model='mistral-nemo:12b-instruct-2407-fp16',
#     api_key='mistral-nemo:12b-instruct-2407-fp16',
#     openai_api_base="http://112.48.199.7:11434/v1"
# )
# print(llm.invoke("hello").content)
# print(llm.invoke("你好,帮我写一首歌").content)
# end = time.time()
# print('\n回答时间:', end - start)
#
# print(llm.get_num_tokens("你好"))
# print(llm.get_num_tokens("nihao"))

system_prompt = """
基本信息:
"世界上最高的山是珠穆朗玛峰。"
用户将提供一些基本信息和问题输入。请根据基本信息解析“question”和“answer”，并以JSON格式输出(不清楚回答:DK)。
示例问题输入:
世界上最高的山是哪座？
示例JSON输出:
{
    "question": "世界上最高的山是哪座？",
    "answer": "珠穆朗玛峰"
}
"""
Basic_info = """
From:xx Page:30F42021-02-0000: SOB2xxxx02-14875 

\title{
采购合同
}
需方:
供方: xxx股份有限公司
一、货物名称、货物型号、数量、金额:
\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|l|}
\hline 项次 & \begin{tabular}{c}
货物名 \\
称
\end{tabular} & 型号 & 封装 & 流转 & \begin{tabular}{l}
单位 \\
数量
\end{tabular} & \begin{tabular}{c}
含税单价 \\
(元)
\end{tabular} & \begin{tabular}{c}
金额 \\
(元)
\end{tabular} & 税率 & 项目 & \begin{tabular}{l}
交货 \\
时间
\end{tabular} \\
\hline 1 & 电容 & & & 个 & 850 & \(¥ 1.50\) & \(¥ 1,275.00\) & \(13 \%\) & 40 \\
\hline 2 & 电容 & & & 个 & 4100 & \(¥ 1.50\) & \(¥ 6,150.00\) & \(13 \%\) & 40 \\
\hline 3 & 电容 & & & 个 & 450 & \(¥ 2.50\) & \(¥ 1,125.00\) & \(13 \%\) & 40 \\
\hline \(\mathbf{4}\) & 电容 & & & 个 & 1150 & \(¥ 6.00\) & \(¥ 6,900.00\) & \(13 \%\) & 40 \\
\hline \multirow{2}{*}{\(\mathbf{5}\)} & 电容 & & & 个 & 250 & \(¥ 4.80\) & \(¥ 1,200.00\) & \(13 \%\) & 40 \\
\hcline { 2 - 10 } & 电容 & & & 个 & 1100 & \(¥ 6.50\) & \(¥ 7,150.00\) & \(13 \%\) & 40 \\
7 & 电容 & & & 个 & 250 & \(¥ 10.00\) & \(¥ 2,500.00\) & \(13 \%\) & 40 \\
\hbar & 电容 & & & 个 & 200 & \(¥ 10.00\) & \(¥ 2,000.00\) & \(13 \%\) & 40 \\
\hrow{2} & 电容 & & & 个 & 150 & \(¥ 68.00\) & \(¥ 10,200.00\) & \(13 \%\) & 40 \\
10 & 电容 & & & 个 & 2100 & \(¥ 1.50\) & \(¥ 3,150.00\) & \(13 \%\) & 40 \\
& & & & & & 合计 & (小) & & \\
\hline
\end{tabular}
\section*{详细技术指标见原厂、技术规格/标准}
合同总计 (大写)：
(人民币)
二、双方责任: 供方保证在合同规定期限内交货, 并保证所提供的产品是原厂原包装新货: 需方按照原厂技术规格标准、加工图纸、附件等进行产品验收和在合同规定的期限内支付货款;
三、交货地点及运输方式: 供方自定运输方式并承担运输费, 运送至 ; 运输的在途货物毁损、灭先
四、付款方式: 口分期付款: 预付第一期, 货到验收符合合同约定后支付第二其
\[
\begin{array}{l}
\text { 第一期 } \% \text {, 合计 (小写): } \\
\text { 第二期 } \% \text {, 合计 (小写): } \\
\text { 第三期 } \% \text {, 合计 (小写): }
\end{array}
\]
口预付款; 合同签订后, 需方预付人民币 (小写)

"""
user_prompt = "合同里面6块钱一个的电容销售了多少个?格式为纯数字"
# user_prompt = '救生部署是什么?'
#user_prompt = "合同里面SOB或者SOA编号是?格式是SOB20..."
# 加载.env文件
load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'), base_url=os.getenv('BASE_URL'))
response = client.chat.completions.create(
    model="mistral-nemo:12b-instruct-2407-fp16",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": Basic_info + user_prompt},
    ],
    response_format={"type": "json_object"},
    temperature=0.0
)
ans_temp = response.choices[0].message.content
print(ans_temp)
print(parse_json_markdown(ans_temp))
