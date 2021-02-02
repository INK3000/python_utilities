import os


def get_files(path):
	result = os.walk()
	return result




def main():
	print(get_files())


if __name__ == '__main__':
	main()