import re
from dotenv import load_dotenv

load_dotenv()


def upload_image_to_minio(image_path):
    # 上传图片到MinIO并返回新的链接
    # bucket_name = os.getenv('bucketName')
    # object_name = os.path.basename(image_path)
    # minio_client.fput_object(bucket_name, object_name, image_path)
    # new_link = minio_client.presigned_get_object(bucket_name, object_name)
    new_link = 'QBQ' + image_path + 'QAQ'
    return new_link


def replace_image_links_in_md(md_file_path, new_md_path):
    """
    1.读取 original_latex_md 文档里面的图片链接 一般是:![desc](path_url)
    2.图片链接解析文件路径path_url
    3.path_url上传到minio的逻辑,获取返回的链接
    4.替换文件,生成新的md文件
    :param md_file_path:
    :param new_md_path:
    :return:
    """
    # 读取Markdown文件内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配图片链接的正则表达式
    pattern = r'!\[.*?\]\((.*?)\)'  # 匹配 ![desc](path_url)

    # 查找所有匹配的图片路径
    image_paths = re.findall(pattern, content)

    # 用上传后的URL替换本地路径
    for image_path in image_paths:
        new_url = upload_image_to_minio(image_path)
        content = content.replace(image_path, new_url)

    # 将新的Markdown内容写入新的文件
    with open(new_md_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return new_md_path


if __name__ == '__main__':
    md_file_path = r'C:\Users\liuch\Documents\img20240708_16193473_latex.md'
    new_md_path = md_file_path.replace('_latex.md', '_latex_up.md')
    replace_image_links_in_md(md_file_path, new_md_path)
    # print(new_md_path)
    with open(new_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content)
