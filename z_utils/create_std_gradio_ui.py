import gradio as gr
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def deal_file(file_path):
    new_file_path = file_path
    return new_file_path, new_file_path


def create_app_test():
    with gr.Blocks(title="文档处理🏅🥇") as demo:
        gr.Markdown("## 上传文件==>开始解析==>文件下载")
        with gr.Row():
            with gr.Column(scale=5):
                media_upload_block = gr.File(file_count='single', file_types=['.doc', '.docx', '.txt', '.md'],
                                             label='上传文件')
                media_upload_block.GRADIO_CACHE = file_default_path
                submit_button = gr.Button(value='开始解析', variant='primary')
            with gr.Column(scale=5):
                media_download_block = gr.File(label='文件处理结束展示')
                download_button = gr.DownloadButton("文件下载", variant='stop')
        submit_button.click(deal_file, media_upload_block, [media_download_block, download_button])
    return demo


if __name__ == '__main__':
    file_default_path = '../upload_files'
    os.makedirs(file_default_path, exist_ok=True)
    app = create_app_test()
    app.launch(server_name="0.0.0.0", server_port=11352, share=False)
