import json
import sys, getopt, os
import struct
import subprocess

f = open(sys.argv[1])
f2 = open(sys.argv[2], 'rb')

data = json.load(f)

shaders = data['SerializedShaders']
hashes = shaders['ShaderMapHashes']
index = hashes.index(sys.argv[3])

map_entry = shaders['ShaderMapEntries'][index]
offset = map_entry['ShaderIndicesOffset']
num = map_entry['NumShaders']

index = 0

for n in range(offset, offset + num):
    shader_index = shaders['ShaderIndices'][n]
    shader_entry = shaders['ShaderEntries'][shader_index]
    group_index = shader_entry['ShaderGroupIndex']
    group_offset = shader_entry['UncompressedOffsetInGroup']
    group_entry = shaders['ShaderGroupEntries'][group_offset]
    size = group_entry['CompressedSize']
    uncompressed_size = group_entry['UncompressedSize']
    f2.seek(4, 0)
    map_array_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(20 * map_array_size, 1)
    shader_array_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(20 * shader_array_size, 1)
    f2.seek(16 * map_array_size + 4, 1)
    f2.seek(17 * shader_array_size + 4, 1)
    shader_group_entries_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(16 * shader_group_entries_size, 1)
    shader_indices_size = struct.unpack('i', f2.read(4))[0]
    f2.seek(4 * shader_indices_size, 1)
    f2.seek(offset, 1)
    data = bytearray()
    data += f2.read(size)
    o = open(sys.argv[4] + str(index), "wb")
    o.write(data)
    o.close()
    subprocess.call(['decompress_shader.exe', sys.argv[4] + str(index), str(uncompressed_size)])
    os.remove(sys.argv[4] + str(index))
    index += 1

f.close()
