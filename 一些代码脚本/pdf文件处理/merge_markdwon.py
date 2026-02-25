import os
import glob

def merge_markdown_basic():
    """合并当前文件夹所有Markdown文件"""
    # 获取所有.md文件
    md_files = glob.glob("*.md")
    
    if not md_files:
        print("❌ 当前文件夹没有找到Markdown文件！")
        return
    
    # 按文件名排序
    md_files.sort()
    
    print(f"📄 找到以下Markdown文件：")
    for i, f in enumerate(md_files, 1):
        print(f"  {i}. {f}")
    
    # 合并内容
    merged_content = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                merged_content.append(content)
                # 在文件之间添加分隔符（可选）
                merged_content.append('\n\n---\n\n')
            print(f"  ✓ 已读取: {md_file}")
        except Exception as e:
            print(f"  ✗ 读取失败 {md_file}: {e}")
    
    # 写入合并文件
    output_file = "merged.md"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(merged_content))
        print(f"\n✅ 合并完成！输出文件: {output_file}")
        print(f"共合并 {len(md_files)} 个文件")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

if __name__ == "__main__":
    merge_markdown_basic()