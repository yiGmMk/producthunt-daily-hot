from product_hunt_list_to_md import Product


a=Product(id='11',
          name='Softr for Notion',
          tagline='将 Notion 数据库转变为门户网站和应用程序，无需编码。',
          description='在你的 Notion 数据库上构建自定义应用程序：比如客户和会员门户、库存跟踪器、目录等。你可以连接到 Notion 数据，定制设计和布局，设置详细的权限，然后将你的应用发布到一个自定义域名上。',
          votesCount=1,
          createdAt='2023-10-05T14:48:00Z',
          featuredAt='2023-10-05T14:48:00Z',
          website='https://www.producthunt.com/r/OBFDFWJ666PSXQ?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+decohack+%28ID%3A+131684%29',
          url='https://www.producthunt.com/posts/softr-for-notion?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+decohack+%28ID%3A+131684%29')
print(a.to_markdown(1))