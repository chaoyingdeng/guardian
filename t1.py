import os


def generate_large_file(filename, size_in_mb):
    size_in_bytes = size_in_mb * 1024 * 1024  # 将 MB 转换为字节
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_in_bytes))  # 写入随机字节


# 生成一个 30MB 的文件
generate_large_file('/Users/dengchaoying/Downloads/large_file1.pptx', 30)

print("文件生成成功")
