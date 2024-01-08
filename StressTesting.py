import subprocess
import time
import os
from multiprocessing import Process, Pool

def run_server():
    with open('data_dump.txt', 'a') as output_file:
        subprocess.run(['python', 'Server.py'], stdout=output_file, stderr=output_file)
        
def run_peer(peer_input):
    process = subprocess.Popen(['python', 'PeerMock.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, _ = process.communicate(input=peer_input.encode())
    return

def clear_file_contents(file_name):
    open(file_name, 'w').close()

def check_output_for_keyword(file_name, keyword):
    with open(file_name, 'r') as f:
        return keyword in f.read()

def main():
    server_process = Process(target=run_server)
    server_process.start()
    base_ip = '192.168.56.1'
    base_username = 'User'
    base_password = 'User123'
    base_port = '5'
    iterations_array = []

    try:
        iteration = 0
        while iteration < 2:
            start_time = time.time()
            
            iteration +=1

            current_username = f"{base_username}{iteration}"
            current_port = f"{base_port}{iteration}"
            peer_inputs = f"{base_ip} {current_username} {base_password} {current_port}"

            with Pool(processes=1) as pool:
                _ = pool.map(run_peer, [peer_inputs])

            if check_output_for_keyword('registry.log', 'login-success'):
                clear_file_contents('registry.log')
                time_taken = time.time() - start_time
                print(f"Iteration completed in {time_taken} seconds")
                iterations_array.append(time_taken)
            else:
                print("Error")

            

    except KeyboardInterrupt:
        print("Error")

    finally:
        print(iterations_array)
        server_process.terminate()

if __name__ == "__main__":
    main()
