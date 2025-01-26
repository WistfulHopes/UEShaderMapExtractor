import json
import sys
import struct


f = open(sys.argv[1])

data = json.load(f)
  
index = 0
count = 0
material = data[0]
resources = material['LoadedMaterialResources']

for resource in resources:
    def extract_value(data):
        global count
        list = []
        type = struct.unpack('<b', data[1:2])[0]
        count += 1

        if type >= 25:
            raise "Cannot parse structs!"
        else:
            match type:
                case 0:
                    return list
                case 1:
                    list.append(struct.unpack('<f', data[2:6])[0])
                    count += 4
                    return list
                case 2:
                    list.append(struct.unpack('<f', data[2:6])[0])
                    list.append(struct.unpack('<f', data[6:10])[0])
                    count += 8
                    return list
                case 3:
                    list.append(struct.unpack('<f', data[2:6])[0])
                    list.append(struct.unpack('<f', data[6:10])[0])
                    list.append(struct.unpack('<f', data[10:14])[0])
                    count += 12
                    return list
                case 4:
                    list.append(struct.unpack('<f', data[2:6])[0])
                    list.append(struct.unpack('<f', data[6:10])[0])
                    list.append(struct.unpack('<f', data[10:14])[0])
                    list.append(struct.unpack('<f', data[14:18])[0])
                    count += 16
                    return list
                case 5 | 17:
                    list.append(struct.unpack('<d', data[2:6])[0])
                    count += 8
                    return list
                case 6 | 18:
                    list.append(struct.unpack('<d', data[2:6])[0])
                    list.append(struct.unpack('<d', data[6:10])[0])
                    count += 16
                    return list
                case 7 | 19:
                    list.append(struct.unpack('<d', data[2:6])[0])
                    list.append(struct.unpack('<d', data[6:10])[0])
                    list.append(struct.unpack('<d', data[10:14])[0])
                    count += 24
                    return list
                case 8 | 20:
                    list.append(struct.unpack('<d', data[2:6])[0])
                    list.append(struct.unpack('<d', data[6:10])[0])
                    list.append(struct.unpack('<d', data[10:14])[0])
                    list.append(struct.unpack('<d', data[14:18])[0])
                    count += 32
                    return list
                case 9:
                    list.append(struct.unpack('<i', data[2:6])[0])
                    count += 4
                    return list
                case 10:
                    list.append(struct.unpack('<i', data[2:6])[0])
                    list.append(struct.unpack('<i', data[6:10])[0])
                    count += 8
                    return list
                case 11:
                    list.append(struct.unpack('<i', data[2:6])[0])
                    list.append(struct.unpack('<i', data[6:10])[0])
                    list.append(struct.unpack('<i', data[10:14])[0])
                    count += 12
                    return list
                case 12:
                    list.append(struct.unpack('<i', data[2:6])[0])
                    list.append(struct.unpack('<i', data[6:10])[0])
                    list.append(struct.unpack('<i', data[10:14])[0])
                    list.append(struct.unpack('<i', data[14:18])[0])
                    count += 16
                    return list
                case 13:
                    list.append(struct.unpack('<?', data[2:3])[0])
                    count += 1
                    return list
                case 14:
                    list.append(struct.unpack('<?', data[2:3])[0])
                    list.append(struct.unpack('<?', data[3:4])[0])
                    count += 2
                    return list
                case 15:
                    list.append(struct.unpack('<?', data[2:3])[0])
                    list.append(struct.unpack('<?', data[3:4])[0])
                    list.append(struct.unpack('<?', data[4:5])[0])
                    count += 3
                    return list
                case 16:
                    list.append(struct.unpack('<?', data[2:3])[0])
                    list.append(struct.unpack('<?', data[3:4])[0])
                    list.append(struct.unpack('<?', data[4:5])[0])
                    list.append(struct.unpack('<?', data[5:6])[0])
                    count += 4
                    return list
                case 21:
                    list.append(struct.unpack('<ffff', data[2:18])[0])
                    list.append(struct.unpack('<ffff', data[18:34])[0])
                    list.append(struct.unpack('<ffff', data[34:50])[0])
                    list.append(struct.unpack('<ffff', data[50:66])[0])
                    count += 64
                    return list
                case 22 | 23 | 24:
                    list.append(struct.unpack('<dddd', data[2:34])[0])
                    list.append(struct.unpack('<dddd', data[34:66])[0])
                    list.append(struct.unpack('<dddd', data[66:98])[0])
                    list.append(struct.unpack('<dddd', data[98:130])[0])
                    count += 128
                    return list
                    

    def extract_swizzle(data):
        list = []
        list.append(struct.unpack('<B', data[1:2])[0])
        list.append(struct.unpack('<B', data[2:3])[0])
        list.append(struct.unpack('<B', data[3:4])[0])
        list.append(struct.unpack('<B', data[4:5])[0])
        list.append(struct.unpack('<B', data[5:6])[0])
        return (list)


    def read_preshader_sub(data):
        global count
        opcode = struct.unpack('<b', data[0:1])[0]
        count += 1

        match opcode:
            case 1:
                return {"ConstantZero": ([])}
            case 2:
                return {"Constant": extract_value(data)}
            case 3:
                idx = struct.unpack('<H', data[1:3])[0]
                count += 2
                return {"NumericParameter": ([numeric_params[idx]['ParameterInfo']['Name']])}
            case 4:
                return {"Add": []}
            case 5:
                return {"Sub": []}
            case 6:
                return {"Mul": []}
            case 7:
                return {"Div": []}
            case 8:
                return {"Fmod": []}
            case 9:
                return {"Min": []}
            case 10:
                return {"Max": []}
            case 11:
                return {"Clamp": []}
            case 19:
                return {"Dot": []}
            case 20:
                return {"Cross": []}
            case 21:
                return {"Sqrt": []}
            case 12:
                return {"Sin": []}
            case 13:
                return {"Cos": []}
            case 14:
                return {"Tan": []}
            case 15:
                return {"Asin": []}
            case 16:
                return {"Acos": []}
            case 17:
                return {"Atan": []}
            case 18:
                return {"Atan2": []}
            case 22:
                return {"Rcp": []}
            case 23:
                return {"Length": []}
            case 24:
                return {"Normalize": []}
            case 25:
                return {"Saturate": []}
            case 26:
                return {"Abs": []}
            case 27:
                return {"Floor": []}
            case 28:
                return {"Ceil": []}
            case 29:
                return {"Round": []}
            case 30:
                return {"Trunc": []}
            case 31:
                return {"Sign": []}
            case 32:
                return {"Frac": []}
            case 33:
                return {"Fractional": []}
            case 34:
                return {"Log2": []}
            case 35:
                return {"Log10": []}
            case 36:
                count += 5
                return {"ComponentSwizzle": extract_swizzle(data)}
            case 37:
                return {"AppendVector": ([])}
            case 38:
                count += 3
                return {"TextureSize": ([struct.unpack('<i', data[1:5])[0]])}
            case 39:
                count += 3
                return {"TexelSize": ([struct.unpack('<i', data[1:5])[0]])}
            case 40:
                return {"ExternalTextureCoordinateScaleRotation": ([])}
            case 41:
                return {"ExternalTextureCoordinateOffset": ([])}
            case 42:
                return {"RuntimeVirtualTextureUniform": ([])}
            case 43:
                return {"SparseVolumeTextureUniform": ([])}
            case 44:
                return {"GetField": ([])}
            case 45:
                return {"SetField": ([])}
            case 46:
                return {"Neg": ([])}
            case 47:
                return {"Jump": ([])}
            case 48:
                return {"JumpIfFalse": ([])}
            case 49:
                return {"PushValue": ([])}
            case 50:
                return {"Less": ([])}
            case 51:
                return {"Assign": ([])}
            case 52:
                return {"Greater": ([])}
            case 53:
                return {"LessEqual": ([])}
            case 54:
                return {"GreaterEqual": ([])}
            

    def read_preshader(data):
        global count
        ret = []
        count = 0
        
        while len(data) > 0:
            ret.append(read_preshader_sub(data))
            data = data[count:]
                
        return ret
        
    shader_map = resource['LoadedShaderMap']
    quality_level = shader_map['ShaderMapId']['QualityLevel']
    feature_level = shader_map['ShaderMapId']['FeatureLevel']
    content = shader_map['Content']
    compilation_output = content['MaterialCompilationOutput']
    uniform_expression_set = compilation_output['UniformExpressionSet']
    preshaders = uniform_expression_set['UniformPreshaders']
    
    numeric_params = uniform_expression_set['UniformNumericParameters']
    
    name = sys.argv[1] + "_" + quality_level + "_" + feature_level
    
    preshader_file = open(name + "_preshader.bin", "rb")
    preshader = preshader_file.read()
    preshader_file.close()
    
    parsed_preshader = {
        "preshader": [],
    }
    
    for i, entry in enumerate(preshaders):
        offset = entry['OpcodeOffset']
        size = entry['OpcodeSize']
        parsed_preshader["preshader"].append(read_preshader(preshader[offset:offset+size]))
    
    o = open(name + "_preshader.json", "w")
    o.write(json.dumps(parsed_preshader, indent=4))
    o.close()
  
f.close()
