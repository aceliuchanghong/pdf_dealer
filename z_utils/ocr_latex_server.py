import os
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()


def get_most_idle_gpu():
    # 运行 nvidia-smi 命令
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=index,memory.used,utilization.gpu', '--format=csv,noheader,nounits'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # 检查是否有错误
    if result.stderr:
        print("Error running nvidia-smi:", result.stderr)
        return None
    # 处理输出
    gpu_data = result.stdout.strip().split('\n')
    min_utilization = 100  # 初始化最大可能的利用率 (100%)
    idle_gpu_index = -1
    for gpu in gpu_data[::-1]:
        index, memory_used, utilization = gpu.split(', ')
        utilization = int(utilization)
        index = int(index)
        # 找到具有最低利用率的GPU
        if utilization < min_utilization:
            min_utilization = utilization
            idle_gpu_index = index
    return idle_gpu_index


@app.post("/run-ocr/")
async def run_ocr(image_file, ocr_type='format'):
    # 检查输入图像文件路径是否存在
    if not os.path.isfile(image_file):
        raise HTTPException(status_code=400, detail="Input image file does not exist.")

    free_gpu = str(get_most_idle_gpu())
    os.environ["CUDA_VISIBLE_DEVICES"] = free_gpu
    # 构建GOT-OCR命令
    command = ["python", "/mnt/data/llch/GOT-OCR2.0/GOT-OCR-2.0-master/GOT/demo/run_ocr_2.0.py", "--model-name",
               "/mnt/data/llch/GOT-OCR2.0/model/", "--image-file",
               image_file, "--type", ocr_type]
    print(f"Executing command: {command} on cuda:{free_gpu}")

    # 执行命令
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Command output:", process.stdout.decode("utf-8"))
        print("Command error:", process.stderr.decode("utf-8"))
        return JSONResponse(
            content={"message": "OCR completed successfully",
                     "output": process.stdout.decode("utf-8")})
    except subprocess.CalledProcessError as e:
        # 处理命令执行失败的情况
        return JSONResponse(content={"error": e.stderr.decode("utf-8")}, status_code=500)


if __name__ == "__main__":
    """
    source activate got
    python z_utils/ocr_latex_server.py
    nohup python z_utils/ocr_latex_server.py > ocr_latex_server.log &
    """
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9522)
