import os
from rembg import remove
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

def get_image_files(directory):
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
    return files[:20]

def list_files_with_modification_time(directory):
    files = get_image_files(directory)
    if not files:
        print(Fore.RED + "No image files found in the directory.")
        return []
    for idx, file in enumerate(files, 1):
        modified_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, file)))
        formatted_time = modified_time.strftime("%d-%m-%Y %I.%M %p")
        print(f"{idx}. {file}")
    return files

def get_unique_filename(output_dir, base_filename):
    filename_without_ext, ext = os.path.splitext(base_filename)
    new_filename = base_filename
    counter = 1
    while os.path.exists(os.path.join(output_dir, new_filename)):
        new_filename = f"{filename_without_ext}_{counter}{ext}"
        counter += 1
    return new_filename

def remove_background(input_image_path, output_image_path):
    try:
        with open(input_image_path, 'rb') as input_file:
            input_data = input_file.read()
        output_data = remove(input_data)
        with open(output_image_path, 'wb') as output_file:
            output_file.write(output_data)
        print(Fore.GREEN + f"Background removed and image saved as {output_image_path}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while processing {input_image_path}: {str(e)}")

def process_image_selection(files_dir, output_dir):
    while True:
        files = list_files_with_modification_time(files_dir)
        if not files:
            return False
        choice = input("\nSelect Number (or) Image path: ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_image = files[int(choice) - 1]
            input_image_path = os.path.join(files_dir, selected_image)
        else:
            input_image_path = choice
        if not os.path.exists(input_image_path):
            print(Fore.RED + f"Error: Image file '{input_image_path}' does not exist.")
        else:
            filename_without_ext = os.path.splitext(os.path.basename(input_image_path))[0]
            base_output_filename = f"{filename_without_ext}.png"
            output_image_path = os.path.join(output_dir, base_output_filename)
            if os.path.exists(output_image_path):
                overwrite_choice = input(Fore.YELLOW + f"File '{base_output_filename}' already exists in the output folder. Do you want to overwrite it (y) or rename (n)? ").strip().lower()
                if overwrite_choice == 'n':
                    new_filename = get_unique_filename(output_dir, base_output_filename)
                    output_image_path = os.path.join(output_dir, new_filename)
                    print(Fore.CYAN + f"Saving as: {new_filename}")
            remove_background(input_image_path, output_image_path)
        next_step = input("\nDo you want to process another image (y/n)? ").strip().lower()
        if next_step == 'n':
            return False
        elif next_step != 'y':
            print("Invalid choice. Exiting...")
            return False

def main():
    files_dir = 'D:\\BGRemove\\files'
    output_dir = 'D:\\BGRemove\\output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    result = process_image_selection(files_dir, output_dir)
    if not result:
        print("Exiting...")
        return

if __name__ == "__main__":
    main()
