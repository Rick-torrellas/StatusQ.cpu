from src.adapter import CPUStateCheck

def main():
    cpu_checker = CPUStateCheck()
    cpu_data = cpu_checker.capture()
    
    print(f"Checking hardware: {cpu_data.name}")
    print(f"Architecture: {cpu_data.current_temperature}")
    print(f"Current Usage: {cpu_data.total_usage_percentage}%")

if __name__ == "__main__":
    main()