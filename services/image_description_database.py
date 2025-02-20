from services.image_describe import ImageDescribeService
import os
import time
from config.settings import Config
from rich import print

class ImageDescriptionDatabase:
    def __init__(self, local_image_folder: str, web_url_file: str, database_file: str, index_file: str,
                 image_describe_api_key=None,
                 image_describe_base_url=None,
                 image_describe_model=None,
                 image_describe_request_delay=None):
        self.image_describe = ImageDescribeService(
            api_key=image_describe_api_key,
            base_url=image_describe_base_url,
            model=image_describe_model,
            request_delay=image_describe_request_delay
        )
        
        self.local_image_folder = local_image_folder
        self.local_image_list = []
        self.load_local_image_folder()
        
        self.web_url_file = web_url_file
        self.web_url_list = []
        self.load_web_url_file()
        
        self.image_url_list = self.web_url_list + self.local_image_list
        
        self.database_file = database_file
        self.index_file = index_file
        
    def load_web_url_file(self):
        if os.path.exists(self.web_url_file):
            with open(self.web_url_file, "r") as f:
                self.web_url_list = f.readlines()
        else:
            self.web_url_list = []
            
    def load_local_image_folder(self):
        if os.path.exists(self.local_image_folder):
            for file in os.listdir(self.local_image_folder):
                if file.endswith(".jpg") or file.endswith(".png"):
                    self.local_image_list.append(file)
        else:
            self.local_image_list = []
    
    def construct_image_description_database(self):
        print(f"Constructing image description database...")
        
        # load database
        if os.path.exists(self.database_file):
            with open(self.database_file, "r") as f:
                description_list = [line.strip() for line in f.readlines()]
                # remove empty lines
                description_list = [line for line in description_list if line]
        else:
            description_list = []
            
        print(f"Database loaded: {len(description_list)} descriptions")
        
        # load index
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                index_list = [line.strip() for line in f.readlines()]
                # remove empty lines
                index_list = [line for line in index_list if line]
        else:
            index_list = []

        print(f"Index loaded: {len(index_list)} images")

        if len(index_list) != len(description_list):
            # 已有的数据库描述和图片对应不上，需要重新构造数据库   
            print(f"Reconstructing database...")
            for image_path in self.image_url_list:
                print(f"Describing image: {image_path}")
                description = self.image_describe.describe_image(os.path.join(self.local_image_folder, image_path))
                description_list.append(description)
                index_list.append(image_path)
                
                # 将描述和图片路径写入数据库和索引
                with open(self.database_file, "w") as f:
                    for description in description_list:
                        f.write(description + "\n")
                with open(self.index_file, "w") as f:
                    for image_path in index_list:
                        f.write(image_path + "\n")
                
            print(f"Database reconstructed: {len(description_list)} descriptions")

        else:
            # 已有的数据库描述和图片对应得上，不需要重新构造数据库
            print(f"Database already exists: {len(description_list)} descriptions")
            # 检查现有的图片路径是否存在于index_list中，如果不存在，创建描述并添加进数据库
            for image_path in self.image_url_list:
                if image_path not in index_list: 
                    print(f"Describing image: {image_path}")
                    description = self.image_describe.describe_image(os.path.join(self.local_image_folder, image_path))
                    description_list.append(description)
                    index_list.append(image_path)
                    
                    # 将描述和图片路径写入数据库和索引  
                    with open(self.database_file, "w") as f:
                        for description in description_list:
                            f.write(description + "\n")
                    with open(self.index_file, "w") as f:
                        for image_path in index_list:
                            f.write(image_path + "\n")
            
            print(f"Database updated: {len(description_list)} descriptions")
                    
        self.database_list = description_list
        self.index_list = index_list
                    
        
        