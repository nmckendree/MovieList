from pathlib import Path
import sys

def get_drive_path():
    drive = input("Enter the drive letter (e.g., F): ").strip().upper()
    if len(drive) != 1 or not drive.isalpha():
        print("Invalid drive letter.")
        sys.exit(1)
    return Path(f"{drive}:\\")  # Windows-style root

def write_movie_list(base_path: Path):
    movies_dir = base_path / "Movies"
    if not movies_dir.is_dir():
        print(f"Movies folder not found at {movies_dir}")
        return

    out_file = Path("movie_list.txt")
    with out_file.open("w", encoding="utf-8") as mf:
        for folder in sorted(movies_dir.iterdir()):
            if folder.is_dir():
                mf.write(folder.name + "\n")
    print(f"Wrote movie_list.txt ({out_file.resolve()})")

def write_tv_list(base_path: Path):
    tv_root = base_path / "TV Shows"
    if not tv_root.is_dir():
        print(f"TV Shows folder not found at {tv_root}")
        return

    out_file = Path("tv_list.txt")
    with out_file.open("w", encoding="utf-8") as tf:
        for show_folder in sorted(tv_root.iterdir()):
            if not show_folder.is_dir():
                continue
            for season_folder in sorted(show_folder.iterdir()):
                if season_folder.is_dir():
                    line = f"{show_folder.name},{season_folder.name}"
                    tf.write(line + "\n")
    print(f"Wrote tv_list.txt ({out_file.resolve()})")

def main():
    base_path = get_drive_path()
    write_movie_list(base_path)
    write_tv_list(base_path)

if __name__ == "__main__":
    main()
