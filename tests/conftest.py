import pkgutil
from pathlib import Path


fixtures_directory_name: str = 'fixtures'
fixtures_directory_path: Path = Path(__file__).parent.joinpath(fixtures_directory_name)
pytest_plugins: list[str] = [
    f'{fixtures_directory_name}.{module}' for _, module, _ in pkgutil.iter_modules([str(fixtures_directory_path)])
]
