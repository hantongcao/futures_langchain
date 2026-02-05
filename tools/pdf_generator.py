"""
PDF 生成工具 - 将多个 Markdown 文件合并为 PDF
"""
import os
import glob
import re
import logging
from datetime import datetime
from typing import List, Optional

from markdown import markdown
from fpdf import FPDF

logger = logging.getLogger(__name__)


class PDFGenerator:
    """
    PDF 生成器
    
    将多个 Markdown 文件按指定顺序合并为 PDF 报告
    """
    
    def __init__(self, reports_dir: str = None):
        """
        初始化 PDF 生成器
        
        参数:
            reports_dir: 报告目录路径，默认为项目根目录下的 reports/
        """
        if reports_dir is None:
            self.reports_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "reports"
            )
        else:
            self.reports_dir = reports_dir
    
    def find_latest_files(self, symbol: str) -> dict:
        """
        查找最新的报告文件
        
        参数:
            symbol: 期货品种代码
        
        返回:
            dict: 各类型报告的文件路径
        """
        files = {
            'fundamental': None,
            'news': None,
            'sentiment': None,
            'bullish': None,
            'bearish': None,
            'summary': None
        }
        
        # 获取所有文件
        all_files = glob.glob(os.path.join(self.reports_dir, "*.md"))
        
        # 按类型查找最新的文件
        for file_path in sorted(all_files, key=os.path.getmtime, reverse=True):
            basename = os.path.basename(file_path).lower()
            
            if f"fundamental_{symbol.lower()}" in basename and files['fundamental'] is None:
                files['fundamental'] = file_path
            elif f"news_" in basename and files['news'] is None:
                files['news'] = file_path
            elif f"sentiment_" in basename and files['sentiment'] is None:
                files['sentiment'] = file_path
            elif f"bullish_{symbol.lower()}" in basename and files['bullish'] is None:
                files['bullish'] = file_path
            elif f"bearish_{symbol.lower()}" in basename and files['bearish'] is None:
                files['bearish'] = file_path
            elif f"summary_{symbol.lower()}" in basename and files['summary'] is None:
                files['summary'] = file_path
        
        return files
    
    def read_markdown_file(self, file_path: str) -> str:
        """读取 Markdown 文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"\n\n**[读取文件失败: {e}]**\n\n"
    
    def md_to_text(self, md_content: str) -> str:
        """
        将 Markdown 转换为纯文本（保留格式）
        
        简化处理，移除 markdown 语法但保留段落结构
        """
        # 移除代码块标记
        text = re.sub(r'```[\w]*\n', '\n', md_content)
        text = re.sub(r'```\n?', '', text)
        
        # 转换标题为带格式的文本
        text = re.sub(r'^# (.*?)$', r'\n\n【\1】\n', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*?)$', r'\n【\1】\n', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.*?)$', r'\n\1\n', text, flags=re.MULTILINE)
        text = re.sub(r'^#### (.*?)$', r'\n\1\n', text, flags=re.MULTILINE)
        
        # 移除表格标记
        text = re.sub(r'\|', ' | ', text)
        text = re.sub(r'^[\s\-\|]+$', '', text, flags=re.MULTILINE)
        
        # 转换列表
        text = re.sub(r'^\s*[-*+]\s', '  • ', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s', '  ', text, flags=re.MULTILINE)
        
        # 移除加粗和斜体标记
        text = re.sub(r'\*\*\*', '', text)
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\*', '', text)
        text = re.sub(r'__', '', text)
        text = re.sub(r'_', '', text)
        
        # 移除链接标记，保留文本
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # 移除图片标记
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
        
        # 清理多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def create_pdf(self, content: str, output_path: str, symbol: str, title: str = None):
        """
        创建 PDF 文件
        
        参数:
            content: PDF 内容
            output_path: 输出路径
            symbol: 期货品种代码
            title: 标题
        """
        pdf = FPDF()
        
        # 设置页面边距（左右各 15mm）
        pdf.set_left_margin(15)
        pdf.set_right_margin(15)
        
        pdf.add_page()
        
        # 添加中文字体支持
        font_added = False
        
        # Windows 常见中文字体路径
        windows_fonts = [
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
            'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
            'C:/Windows/Fonts/msyhbd.ttc',  # 微软雅黑粗体
        ]
        
        for font_path in windows_fonts:
            if os.path.exists(font_path):
                try:
                    pdf.add_font('CN', '', font_path, uni=True)
                    pdf.add_font('CN', 'B', font_path, uni=True)
                    font_added = True
                    break
                except:
                    continue
        
        if not font_added:
            pdf.set_font('Arial', '', 12)
        else:
            pdf.set_font('CN', '', 12)
        
        # 添加标题
        if title:
            if font_added:
                pdf.set_font('CN', 'B', 20)
            else:
                pdf.set_font('Arial', 'B', 20)
            pdf.cell(0, 15, title, ln=True, align='C')
            pdf.ln(5)
        
        # 添加副标题
        if font_added:
            pdf.set_font('CN', '', 10)
        else:
            pdf.set_font('Arial', '', 10)
        pdf.cell(0, 8, f"品种代码: {symbol.upper()}  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(10)
        
        # 添加内容
        if font_added:
            pdf.set_font('CN', '', 10)
        else:
            pdf.set_font('Arial', '', 10)
        
        # 获取可用宽度（页面宽度减去左右边距）
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        
        # 分行写入内容
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(3)
                continue
            
            # 检测是否是标题行
            if line.startswith('【') and line.endswith('】'):
                if font_added:
                    pdf.set_font('CN', 'B', 14)
                else:
                    pdf.set_font('Arial', 'B', 14)
                pdf.ln(5)
                # 使用 available_width 而不是 0
                pdf.multi_cell(available_width, 10, line, ln=True)
                if font_added:
                    pdf.set_font('CN', '', 10)
                else:
                    pdf.set_font('Arial', '', 10)
            else:
                # 普通文本，自动换行，使用 available_width
                try:
                    pdf.multi_cell(available_width, 6, line, ln=True)
                except Exception as e:
                    # 如果某行出错，跳过该行
                    logger.warning(f"PDF 写入行失败，跳过: {line[:50]}... 错误: {e}")
                    continue
        
        # 保存 PDF
        pdf.output(output_path)
    
    def merge_reports_to_pdf(
        self, 
        symbol: str, 
        output_filename: str = None,
        order: List[str] = None
    ) -> str:
        """
        合并报告为 PDF
        
        参数:
            symbol: 期货品种代码
            output_filename: 输出文件名，默认自动生成
            order: 报告顺序，默认 ['fundamental', 'news', 'sentiment', 'bullish', 'bearish', 'summary']
        
        返回:
            str: 生成的 PDF 文件路径
        """
        # 默认顺序：基本面 -> 新闻 -> 情绪 -> 看涨 -> 看跌 -> 总结
        if order is None:
            order = ['fundamental', 'news', 'sentiment', 'bullish', 'bearish', 'summary']
        
        # 查找最新文件
        files = self.find_latest_files(symbol)
        
        # 构建完整内容
        full_content = ""
        
        section_titles = {
            'fundamental': '一、基本面技术分析报告',
            'news': '二、新闻分析报告',
            'sentiment': '三、市场情绪分析报告',
            'bullish': '四、看涨分析报告（多头视角）',
            'bearish': '五、看跌分析报告（空头视角）',
            'summary': '六、综合投资报告'
        }
        
        for section in order:
            file_path = files.get(section)
            
            # 添加章节标题
            full_content += f"\n\n{'='*60}\n"
            full_content += f"【{section_titles.get(section, section)}】\n"
            full_content += f"{'='*60}\n\n"
            
            if file_path and os.path.exists(file_path):
                md_content = self.read_markdown_file(file_path)
                text_content = self.md_to_text(md_content)
                full_content += text_content
            else:
                full_content += f"\n[该部分报告未生成或文件未找到]\n"
        
        # 生成输出文件名
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"futures_report_{symbol}_{timestamp}.pdf"
        
        output_path = os.path.join(self.reports_dir, output_filename)
        
        # 创建 PDF
        title = f"期货综合分析报告 - {symbol.upper()}"
        self.create_pdf(full_content, output_path, symbol, title)
        
        return output_path


def generate_pdf_report(symbol: str) -> str:
    """
    便捷函数：生成 PDF 报告
    
    参数:
        symbol: 期货品种代码
    
    返回:
        str: 生成的 PDF 文件路径
    """
    generator = PDFGenerator()
    return generator.merge_reports_to_pdf(symbol)


if __name__ == "__main__":
    # 测试
    import sys
    
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
    else:
        symbol = "ss"  # 默认不锈钢
    
    print(f"正在生成 {symbol} 的 PDF 报告...")
    pdf_path = generate_pdf_report(symbol)
    print(f"PDF 报告已生成: {pdf_path}")
