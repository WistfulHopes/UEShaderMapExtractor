import json
import sys, getopt, os
import base64
import subprocess

f = open(sys.argv[1])

data = json.load(f)
  
index = 0

material = data[0]
resources = material['LoadedMaterialResources']

for resource in resources:
    shader_map = resource['LoadedShaderMap']
    code = shader_map['Code']

    for i in code['ShaderEntries']:
        coded_string = i['Code']
        o = open(sys.argv[1] + str(index), "wb")
        o.write(base64.b64decode(coded_string))
        o.close()
        subprocess.call(['decompress_shader.exe', sys.argv[1] + str(index), str(i['UncompressedSize'])])
        os.remove(sys.argv[1] + str(index))
        index += 1
  
f.close()
