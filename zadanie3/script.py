import subprocess

# Lista rozmiarów instancji do przetestowania
sizes = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

# Ścieżki do plików
instance_path_template = "instancje/in_151788_{size}.txt"
output_path_template = "pliki_wynikowe/out_{size}"

# Uruchamianie testów
for size in sizes:
    instance_file = instance_path_template.format(size=size)
    output_file = output_path_template.format(size=size)

    try:
        result = subprocess.run(
            ["python3", "verifier.py", instance_file, output_file],
            capture_output=True,
            text=True
        )
        print(f"Test for size {size}:")
        print(result.stdout.strip() if result.returncode == 0 else result.stderr.strip())
        print("-" * 60)

    except Exception as e:
        print(f"Error testing size {size}: {e}")
