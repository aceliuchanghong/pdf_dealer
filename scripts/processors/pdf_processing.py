from abc import ABC, abstractmethod


# 抽象类：定义PDF处理的模板
class PDFProcessor(ABC):

    # 模板方法：定义处理PDF的流程
    def process_pdf(self, pdf_file):
        self.load_pdf(pdf_file)
        self.preprocess()

    # 加载PDF（所有子类共享的实现）
    def load_pdf(self, pdf_file):
        print(f"Loading PDF: {pdf_file}")

    # 处理PDF，抽象方法
    @abstractmethod
    def preprocess(self):
        pass
