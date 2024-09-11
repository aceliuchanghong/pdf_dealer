import os
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/convert-pdf/")
async def convert_pdf(input_pdf_path: str, output_dir: str = "/mnt/data/llch/ForMinerU/output", mode: str = "auto"):
    # 检查输入PDF文件路径是否存在
    if not os.path.isfile(input_pdf_path):
        raise HTTPException(status_code=400, detail="Input PDF file does not exist.")
    name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 构建magic-pdf命令
    command = ["magic-pdf", "-p", input_pdf_path, "-o", output_dir, "-m", mode]
    print(f"Executing command: {command}")
    # 执行命令
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Command output:", process.stdout.decode("utf-8"))
        print("Command error:", process.stderr.decode("utf-8"))
        return JSONResponse(
            content={"message": "PDF converted successfully",
                     "output_dir": os.path.join(output_dir, name, mode),
                     "output_md_path": os.path.join(output_dir, name, mode, name + ".md")})
    except subprocess.CalledProcessError as e:
        # 处理命令执行失败的情况
        return JSONResponse(content={"error": e.stderr.decode("utf-8")}, status_code=500)


if __name__ == "__main__":
    """
    From https://github.com/opendatalab/MinerU
    source activate MinerU
    nohup python magic_pdf_server.py > magic_pdf_server.log &
    """
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9521)
