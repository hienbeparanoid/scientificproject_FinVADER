import pandas as pd
import glob

# Đường dẫn tới thư mục chứa các file CSV
folder_path = 'C:\\Users\\PHAM HAI LONG\\Downloads\\mack_comments'

# Tạo một từ điển để lưu trữ DataFrame theo từ khóa trong tên file
data_frames = {
    'aapl': [],
    'amd': [],
    'msft': [],
    'nio': [],
    'tsla': []
}

# Đọc và phân loại các file CSV theo từ khóa trong tên
for file_path in glob.glob(folder_path + "/*.csv"):
    file_name = file_path.split("/")[-1]  # Lấy tên file từ đường dẫn
    for keyword in data_frames.keys():
        if keyword in file_name:
            df = pd.read_csv(file_path)
            data_frames[keyword].append(df)
            break  # Khi đã tìm thấy từ khóa, không cần kiểm tra các từ khóa khác

# Gộp và xuất từng file CSV tương ứng với từ khóa đã lọc
for keyword, dfs in data_frames.items():
    if len(dfs) > 0:
        merged_df = pd.concat(dfs)
        output_file = keyword + "_merged.csv"
        merged_df.to_csv(output_file, index=False)