from pdf2docx import Converter

pdf_file = 'ilovepdf_merged_merged.pdf'
docx_file = 'test.docx'

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file) # 默认参数start=0, end=None
cv.close()

# more samples
# cv.convert(docx_file, start=1) # 转换第2页到最后一页
# cv.convert(docx_file, pages=[1,3,5]) # 转换第2，4，6页