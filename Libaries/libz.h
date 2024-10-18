#ifndef LIBZ_H
#define LIBZ_H

#include <windows.h>

size_t strlen(const char* String){
    size_t len = 0;
    while(*String++){
        len++;
    }
    return len;
}

void Println(const char* String){
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

    DWORD written;
    WriteConsole(hConsole, String, (DWORD)strlen(String), &written, NULL);
}

#endif