import logging_functions as rmtlog


def main():
    
    b = rmtlog.login('user1', 'psw1')
    print(b)

    rmtlog.start_run("t1")

    rmtlog.log("test", "rt")
    rmtlog.log("1/0.4","el")

    rmtlog.upload_file('weights.txt',".chp")

    rmtlog.log("0.95", "acc")

    # # with open("silver_labels.txt", "w") as file:
    # #     file.write("cat.jpg, CatS\r\n")
    # #     file.write("lion.jpg, BigCatS\r\n")
    # #
    # # rmtlog.upload_file('silver_labels.txt')
    #
    # rmtlog.upload_file('python_logging_client.py')

    rmtlog.finish_run()


main()
