// implementation of generic tools

#include "tools.h"

void *operator new(size_t size)
{
    void *p = malloc(size);
    if(!p) abort();
    return p;
}

void *operator new[](size_t size)
{
    void *p = malloc(size);
    if(!p) abort();
    return p;
}

void operator delete(void *p) { if(p) free(p); }

void operator delete[](void *p) { if(p) free(p); }
