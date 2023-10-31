def caesar_cipher_decode(target_text, keywords):
    decrypted_texts = []
    print("자리수에 따른 암호 출력(shift : 1~26)")
    for shift in range(26):
        decrypted_text = ""
        for char in target_text:
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') + shift + 1) % 26 + ord('A'))
            elif char.islower():
                decrypted_char = chr((ord(char) - ord('a') + shift + 1) % 26 + ord('a'))
            else:
                decrypted_char = char
            decrypted_text += decrypted_char
        decrypted_texts.append(decrypted_text)
        print(decrypted_texts[shift])

        for keyword in keywords:
            if keyword in decrypted_text:
                print(f"Keyword '{keyword}' found in result (Shift {shift+1})")
                return decrypted_texts

    return decrypted_texts


try:
    f = open("password.txt", "r")
except IOError as err:
    print("FileNotFoundError: No such file or directory")
except Exception as e:
    print(f"Unexpected Error occurred:\n{e}")
else:
    target_pwd = f.read()
    f.close()
    keywords = ["desired_keyword1", "Hello world!1"]  # Add your desired keywords here

    lines = caesar_cipher_decode(target_pwd, keywords)
    while True:
        answer_line = int(input("몇 번째 자리수(줄)가 암호입니까?(1~26) : "))
        if 1 <= answer_line <= 26:
            try:
                with open("result.txt", "w") as result_file:
                    result_file.write(lines[answer_line - 1])
                    print(f"결과가 result.txt에 저장되었습니다.")
            except IOError as err:
                print(f"IOError: {err}")
            except Exception as e:
                print(f"Unexpected Error occurred while writing result.txt:\n{e}")
            break
        else:
            print("올바른 범위의 자리수를 입력하세요 (1~26).")