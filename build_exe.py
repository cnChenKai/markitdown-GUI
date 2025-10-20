import PyInstaller.__main__
import os
import sys

def build_exe():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # PyInstaller 参数
    args = [
        'markitdown_gui.py',  # 主脚本
        '--onefile',  # 打包成单个exe文件
        '--windowed',  # 不显示控制台窗口
        '--name=MarkitdownGUI',  # exe文件名
        # '--icon=icon.ico',  # 图标文件（如果有的话）
        '--add-data', f'packages/markitdown/src/markitdown;markitdown',  # 添加markitdown包
        '--add-data', f'C:/Users/yxxck/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/magika/models;magika/models',  # 添加magika模型
        '--add-data', f'C:/Users/yxxck/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/magika/config;magika/config',  # 添加magika配置
        # 包含所有可选依赖的数据文件
        '--hidden-import=markitdown',
        '--hidden-import=markitdown._markitdown',
        '--hidden-import=markitdown.converters',
        '--hidden-import=markitdown.converters._pdf_converter',
        '--hidden-import=markitdown.converters._docx_converter',
        '--hidden-import=markitdown.converters._pptx_converter',
        '--hidden-import=markitdown.converters._xlsx_converter',
        '--hidden-import=markitdown.converters._html_converter',
        '--hidden-import=markitdown.converters._image_converter',
        '--hidden-import=markitdown.converters._audio_converter',
        '--hidden-import=markitdown.converters._epub_converter',
        '--hidden-import=markitdown.converters._plain_text_converter',
        '--hidden-import=markitdown.converters._csv_converter',
        '--hidden-import=markitdown.converters._outlook_msg_converter',
        '--hidden-import=markitdown.converters._youtube_converter',
        '--hidden-import=markitdown.converters._zip_converter',
        '--hidden-import=markitdown.converters._bing_serp_converter',
        '--hidden-import=markitdown.converters._wikipedia_converter',
        '--hidden-import=markitdown.converters._doc_intel_converter',
        '--hidden-import=markitdown.converters._llm_caption',
        '--hidden-import=markitdown.converters._transcribe_audio',
        '--hidden-import=markitdown.converters._exiftool',
        '--hidden-import=markitdown.converters._markdownify',
        # 第三方库隐藏导入
        '--hidden-import=beautifulsoup4',
        '--hidden-import=requests',
        '--hidden-import=markdownify',
        '--hidden-import=magika',
        '--hidden-import=charset_normalizer',
        '--hidden-import=defusedxml',
        '--hidden-import=python_pptx',
        '--hidden-import=mammoth',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=xlrd',
        '--hidden-import=lxml',
        '--hidden-import=pdfminer.six',
        '--hidden-import=olefile',
        '--hidden-import=pydub',
        '--hidden-import=speech_recognition',
        '--hidden-import=youtube_transcript_api',
        '--hidden-import=azure.ai.documentintelligence',
        '--hidden-import=azure.identity',
        # Tkinter相关
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.ttk',
        # 其他系统库
        '--hidden-import=threading',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=codecs',
        '--hidden-import=textwrap',
        '--hidden-import=importlib.metadata',
        # 数据文件
        '--add-data', 'packages/markitdown/src/markitdown/converters/_markdownify.py;markitdown/converters',
        '--add-data', 'packages/markitdown/src/markitdown/converter_utils;markitdown/converter_utils',
    ]

    # 如果在Windows上，添加Windows特定的选项
    if os.name == 'nt':
        args.extend([
            '--hidden-import=win32api',
            '--hidden-import=win32con',
        ])

    # 运行PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_exe()