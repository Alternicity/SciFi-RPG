def simulate_turn():
    print("Simulating city dynamics...")
    auto_connect()
    distribute_energy()
    update_loyalties()
    display_status()
    adjust_morale()
    simulate_day()