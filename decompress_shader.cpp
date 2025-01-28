#include "lz4.h"
#include "zlib-1.2.5/Inc/zlib.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include "oodle/include/oodle2.h"
#include "zstd-v1.5.6-win64/include/zstd.h"

int write_file(char* outBuffer, size_t finalSize, const char* outName)
{
	std::string binName = std::string(outName) + ".bin";
    std::ofstream outBin(binName, std::ios::binary | std::ios::out);
    outBin.write(outBuffer, finalSize);
    
	uint8_t magic[] = {0x44, 0x58, 0x42, 0x43};
    int final_index = -1;
    for (int i = 0; i < finalSize; i++)
    {
        if (std::memcmp(magic, (void*)(outBuffer + i), sizeof magic) == 0)
        {
            final_index = i;
            break;
        }
    }
    bool is_pssl = false;
    bool is_glsl = false;
    if (final_index == -1)
    {
        uint8_t magic[] = {0x53, 0x68, 0x64, 0x72};
        for (int i = 0; i < finalSize; i++)
        {
            if (std::memcmp(magic, (void*)(outBuffer + i), sizeof magic) == 0)
            {
                final_index = i;
                is_pssl = true;
                break;
            }
        }
    	is_glsl = true;
    }
    uint32_t size = *(uint32_t*)&outBuffer[final_index + 24];
    std::string newName = outName;
    uint8_t dxil_magic[] = {0x44, 0x58, 0x49, 0x4C};
    bool is_dxil = false;
    for (int i = 0; i < finalSize; i++)
    {
        if (std::memcmp(dxil_magic, (void*)(outBuffer + i), sizeof magic) == 0)
        {
            is_dxil = true;
            break;
        }
    }
    if (is_dxil)
        newName += ".dxil";
    else if (is_pssl)
    	newName += ".pssl";
    else if (is_glsl)
    	newName += ".glsl";
    else
        newName += ".dxbc";
    std::ofstream outShader(newName, std::ios::binary | std::ios::out);
    if (is_pssl || is_glsl)
    {
        outShader.write(outBuffer, finalSize);
        std::cout << "File written to " << newName << " with size " << finalSize << std::endl;
    }
    else
    {
        outShader.write(outBuffer + final_index, size);
        std::cout << "File written to " << newName << " with size " << size << std::endl;
    }
    outShader.close();
    return 0;
}


static void *zalloc(void *opaque, unsigned int size, unsigned int num)
{
	return malloc(size * num);
}

static void zfree(void *opaque, void *p)
{
	free(p);
}

bool appUncompressMemoryZLIB( void* UncompressedBuffer, int32_t UncompressedSize, const void* CompressedBuffer, int32_t CompressedSize, int32_t BitWindow )
{
	// Zlib wants to use unsigned long.
	unsigned long ZCompressedSize	= CompressedSize;
	unsigned long ZUncompressedSize	= UncompressedSize;
	
	z_stream stream;
	stream.zalloc = &zalloc;
	stream.zfree = &zfree;
	stream.opaque = Z_NULL;
	stream.next_in = (uint8_t*)CompressedBuffer;
	stream.avail_in = ZCompressedSize;
	stream.next_out = (uint8_t*)UncompressedBuffer;
	stream.avail_out = ZUncompressedSize;

	if (BitWindow == 0)
	{
		BitWindow = 15;
	}

	int32_t Result = inflateInit2(&stream, BitWindow);

	if(Result != Z_OK)
		return false;

	// Uncompress data.
	Result = inflate(&stream, Z_FINISH);
	if(Result == Z_STREAM_END)
	{
		ZUncompressedSize = stream.total_out;
	}

	int32_t EndResult = inflateEnd(&stream);
	if (Result >= Z_OK)
	{
		Result = EndResult;
	}

	bool bOperationSucceeded = (Result == Z_OK);

	// Sanity check to make sure we uncompressed as much data as we expected to.
	if( UncompressedSize != ZUncompressedSize )
	{
		bOperationSucceeded = false;
	}
	return bOperationSucceeded;
}

bool appUncompressMemoryGZIP(void* UncompressedBuffer, int32_t UncompressedSize, const void* CompressedBuffer, int32_t CompressedSize)
{
	// Zlib wants to use unsigned long.
	unsigned long ZCompressedSize = CompressedSize;
	unsigned long ZUncompressedSize = UncompressedSize;

	z_stream stream;
	stream.zalloc = &zalloc;
	stream.zfree = &zfree;
	stream.opaque = Z_NULL;
	stream.next_in = (uint8_t*)CompressedBuffer;
	stream.avail_in = ZCompressedSize;
	stream.next_out = (uint8_t*)UncompressedBuffer;
	stream.avail_out = ZUncompressedSize;

	int32_t Result = inflateInit2(&stream, 16 + MAX_WBITS);

	if (Result != Z_OK)
		return false;

	// Uncompress data.
	Result = inflate(&stream, Z_FINISH);
	if (Result == Z_STREAM_END)
	{
		ZUncompressedSize = stream.total_out;
	}

	int32_t EndResult = inflateEnd(&stream);
	if (Result >= Z_OK)
	{
		Result = EndResult;
	}

	// These warnings will be compiled out in shipping.
	bool bOperationSucceeded = (Result == Z_OK);

	// Sanity check to make sure we uncompressed as much data as we expected to.
	if (UncompressedSize != ZUncompressedSize)
	{
		bOperationSucceeded = false;
	}
	return bOperationSucceeded;
}

bool appDecompressOodle(const char *CompressedBuffer, int CompressedSize, char *UncompressedBuffer, int UncompressedSize)
{
	size_t ret = OodleLZ_Decompress(CompressedBuffer, CompressedSize, UncompressedBuffer, UncompressedSize,
		OodleLZ_FuzzSafe_Yes, OodleLZ_CheckCRC_No, OodleLZ_Verbosity_Minimal);
	if (ret != UncompressedSize)
	{
		std::cout << "OodleLZ_Decompress returned " << ret << std::endl;
		return false;
	}
	return true;
}

bool
appDecompressZstd(const char* InputData, size_t InputDataSize, const char* OutputData, size_t OutputDataSize)
{
	size_t DecompressedSizeExpected = ZSTD_getDecompressedSize(InputData, InputDataSize);
	if (OutputDataSize >= DecompressedSizeExpected)
	{
		size_t DecompressedSizeActual = ZSTD_decompress((void*)OutputData, OutputDataSize, InputData, InputDataSize);
		return DecompressedSizeActual == OutputDataSize;
	}

	return false;
}

int main(int argc, char const *argv[])
{
	if (argc < 3)
	{
		std::cout << "Not enough arguments! First argument should be the shader to decompress. Second argument should be the uncompressed size." << std::endl;

		return 1;
	}
	
    std::ostringstream sstream;
    std::ifstream shader(argv[1], std::ios::binary);
    sstream << shader.rdbuf();
    shader.seekg(0, std::ios::end);
    size_t compressedSize = shader.tellg();
    shader.close();
    const std::string str(sstream.str());
    const char* buffer = str.c_str();
    size_t uncompressedSize = atoi(argv[2]);
    auto outBuffer = (char*)malloc(uncompressedSize);
	std::cout << "Decompressing file " << argv[1] << " with size " << compressedSize << std::endl;
	if (appDecompressOodle(buffer, compressedSize, outBuffer, uncompressedSize)) 
	{
		return write_file(outBuffer, uncompressedSize, argv[1]);
	}
    if (LZ4_decompress_safe(buffer, outBuffer, compressedSize, uncompressedSize))
    {
        return write_file(outBuffer, uncompressedSize, argv[1]);
    }
    if (appUncompressMemoryZLIB(outBuffer, uncompressedSize, buffer, compressedSize, 0)) 
    {
        return write_file(outBuffer, uncompressedSize, argv[1]);
    }
	if (appUncompressMemoryGZIP(outBuffer, uncompressedSize, buffer, compressedSize)) 
	{
		return write_file(outBuffer, uncompressedSize, argv[1]);
	}
	if (appDecompressZstd(buffer, compressedSize, outBuffer, uncompressedSize)) 
	{
		return write_file(outBuffer, uncompressedSize, argv[1]);
	}
    
    std::cout << "Failed to decompress file!" << std::endl;

    return 1;
}