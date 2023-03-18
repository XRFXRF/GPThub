# 打开原始文本文件和目标文本文件
with open('requirements.txt', 'r') as f_in, open('output.txt', 'w') as f_out:
    # 逐行读取原始文件
    for line in f_in:
        # 如果该行不包含 '@' 符号，则写入目标文件
        if '@' not in line:
            f_out.write(line)