import gradio as gr
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from z_utils.check_db import excute_sqlite_sql
from z_utils.get_text_chunk import get_command_run
from z_utils.sql_sentence import create_rule_table_sql, select_rule_sql, insert_rule_sql, delete_rule_sql, \
    select_all_rule_name_sql

load_dotenv()
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


def create_app():
    with gr.Blocks(title="📋文档实体提取📋") as demo:
        with gr.Tab(label='📙文档处理'):
            with gr.Row():
                gr.Image(label='🤖basic_info', value="z_using_files/pics/ell-wide-light.png")
            gr.Markdown("---")
            with gr.Row():
                file_original = gr.File(file_count='single', file_types=['image', '.pdf'],
                                        label='📕上传文件', scale=5)
                file_original.GRADIO_CACHE = file_default_path
                pic_show = gr.Gallery(label='📙文件预览', scale=5, columns=4, container=True, preview=True)
            gr.Markdown("---")
            with gr.Row():
                with gr.Accordion("🔧基本参数设置", open=False):
                    with gr.Row():
                        rule_option1 = gr.Dropdown(label='1️⃣选择规则',
                                                   choices=['提取合同信息规则', '提取发票信息规则'],
                                                   value='提取合同信息规则', interactive=True,
                                                   info='自定义好规则后需要点击右侧刷新', scale=5)
                        refresh1 = gr.Button("🧲刷新规则", scale=1)
                    save_pic_or_table = gr.Dropdown(label='2️⃣短文档快速识别', choices=['是', '否'],
                                                    value='是', interactive=True,
                                                    info='快速读取文档内容-内含表格未结构化-仅对页数小于3起效')
                generate_button = gr.Button("开始提取", variant='primary', icon='z_using_files/pics/shoot.ico')
        with gr.Tab(label='👉规则设定'):
            with gr.Row():
                gr.Image(label='🤖basic_info', value="z_using_files/pics/ell-wide-light.png")
            gr.Markdown("---")
            with gr.Row():
                rule_basic_name = gr.Textbox(label="⚙️设置/查询规则名称",
                                             placeholder="输入规则名称...eg:提取合同信息规则",
                                             autofocus=True, scale=3)
                tasks = gr.State([])
                query_rule = gr.Button("🔍查询规则", scale=1)
                add_rule = gr.Button("🎨新增规则细节", scale=1)

                def add_task(tasks, new_task_name):
                    if len(new_task_name) == 0:
                        return tasks
                    return tasks + [
                        {
                            "name": new_task_name + "_id" + str(len(tasks)),
                            "rendered": False,
                            "entity_name": "",
                            "entity_format": "",
                            "entity_regex_pattern": "",
                            "entity_order": "",
                        }
                    ]

                def query_rule_click(rule_basic_name, tasks):
                    if rule_basic_name == os.getenv('KEY_WORD'):
                        return gr.update(visible=True), tasks
                    else:
                        try:
                            tasks = []
                            entity_tuple_list = excute_sqlite_sql(select_rule_sql, (rule_basic_name,), False)
                            logger.debug(f"entity_tuple_list:{entity_tuple_list}")
                            for i, entity in enumerate(entity_tuple_list):
                                task = {
                                    "name": rule_basic_name + "_id" + str(i),
                                    "rendered": True,
                                    "entity_name": entity[0],
                                    "entity_format": entity[1],
                                    "entity_regex_pattern": entity[2],
                                    "entity_order": entity[3],
                                }
                                tasks.append(task)
                                logger.debug(f"entity:{entity}")
                            logger.debug(f"tasks:{tasks}")
                            return gr.update(visible=False), tasks
                        except Exception as e:
                            logger.error(e)

                add_rule.click(add_task, [tasks, rule_basic_name], [tasks])
            gr.Markdown("---")
            with gr.Column():
                confirm = gr.Button("🎯提交规则", variant='primary', icon='z_using_files/pics/shoot.ico')

                def confirm_click(tasks, rule_basic_name):
                    target_tasks = [task for task in tasks if
                                    task["rendered"] and task["name"].split("_id")[0] == rule_basic_name]

                    current_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                    sql_delete = excute_sqlite_sql(delete_rule_sql, (target_tasks[0]['name'].split("_id")[0],), False)
                    for target_task in target_tasks:
                        entity = {
                            'rule_name': target_task['name'].split("_id")[0],
                            'entity_name': target_task['entity_name'],
                            'entity_format': target_task['entity_format'],
                            'entity_regex_pattern': target_task['entity_regex_pattern'],
                            'entity_order': target_task['entity_order'],
                            'rule_state': 1,
                            'latest_modified_insert': current_time,
                            'remark': '暂无'
                        }
                        logger.debug(f"{entity}")
                        try:
                            sql_insert = excute_sqlite_sql(insert_rule_sql, (entity['rule_name'],
                                                                             entity['entity_name'],
                                                                             entity['entity_format'],
                                                                             entity['entity_regex_pattern'],
                                                                             entity['entity_order'],
                                                                             entity['rule_state'],
                                                                             entity['latest_modified_insert'],
                                                                             entity['remark'],),
                                                           False)
                            logger.debug(f"sql插入返回结果:{sql_insert}")  # 正常返回[]
                            if sql_insert is None:
                                return [], rule_basic_name + ":新增规则失败"
                        except Exception as e:
                            logger.error(e)
                    return [], rule_basic_name + ":已提交"

                confirm.click(confirm_click, inputs=[tasks, rule_basic_name], outputs=[tasks, rule_basic_name])

            @gr.render(inputs=tasks)
            def render_add_rules(task_list):
                # 参考自:https://blog.csdn.net/cxyhjl/article/details/139712016
                incomplete = [task for task in task_list if not task["rendered"]]  # 过滤出渲染未完成的任务
                complete = [task for task in task_list if task["rendered"]]

                for task in incomplete:
                    with gr.Row():
                        entity_name = gr.Textbox(label='🔑要提取的值', placeholder="提取什么值?eg:SOB编号", scale=3,
                                                 interactive=True)
                        entity_format = gr.Textbox(label='🔑值的样式', placeholder="该值大概什么样式?eg:SOB20..",
                                                   scale=3,
                                                   interactive=True)
                        entity_regex_pattern = gr.Textbox(label='🔑值的正则表达式', scale=3, interactive=True,
                                                          placeholder="该值的正则表达式?(可选/若填入则准确值上升)eg:S[Oo0]B[0-9]{1,}-[0-9]{1,}")
                        entity_order = gr.Textbox(label='🔑值的重命名顺序', placeholder="1,2,3,...", scale=3,
                                                  interactive=True)
                        temp_sure_btn = gr.Button("💪确定", scale=1, variant="secondary")
                        delete_btn = gr.Button("🖍️删除此行", scale=1, variant="stop")

                        def mark_done(entity_name_value, entity_format_value, entity_regex_value, entity_order,
                                      task=task):  # 捕获输入值
                            task["rendered"] = True
                            task["entity_name"] = entity_name_value
                            task["entity_format"] = entity_format_value
                            task["entity_regex_pattern"] = entity_regex_value
                            task["entity_order"] = entity_order
                            logger.debug(
                                f"{task['name']},{task['rendered']},{task['entity_name']},{task['entity_format']},{task['entity_regex_pattern']},{task['entity_order']}")
                            return task_list

                        def delete(task=task):
                            task_list.remove(task)
                            return task_list

                        temp_sure_btn.click(mark_done, [entity_name, entity_format, entity_regex_pattern, entity_order],
                                            [tasks])
                        delete_btn.click(delete, None, [tasks])
                for task in complete:
                    with gr.Row():
                        gr.Textbox(label='🔒要提取的值', value=task["entity_name"], interactive=False, scale=3)
                        gr.Textbox(label='🔒样式', value=task["entity_format"], interactive=False, scale=3)
                        gr.Textbox(label='🔒正则表达式', value=task["entity_regex_pattern"], interactive=False,
                                   scale=3)
                        gr.Textbox(label='🔒重命名顺序', value=task["entity_order"], scale=3,
                                   interactive=True)
                        delete_btn2 = gr.Button("🖍️删除此行", scale=1, variant="stop")

                        def delete2(task=task):
                            task_list.remove(task)
                            return task_list

                        delete_btn2.click(delete2, None, [tasks])
        with gr.Tab(label='🛸秘密后台', visible=False) as secret_tab:
            with gr.Row():
                gr.Image(label='🤖basic_info', value="z_using_files/pics/ell-wide-light.png")
            gr.Markdown("---")
            with gr.Row():
                rule_option2 = gr.Dropdown(label='🎨选择规则', choices=['提取合同信息规则', '提取发票信息规则'],
                                           interactive=True, value='提取合同信息规则',
                                           info='自定义好规则后需要点击右侧刷新', scale=5)
                refresh2 = gr.Button("🧲刷新规则", scale=1)
                button_del = gr.Button("🔑删除此规则", scale=1, variant="stop")
            notice = gr.Textbox(visible=False)
            with gr.Row():
                input_command = gr.Textbox(label='🌐输入命令', placeholder="ls", value="ls", interactive=True, scale=5)
                button_command = gr.Button("🔑执行", scale=1, variant="secondary")
            output_command = gr.Textbox(label="✨执行结果", lines=5)

            def get_all_rule_name():
                rule_name_list = []
                all_rule_name = excute_sqlite_sql(select_all_rule_name_sql)
                for rule_name in all_rule_name:
                    rule_name_list.append(rule_name[0])
                logger.debug(f"rule_name_list:{rule_name_list}")
                return gr.update(value=rule_name_list[0], choices=rule_name_list)

            def delete_rule(rule_name):
                excute_sqlite_sql(delete_rule_sql, (rule_name,), False)
                return gr.Textbox(visible=True, value="已删除:" + rule_name)

        button_command.click(get_command_run, input_command, output_command)
        button_del.click(delete_rule, rule_option2, notice)
        refresh2.click(get_all_rule_name, [], rule_option2)
        refresh1.click(get_all_rule_name, [], rule_option1)
        query_rule.click(query_rule_click, inputs=rule_basic_name, outputs=[secret_tab, tasks])
    return demo


if __name__ == '__main__':
    """
    python entity_extract_ui.py
    nohup python entity_extract_ui.py>entity_extract_ui.log &
    """
    file_default_path = './upload_files'
    os.makedirs(file_default_path, exist_ok=True)
    excute_sqlite_sql(create_rule_table_sql)
    app = create_app()
    app.launch(server_name=os.getenv('HOST'), server_port=int(os.getenv('PORT')), share=False)
