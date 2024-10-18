#ifndef LIBZ_MEMORY_H
#define LIBZ_MEMORY_H

#include <windows.h>

void* Alloc(size_t size){
    if(size == 0){
        return NULL;
    }
    HANDLE Hheap = GetProcessHeap();
    void* ptr = HeapAlloc(Hheap, HEAP_ZERO_MEMORY, size);

    return ptr;
}

BOOL Free(void* ptr){
    HANDLE Hheap = GetProcessHeap();
    BOOL Ret = HeapFree(Hheap, 0, ptr);
    ptr = NULL;
    return Ret;
}


void MemCopy(void* dest, void* src, size_t size){
    unsigned char* Destination = (unsigned char*)dest;
    const unsigned char* Source = (const unsigned char*)src;

    for(size_t i = 0; i < size; i++){
        Destination[i] = Source[i];
    }
}

void Realloc(void* ptr, size_t size){
    HANDLE Hheap = GetProcessHeap();
    ptr = HeapReAlloc(Hheap, 0, ptr, size); 
}



// typedef struct{
//     void* Ptr;
//     int RefCount;
//     void (*Destroy)(void *);
// } Smart_Ptr;

// void DestroySmartPtr(Smart_Ptr *smt_Ptr){
//     (*smt_Ptr->Destroy)(smt_Ptr->Ptr);
//     smt_Ptr->RefCount = 0;
// }


// void IncPtr(Smart_Ptr *smt_Ptr){
//     smt_Ptr->RefCount++;
// }

// void DecPtr(Smart_Ptr *smt_Ptr){
//     smt_Ptr->RefCount--;
//     if(smt_Ptr->RefCount == 0){

//         DestroySmartPtr(smt_Ptr);
//     }
// }
#endif
