import os


def find_migrations_with_columns(directory, columns_to_check):
    all_files = []
    containing_files = {column: [] for column in columns_to_check}

    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            full_path = os.path.join(directory, filename)
            all_files.append(filename)
            with open(full_path, 'r') as file:
                file_content = file.read()
                for column in columns_to_check:
                    if column in file_content:
                        containing_files[column].append(filename)

    return all_files, containing_files


if __name__ == "__main__":
    migration_dir = 'pages/migrations'
    columns_to_check = ['translation_key', 'title_en']
    all_files, containing_files = find_migrations_with_columns(migration_dir, columns_to_check)

    print("All migration files found:")
    for file in all_files:
        print(f"- {file}")

    for column, files in containing_files.items():
        if files:
            print(f"\nMigration files containing '{column}':")
            for file in files:
                print(f"- {file}")
        else:
            print(f"\nNo migration files containing '{column}' found.")

