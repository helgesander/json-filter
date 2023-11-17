#include <iostream>
#include <windows.h>

int main(int argc, char* argv[]) {
    int status_code = 0;
    if (argc == 1) {
        std::cerr << "no PID set" << std::endl;
        status_code = 1;
    } else {
        DWORD pid = atoi(argv[1]);
        HANDLE process = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
        if (process == NULL) {
            std::cerr << "Failed to open the process" << std::endl;
            status_code = 1;
        } else {
            if (TerminateProcess(process, 0) == NULL) {
                std::cerr << "Failed to terminate the process" << std::endl;
                status_code = 1;
            } else {
                std::cout << "Process with PID = " << pid << "was terminated successfully" << std::endl;
            }
        }
        return status_code;
    }
}
