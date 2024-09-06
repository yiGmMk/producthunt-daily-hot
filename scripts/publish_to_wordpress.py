from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import os
from datetime import datetime, timezone

def publish_to_wordpress():
    wordpress_url = os.getenv('WORDPRESS_URL')
    wordpress_username = os.getenv('WORDPRESS_USERNAME')
    wordpress_password = os.getenv('WORDPRESS_PASSWORD')

    wp = Client(wordpress_url, wordpress_username, wordpress_password)
    post = WordPressPost()

    # 获取今天的日期并格式化
    today = datetime.now(timezone.utc)
    date_today = today.strftime('%Y-%m-%d')

    # 获取最新的Markdown文件内容
    file_name = f'data/producthunt-daily-{date_today}.md'
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    post.title = "PH今日热榜"
    post.content = content
    post.post_status = 'publish'  # 设置为发布状态

    wp.call(NewPost(post))

if __name__ == "__main__":
    publish_to_wordpress()
