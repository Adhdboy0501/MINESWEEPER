def main():
    with open("src\\code\\MINESWEEPER.py", 'r') as f:
        data = f.read()
        
    exec(data)

if __name__ == "__main__":
    main()