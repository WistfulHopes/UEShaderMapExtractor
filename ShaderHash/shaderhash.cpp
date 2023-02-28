#include "CityHash.h"
#include <iostream>
#include <algorithm>
#include <string>
#include <stdio.h>

typedef unsigned long DWORD;
typedef unsigned short WORD;
#define LOWORD(a) ((WORD)(a))
#define HIWORD(a) ((WORD)(((DWORD)(a) >> 16) & 0xFFFF))

int main(int argc, char const *argv[])
{
    std::string str(argv[1]);
    std::transform(str.begin(), str.end(),str.begin(), ::toupper);
    uint64 Hash = CityHash64WithSeed(str.c_str(), str.length(), atoi(argv[2]));
    std::cout << Hash << std::endl;
    return 0;
}
