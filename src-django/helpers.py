#General helpers used for maintainance
from sys import argv
from datetime import datetime
import hashlib


USERNAME="Blazzee"
DATE = datetime.now()

#python helpers
#Generate blog headers
def create_blog_headers():
    pass

def main():
    if len(argv[1:]) !=2:
        print(f"Error: Usage python helpers.py create_blog_headers filename")
        raise Exception("Incorrect Usage")
    else:
        try:
            with open(f"{argv[2]}", mode="r", encoding="utf-8") as blog_original:
                blog_content = blog_original.read()
                num_lines = len(blog_original.readlines())

                seed = f"{USERNAME}:{num_lines}"
                hash_object=hashlib.sha1(seed.encode("utf-8"))

                commit = hash_object.hexdigest()[:7]
                
                header = f" commit: {commit} \n Author: {USERNAME} <maanik@tui.blog>\n Tags: Version Control,Git \n Date: {DATE}\n\n\n" + blog_content 
                print(header)
                try:
                    with open(f"headers_{argv[2]}", mode="w", encoding="utf-8") as blog_modified:
                            blog_modified.write(header)
                        print(f"Created blog headers and new file ")
                except Exception as e:
                    print(f"Could not write to file")
        except FileNotFoundError as e:
            print(f"File {argv[2]} could not be found")



if __name__=="__main__":
    main()
