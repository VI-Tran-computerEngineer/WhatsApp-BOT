import threading

from whatsapp_postman import WhatsApp_user_callback


def main():
    print("******************************")
    print("*     Starting the BOT       *")
    print("******************************")
    callback = WhatsApp_user_callback()
    threading.Thread(target=callback.send_preschedule_msgs,
                     daemon=True).start()

    try:
        callback.wait_4_msgs_received()
        exit(0)
    except KeyboardInterrupt:
        print("******************************")
        print("*    End the BOT manually    *")
        print("******************************")
        exit(1)


if __name__ == "__main__":
    main()
