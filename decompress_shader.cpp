#include "lz4.h"
#include <iostream>
#include <fstream>
#include <sstream>

int main(int argc, char const *argv[])
{
    std::ostringstream sstream;
    std::ifstream shader(argv[1], std::ios::binary);
    sstream << shader.rdbuf();
    shader.seekg(0, std::ios::end);
    size_t fsize = shader.tellg();
    shader.close();
    const std::string str(sstream.str());
    const char* buffer = str.c_str();
    char* outBuffer = (char*)malloc(atoi(argv[2]));
    std::cout << "Decompressing file " << argv[1] << " with size " << fsize << std::endl;
    int success = LZ4_decompress_safe(buffer, outBuffer, fsize, atoi(argv[2]));
    if (success > 0)
    {
        uint8_t magic[] = {0x44, 0x58, 0x42, 0x43};
        int final_index = -1;
        for (int i = 0; i < atoi(argv[2]); i++)
        {
            if (std::memcmp(magic, (void*)(outBuffer + i), sizeof magic) == 0)
            {
                final_index = i;
                break;
            }
        }
        if (final_index == -1)
            return final_index;
        uint32_t size = *(uint32_t*)&outBuffer[final_index + 24];
        std::string newName = argv[1];
        newName += ".dxbc";
        std::ofstream outShader(newName, std::ios::binary | std::ios::out);
        outShader.write(outBuffer + final_index, size);
        outShader.close();
        std::cout << "File written to " << newName << " with size " << size << std::endl;
        return 0;
    }
    return success;
}