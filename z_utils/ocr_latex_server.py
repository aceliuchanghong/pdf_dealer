import os
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/run-ocr/")
async def run_ocr(image_file: str):
    # 检查输入图像文件路径是否存在
    if not os.path.isfile(image_file):
        raise HTTPException(status_code=400, detail="Input image file does not exist.")

    # 构建GOT-OCR命令
    command = ["python", "GOT-OCR-2.0-master/GOT/demo/run_ocr_2.0.py", "--model-name", "model/", "--image-file",
               image_file, "--type", "format"]
    print(f"Executing command: {command}")

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
    python ocr_latex_server.py
    """
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9522)