from src.environment.config import Config
import sys

def main():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("The name of the input file must be provided")
    cfg = Config(sys.argv[1])
    cfg.declare_content()