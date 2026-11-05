import copy
from dataclasses import dataclass, field


@dataclass
class LittleCow:
    age: int
    name: str
    prefereces: dict = field(default_factory=dict)

def main():
    original = LittleCow(1, "little")
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    print(shallow is original)
    print(shallow == original)

    print(deep is original)
    print(deep == original)

    original.age = 2
    original.prefereces['food'] = 'dry'
    print(f"original={original}")
    print(f"shallow={shallow}")
    print(f"deep={deep}")


if __name__ == "__main__":
    main()
