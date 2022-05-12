from my_package.ft_serial_1 import Serial
from my_package.conf_com_port import configure_window
from my_package.chat import chat


def main():
	ser1 = Serial()
	ser2 = Serial()
	ok_button = configure_window(ser1,ser2)
	if ok_button:
		chat(ser1, ser2)


if __name__== "__main__":
	main()
