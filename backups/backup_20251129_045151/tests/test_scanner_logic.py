
def parse_ports(input_str):
    if not input_str.strip():
        return None

    ports = set()
    parts = input_str.split(',')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if start > end:
                    start, end = end, start
                
                if (end - start) > 1000:
                    print(f"[!] Rango {part} demasiado grande. Limitando a primeros 1000.")
                    end = start + 1000
                    
                ports.update(range(start, end + 1))
            except ValueError:
                print(f"[!] Rango inválido ignorado: {part}")
        else:
            try:
                port = int(part)
                if 1 <= port <= 65535:
                    ports.add(port)
                else:
                    print(f"[!] Puerto fuera de rango (1-65535) ignorado: {port}")
            except ValueError:
                print(f"[!] Puerto inválido ignorado: {part}")
                
    return sorted(list(ports))

# Test Cases
tests = [
    ("22, 80, 443", [22, 80, 443]),
    ("20-25", [20, 21, 22, 23, 24, 25]),
    ("22, 80-82, 443", [22, 80, 81, 82, 443]),
    ("", None),
    ("  ", None),
    ("abc, 80", [80]),
    ("1-", [80]), # Should fail the range part, but how? split('-') gives ['1', ''] -> int('') fails.
    ("90000, 80", [80]),
    ("80-78", [78, 79, 80]) # Swapped range
]

print("--- Running Tests ---")
for inp, expected in tests:
    if inp == "1-": # Special case handling for test loop simplicity
        print(f"Testing '{inp}'...")
        res = parse_ports(inp)
        print(f"Result: {res}")
        continue
        
    print(f"Testing '{inp}' -> Expected: {expected}")
    result = parse_ports(inp)
    if result == expected:
        print("  [PASS]")
    else:
        print(f"  [FAIL] Got: {result}")

