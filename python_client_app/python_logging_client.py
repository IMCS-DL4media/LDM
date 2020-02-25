from python_client_library.logging_functions import login, start_run, log, upload_file, finish_run

def main():
    print("Starting main ... ")
    logged_in = login('user1', 'psw1')
    if logged_in:
        print("Logged in successfully.")
    else:
        print("Login failed.")

    start_run("t5")

    log("test", "rt")
    log("1/0.4","el")

    upload_file('./python_client_app/weights.txt',".chp")

    log("0.95", "acc")

    # # with open("silver_labels.txt", "w") as file:
    # #     file.write("cat.jpg, CatS\r\n")
    # #     file.write("lion.jpg, BigCatS\r\n")
    # #
    # # rmtlog.upload_file('silver_labels.txt')
    #
    upload_file('./python_client_app/python_logging_client.py', "code")

    finish_run()


main()
