from core.scheduler import blogs_do_dia

def main():
    blogs = blogs_do_dia()

    if not blogs:
        print("Nenhum blog programado para hoje.")
        return

    print("Blogs programados para hoje:")

    for blog in blogs:
        print(f"- {blog['nome']} (ID: {blog['blog_id']})")

if __name__ == "__main__":
    main()
