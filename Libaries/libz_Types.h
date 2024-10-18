#ifndef LIBZ_TYPES_H
#define LIBZ_TYPES_H

#include "libz_memory.h"


/*

THIS LIBARY MOST LIKEY WONT BE USED AS THE STR TYPE AND OTHER TYPES WILL BE BUILT-IN LOOK AT Includes/Built-ins.z TO SEE MORE

*/
typedef struct{
    size_t Size;
    char* String;
} Str;


Str MakeStr(const char* String){
    size_t len = strlen(String);
    Str str;

    if(len != 0){
        str.String = (char*)Alloc(len * sizeof(char));
        MemCopy(str.String, String, len);
        str.Size = len;
    }else{
        str.String = (char*)Alloc(sizeof(char));
        str.Size = 1;
    }
    return str;
}

void DeleteStr(Str* String){
    Free(&String->String);
    String->Size = 0;
    String->String = NULL;
}

char* StrCat(char* Dest, const char* Src){
    char* ptr = Dest;
    while(*ptr != '\0'){
        ptr++;
    }

    while(*Src != '\0'){
        *ptr = *Src;
        ptr++;
        Src++;
    }
    *ptr = '\0';

    return Dest;
};

void Append(const char* AString, Str* String){
    size_t Len1 = strlen(AString);
    size_t Len2 = strlen(String->String);
    Realloc(String->String, (Len1 + Len2 + 1) * sizeof(char));

    StrCat((char *)String->String, AString);

    
    String->Size = (Len1 + Len2 + 1); 
}


void SmartPointer_DeleteStr(void* ptr){
    Str* String = (Str *)ptr;
    DeleteStr(String);
}

#endif