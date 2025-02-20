from services.image_search import ImageSearch

def main():
    search_engine = ImageSearch()
    
    while True:
        user_input = input("请输入需要回应的内容（输入q退出）: ")
        if user_input.lower() == 'q':
            break
            
        result = search_engine.search(user_input)
        if result:
            print(f"推荐表情包: {result}")
        else:
            print("未找到匹配的表情包")

if __name__ == "__main__":
    main()
