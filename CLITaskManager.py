import json
import csv
import os

FILE_NAME = "tasks"
FORMAT = "json"  # "json", "csv", or "txt"


# ---------------- LOAD & SAVE ---------------- #

def load_tasks():
    filename = f"{FILE_NAME}.{FORMAT}"

    if not os.path.exists(filename):
        return []

    if FORMAT == "json":
        with open(filename, "r") as f:
            return json.load(f)

    elif FORMAT == "csv":
        tasks = []
        with open(filename, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append({
                    "title": row["title"],
                    "description": row.get("description", ""),
                    "done": row["done"] == "True"
                })
        return tasks

    elif FORMAT == "txt":
        tasks = []
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                title = parts[0]
                description = parts[1] if len(parts) > 2 else ""
                done = parts[-1] == "True"

                tasks.append({
                    "title": title,
                    "description": description,
                    "done": done
                })
        return tasks


def save_tasks(tasks):
    filename = f"{FILE_NAME}.{FORMAT}"

    if FORMAT == "json":
        with open(filename, "w") as f:
            json.dump(tasks, f, indent=2)

    elif FORMAT == "csv":
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "description", "done"])
            writer.writeheader()
            writer.writerows(tasks)

    elif FORMAT == "txt":
        with open(filename, "w") as f:
            for task in tasks:
                f.write(f"{task['title']}|{task['description']}|{task['done']}\n")


# ---------------- CRUD ---------------- #

def create_task(tasks, title, description):
    tasks.append({
        "title": title,
        "description": description,
        "done": False
    })
    save_tasks(tasks)
    print(f"✅ Created: {title}")


def read_tasks(tasks):
    if not tasks:
        print("📭 No tasks.")
        return

    for i, task in enumerate(tasks, start=1):
        status = "✔" if task["done"] else "✘"
        print(f"{i}. [{status}] {task['title']}")
        if task["description"]:
            print(f"   └─ {task['description']}")


def update_task(tasks, index):
    try:
        task = tasks[index]
        print(f"Editing: {task['title']}")

        new_title = input("New title (leave blank to keep): ").strip()
        if new_title:
            task["title"] = new_title

        new_desc = input("New description (leave blank to keep): ").strip()
        if new_desc:
            task["description"] = new_desc

        status = input("Mark as done? (y/n/skip): ").lower()
        if status == "y":
            task["done"] = True
        elif status == "n":
            task["done"] = False

        save_tasks(tasks)
        print("✏️ Task updated!")

    except IndexError:
        print("❌ Invalid task number.")


def delete_task(tasks, index):
    try:
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑 Deleted: {removed['title']}")
    except IndexError:
        print("❌ Invalid task number.")


# ---------------- MAIN LOOP ---------------- #

def main():
    tasks = load_tasks()

    while True:
        print("\n📌 Task Manager (CRUD + Description)")
        print("1. Create task")
        print("2. Read tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            description = input("Description: ").strip()
            if title:
                create_task(tasks, title, description)

        elif choice == "2":
            read_tasks(tasks)

        elif choice == "3":
            read_tasks(tasks)
            try:
                idx = int(input("Task number: ")) - 1
                update_task(tasks, idx)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "4":
            read_tasks(tasks)
            try:
                idx = int(input("Task number: ")) - 1
                delete_task(tasks, idx)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "5":
            print("👋 Bye!")
            break

        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()