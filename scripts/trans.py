import re

categories= ["AI","人工智能","机器学习","工具"]

"""
将markdown文件转换为hugo格式
"""
# Define category to keywords mapping
# Add more categories and corresponding keywords as needed
category_mapping = {
    "人工智能": ["AI", "人工智能", "机器学习"],
    "工具": ["工具", "生产力工具", "效率"],
    "开发": ["API","数据库","REST API","SQL"]
}

def convert_to_hugo_format(markdown_content,top_keywords):
    # 提取日期
    date_match = re.search(r'\| (\d{4}-\d{2}-\d{2})', markdown_content)
    if date_match:
        date_str = date_match.group(1)
    else:
        raise ValueError("Date not found in the content")
    # 提取第一张图片
    image_url = extract_first_image(markdown_content)
    
    # 构建Hugo前缀
    hugo_prefix = f"""---
title: 今日热榜 | {date_str}
date: {date_str} 06:25:17+0000
"""
    if image_url:
        hugo_prefix += f'image: {image_url}\n'

    if len(top_keywords)>0:
        hugo_keywords = ', '.join([f'"{keyword}"' for keyword, _ in top_keywords[:3]])
        hugo_prefix += f'tags: [{hugo_keywords}]\n'
    
    # Check for top keywords related to specific categories
    categories = set()
    keyword_set = set(keyword for keyword, _ in top_keywords)
    for category, keywords in category_mapping.items():
        if any(keyword in keyword_set for keyword in keywords):
            categories.add(category)

    if categories:
        vals = list(categories)
        vals.sort()
        formatted_categories = ', '.join(f'"{category}"' for category in vals)
        hugo_prefix += f'categories: [{formatted_categories}]\n'

    hugo_prefix += '---\n'

    # 移除原始标题
    markdown_content = re.sub(r'# 今日热榜 \| \d{4}-\d{2}-\d{2}\n\n', '', markdown_content)

    # Add two spaces before line break for specific lines
    lines = markdown_content.splitlines()
    lines_to_modify = ["标语", "介绍", "产品网站", "Product Hunt", "关键词", "票数", "是否精选", "发布时间"]
    updated_lines = []

    for line in lines:
        # 删除二级标题的链接
        # Remove links from level 2 headings
        if line.startswith('## '):
            line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line)
        # Check for any keywords in the line and append two spaces if found
        if any(f"**{keyword}**" in line for keyword in lines_to_modify):
            updated_lines.append(line + '  ')
        else:
            updated_lines.append(line)
    
    updated_content = '\n'.join(updated_lines)

    return hugo_prefix + updated_content

def extract_first_image(markdown_content):
    # 使用正则表达式提取第一张图片的URL
    image_match = re.search(r'!\[.*?\]\((.*?)\)', markdown_content)
    if image_match:
        return image_match.group(1)
    else:
        return None

import os
from collections import Counter

# 提取关键字
def extract_keywords_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 查找包含关键词的那一行
    keywords=[]
    
    for line in lines:
        if "关键词" in line:
            keywords_line = line.strip()
            keywords_line = keywords_line.replace('**关键词**：',"").strip()
            val=[keyword.strip() for keyword in keywords_line.split(',') if keyword.strip() and len(keyword)<10]
            keywords.extend(val)    
    return keywords

def count_and_sort_keywords(keywords):
    # 计算每个关键词的出现次数
    keyword_counts = Counter(keywords)
    # 按出现次数排序
    sorted_keywords = keyword_counts.most_common()
    return sorted_keywords

def process_markdown_files(input_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有Markdown文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            keywords=extract_keywords_from_file(input_path)
            top_keywords=count_and_sort_keywords(keywords)

            with open(input_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()

            try:
                converted_content = convert_to_hugo_format(markdown_content,top_keywords)
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(converted_content)
                print(f"Converted and saved: {filename}")
            except ValueError as e:
                print(f"Error processing {filename}: {e}")

# 指定输入和输出目录
input_dir = 'data'
output_dir = 'hugo'

# 处理Markdown文件
process_markdown_files(input_dir, output_dir)