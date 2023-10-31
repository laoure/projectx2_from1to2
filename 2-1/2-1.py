import os
import zipfile
import time
import string
from itertools import combinations


def unlock_zip(zip_file_path: str):
    """ # docstring -> 함수 설명
    unlock and extract zip file fucntion
    extract zip file to current directory

    Args:
        file_path (str): file path
    """
    
    # check file path
    if not os.path.isfile(zip_file_path): # 파일 경로가 존재하는지 확인
        print("file not found")
        return
    
    password_str = list(string.ascii_lowercase + string.digits) # 비밀번호 후보군
    
    # search password
    start_time = time.time()  # 시간 측정 시작
    print('start time: ', time.strftime('%X', time.localtime(start_time)))
    trial = 0 # 시도 횟수
    for pw in combinations(password_str, 6):  # combination을 사용하여 6자리 비밀번호 생성
        password = ''.join(pw) # tuple을 string으로 변환
        try:
            trial += 1 # 시도 횟수 증가
            with zipfile.ZipFile(zip_file_path) as zf:
                zf.extractall(pwd=password.encode()) # 비밀번호가 맞는지 확인 (맞다면 압축 해제)
        except:
            continue # 비밀번호가 틀리면 다음 비밀번호 후보로 넘어감
        
        # if password is correct
        print(f"trial: {trial}")
        print(f"password: {password}")
        end_time = time.time()
        print('end time: ', time.strftime('%X', time.localtime(end_time)))
        print('time taken: ', end_time - start_time, 'seconds')

        with open("password.txt", 'w') as f: # 비밀번호를 password.txt에 저장
            f.write(password)

        return




unlock_zip("emergency_storage_key.zip")