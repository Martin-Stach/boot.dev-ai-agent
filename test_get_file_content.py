from functions.get_file_content import get_file_content


def test():
    result = get_file_content("calculator", "lorem.txt")
    print("Result for current file:")
    print(f"File length: {len(result)}")
    # print(result)
    print("")

    result = get_file_content("calculator", "main.py")
    print("Result for current file:")
    print(f"File length: {len(result)}")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for current file:")
    print(f"File length: {len(result)}")
    print(result)
    print("")

    result = get_file_content("calculator", "/bin/cat") # (this should return an error string)
    print("Result for current file:")
    print(f"File length: {len(result)}")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for current file:")
    print(f"File length: {len(result)}")
    print(result)
    print("")



if __name__ == "__main__":
    test()