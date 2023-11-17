#include <windows.h>
#include <string>
#include <iostream>

int main(int argc, char* argv[])
{
    STARTUPINFO si = {};
    PROCESS_INFORMATION pi = {};
    LPCWSTR script_name = L"python.exe";
    LPWSTR args = L"..\\json_filter.py --str";
    BOOL success = CreateProcessW(script_name, args, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    if (success) std::cout << "=========== json_filter.py was launched ============"
    else std::cout << "Oh, I can't find python on your computer...\nMaybe you need install it? 0_0";
    return 0;
}