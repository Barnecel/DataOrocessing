import os

def get_files():
    for filepath,dirnames,filenames in os.walk(r'C:\Users\Enabot\Desktop\test'):
        for filename in filenames:

            p1=os.path.join(filepath,filename)
            p2=os.path.join(filepath,filenames[2])
            print(p1)
            print("这是",p2)
if __name__ == '__main__':
    get_files()