import os
import tarfile

# tar 파일이 있는 디렉토리 경로 설정
tar_dir = 'D:\\DGU_ICE\\Image_Files'

# 디렉토리 내의 모든 파일 리스트 가져오기
files = os.listdir(tar_dir)

# 리스트에서 tar 파일만을 골라내기
tar_files = [file for file in files if file.endswith('.tar')]

# 각 tar 파일을 압축 해제
for tar_file in tar_files:
    tar_path = os.path.join(tar_dir, tar_file)  # tar 파일의 전체 경로
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(tar_dir)  # tar 파일을 해당 디렉토리에 압축 해제

print('디렉토리 내의 모든 tar 파일을 성공적으로 압축 해제하였습니다.')
