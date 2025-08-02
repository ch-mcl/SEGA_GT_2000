import array
import io
import typing
import mathutils
import struct

import bmesh
import bpy


# Ninja Chunk Format
# IF file has "NJCM"(Ninja Chank Model Tree) Magic I'll not write this code.

# Chunk Tiny (0x08 - 0x09)
class Tiny:
    fmt = '<4B'
    def __init__(self):
        self.flip_u = False
        self.flip_v = False
        self.clamp_u = False
        self.clamp_v = False
        self.mipmap_adjust = 0x00
        slef.filter_mode = 0x00
        self.super_sample = 0x00
        self.TexId = 0x00

    def unpakc(self, file: typing.IO) -> None:
        bytes = file.read(struct.calcsize(self.fmt))
        buff = struct.unpack_from(self.fmt, bytes, 0)
        # TDOO Store


# Material (0x10 - 0x1F)
class Material:
    def __init__(self):
        self.chunck_flags = 0x00
        self.chunk_head = 0x00
        self.size = 0x00

    fmt = '<1B'
    def unpakc(self, file: typing.IO) -> bool:
        bytes = file.read(struct.calcsize(self.fmt))
        buff = struct.unpack_from(self.fmt, bytes, 0)
        # TDOO Store
        skip = 0x00
        if ((buff[1]&0xF) == 1):
            skip = 7
        elif ((buff[1]&0xF) == 3):
            skip = 11
        else:
            return True
        file.seek(skip, io.SEEK_CUR)
        return False


class VertexElemnt:
    fmt = [ # optimize for SH4
            '>4f',     #00: x,y,z,1.0F, ...              correct?
            '>8f',     #01: x,y,z,1.0F,nx,ny,nz,0.0F,... correct?

            '>3f',     #02: x,y,z, ...
            '>3f1H',   #03: x,y,z,D8888,...
            '>3f1I',   #04: x,y,z,UserFlags32, ...
            '>3f1I',   #05: x,y,z,NinjaFlags32,...
            '>3f2H',   #06: x,y,z,D565|S565,...
            '>3f2H',   #07: x,y,z,D4444|S565,...
            '>3f2H',   #08: x,y,z,D16|S16,...
            # float vertex normal
            '>6f',     #09: x,y,z,nx,ny,nz, ...
            '>6f1H',   #10: x,y,z,nx,ny,nz,D8888,...
            '>6f1I',   #11: x,y,z,nx,ny,nz,UserFlags32,...
            '>6f1I',   #12: x,y,z,nx,ny,nz,NinjaFlags32,...
            '>6f2H',   #13: x,y,z,nx,ny,nz,D565|S565,...
            '>6f2H',   #14: x,y,z,nx,ny,nz,D4444|S565,...
            '>6f2H',   #15: x,y,z,nx,ny,nz,D16|S16,...
            # 32bits vertex normal  reserved(2)|x(10)|y(10)|z(10)
            '>3f1I',   #16: x,y,z,nxyz32, ...
            '>3f2I',   #17: x,y,z,nxyz32,D8888,...
            '>3f2I'    #18: x,y,z,nxyz32,UserFlags32,...
          ]
    def __init__(self):
        self.pos = [0.0, 0.0, 0.0]
        self.normal = [0.0, 0.0, 0.0]
        self.user_flag = 0x00
        self.ninja_flag = 0x00
        self.diffuse_color = [0.0, 0.0, 0.0, 0.0]
        self.specular_color = [0.0, 0.0, 0.0, 0.0]

    def unpack(self, file: typing.IO, vtx_type: int) -> None:
        _fmt = self.fmt[vtx_type]
        bytes = file.read(struct.calcsize(_fmt))
        buff = struct.unpack_from(_fmt, bytes, 0)
        self.pos = [buff[0], buff[1], buff[2]]
        
# Chunk Vertex
class Vertex:
    fmt = '<2B3H'
    def __init__(self):
        self.head_bits = 0x00 # NF NinjaFlags32 only
        self.chunk_head = 0x00
        self.size = 0x00 # needs "(this_value - 1) * 4" to byte size
        self.user_offset = 0x00
        self.elments = []


    def unpack(self, file: typing.IO) -> None:
        bytes = file.read(struct.calcsize(self.fmt))
        buff = struct.unpack_from(self.fmt, bytes, 0)
        self.chunk_head = buf[0]
        #self.head_bits = buf[1] #?
        self.size = buf[2]
        self.user_offset = buf[3]
        end_adr = file.tell()
        vtx_type = buf[0]-0x20
        for i in range(buf[4]):
            if (file.tell() > end_adr):
                break
            vtx = VertexElement()
            vtx.unpack(file, vtx_type)
            self.elements.append(vtx)
        

# Chunk Volume (0x38 - 0x3A)
class Volume:
    fmt = '<3H'
    def __init__(self):
        self.chunck_flags = 0x00
        self.chunk_head = 0x00
        self.size = 0x00
        self.user_offset = 0x00
        self.count_polygon = 0x00
        self.count_strip = 0x00
    
    def unapck(self, file: typing.IO):
        bytes = file.read(struct.calcsize(self.fmt))
        buff = struct.unpack_from(self.fmt, bytes, 0)
        # TDOO Store
        skip = (buff[1]-1)*2
        file.seek(skip, io.SEEK_CUR)
        return False


# Elment of "Chunk Strip"
class StripElemnt:
    def __init__(self):
        self.idx = 0x00
        self.uv = [0.0, 0.0]
        self.normal = [0.0, 0.0, 0.0]
        self.user_flag = 0x00

# Chunk Strip (0x40 - 0x4B)
class Strip:
    fmt = '<2B2H'

    def __init__(self):
        self.chunck_flags = 0x00
        self.chunk_head = 0x00
        self.size = 0x00
        self.user_offset = 0x00
        self.count_strip = 0x00 # nbStrip
        self.elments = []

    def unpakc(self, file: typing.IO) -> None:
        bytes = file.read(struct.calcsize(self.fmt))
        buff = struct.unpack_from(self.fmt, bytes, 0)
        # TDOO Store
        # TODO unapck strip elemnts
        #elment = StripElemnt()
        size = buff[2]
        self.size = size
        skip = size * 2
        file.seek(skip, io.SEEK_CUR)


class Mesh:
    def __init__(self):
        self.tinys = []
        self.materials = []
        self.vertexs = []
        self.volumes = []
        self.strips = []

    # Chunk Head ... means "Sort of Commands".
    def detect_head(self, file: typing.IO) -> bytes:
        bytes = file.read(struct.calcsize('B'))
        buff = struct.unpack_from('B', bytes, 0)
        file.seek(-1, io.SEEK_CUR) # Go Back Head Parse
        return buff[0]

    def unpack(self, file: typing.IO, max_chunk_count: int) -> bool:
        i = 0
        while(True):
            if (i > max_chunk_count):
                return True
            chunk_head = self.detect_head(file)
            if (chunk_head == 0xFF):
                file.seek(4, io.SEEK_CUR)
                break
            elif ((chunk_head&0xF0) == 0x08):
                # Tiny
                tiny = Tiny()
                tiny.unpack(file)
                self.tinys.append(tiny)
            elif ((chunk_head&0xF0) == 0x10):
                # Material
                material = Material()
                material.unpack(file)
                self.materials.append(material)
            elif ((chunk_head&0x20) == 0x20):
                # Vertex
                vertex = Vertex()
                vertex.unpack(file)
                self.vertexs.append(vertex)
            elif ((chunk_head&0x3B) == 0x38):
                # Volume
                volume = Volume()
                volume.unpack()
                self.volumes = []
            elif ((chunk_head&0xF0) == 0x40):
                # Strip
                strip = StripChunk()
                strip.unkpack(file)
                self.strips.append(strip)
            i = i + 1
        return False


class Polygon:
    fmtHead = 'B'
    def __init__(self):
        self.meshs = []
        self.vertexs = [] 
   
    def unpack(self, file: typing.IO, max_chunk_count: int) -> bool:
        mesh = Mesh()
        result = mesh.unpack(file, max_chunk_count)
        if result:
            print('Chunk Unpack Faild!!! File Position: {0:#X}'.format(file.tell()))
            return True
        self.meshs.append(mesh)
        
        vtx = Mesh()
        result = vtx.unpack(file, max_chunk_count)
        if result:
            print('Vertex Chunk Unpack Faild!!! File Position: {0:#X}'.format(file.tell()))
            return True
        self.vertexs(vtx)
        return False

class Model:
    def __init__(self):
        self.polygons = []
    
    def unpack(self, file: typing.IO, skip: int, max_polygon_count: int, max_chunk_count) -> None:
        # Go to EOF
        file.seek(0x0, io.SEEK_END)
        file_max = file.tell()
        # Go to 1st Polygon
        file.seek(skip, io.SEEK_SET)
        
        #while (True):
        for i in range(max_polygon_count):
            if ( file.tell() >= file_max ):
                break
            polygon = Polygon()
            result = polygon.unpack(file, max_chunk_count)
            if result:
                break
            self.polygons.append(polygon)
            print('File Position: {0:#X}'.format(file.tell()))
        




# COURSE
offset = 0x1C20
#for safe
max_polygon_count = 1
max_chunk_count = 10
filename = r"format\track\night_section_a_001\00000000\00000000.bin" # Night Section A
filename = r"format\track\SonyGT2\00000152\00000000.bin" # SonyGT2


# Path
path = "D:\Hack\SEGA\segaGT\\" + filename

# open files
file = open(path, 'rb')

model = Model()
model.unpack(file, offset, max_polygon_count, max_chunk_count)

for i, polygon in enumerate(model.polygons):
    break
    mesh_name = 'polygon_{0:04}'.format(i)
    print("---- Generate {0} ---".format(mesh_name))
    bl_mesh = bpy.data.meshes.new(mesh_name)
    bl_obj = bpy.data.objects.new(mesh_name, bl_mesh)

    scene = bpy.context.scene
    bpy.context.collection.objects.link(bl_obj)
    bpy.context.view_layer.objects.active = bl_obj
    bl_obj.select_set(True)
    bl_mesh = bpy.context.object.data
    bm = bmesh.new()
    
    normals = []
    uvs = []
    #vertex
    vtxs = []
    for vtx in polygon.vertexs:
        v = bm.verts.new(vtx.position)
        vtxs.append(v)
        #normals.append(vtx.normal)
        #uvs.append(vtx.uv)

    idx_lists = []
    for j, mesh in enumerate(polygon.meshs):
        
        idx = mesh.idx
        print("vtx0:0x{0:02X}, vtx1:0x{1:02X}, vtx2:0x{2:02X}, vtx3:0x{3:02X}".format(\
                idx[0], idx[1], idx[2], idx[3]))
        
        # already generated face
        if (idx in idx_lists):
            continue
        
        idx_lists.append(idx) # store current list of idx
        _idx = list(dict.fromkeys(idx))
        idx_count = len(_idx)
        try:
            # no face
            if (idx_count < 3):
                continue #skip

            # triangle
            elif(idx_count == 3):
                v0 = vtxs[_idx[0]] if j % 2 == 0 else vtxs[_idx[0]]
                v1 = vtxs[_idx[1]]
                v2 = vtxs[_idx[2]] if j % 2 == 0 else vtxs[_idx[1]]
                bm.faces.new((v0, v1, v2))
                uv = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
                uvs.append(uv)

            # quad                
            if(idx_count == 4):
                v0 = vtxs[idx[1]] if j % 2 == 0 else vtxs[idx[1]]
                v1 = vtxs[idx[2]] if j % 2 == 0 else vtxs[idx[2]]
                v2 = vtxs[idx[3]] if j % 2 == 0 else vtxs[idx[3]]
                bm.faces.new((v0, v1, v2))
                v0 = vtxs[idx[1]] if j % 2 == 0 else vtxs[idx[1]]
                v1 = vtxs[idx[3]] if j % 2 == 0 else vtxs[idx[3]]
                v2 = vtxs[idx[0]] if j % 2 == 0 else vtxs[idx[0]]
                bm.faces.new((v0, v1, v2))
                uv = [[0.0, 1.0], [0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
                uvs.append(uv)
        except:
            print("Vertex Exception vtx0:0x{0:02X}, vtx1:0x{1:02X}, vtx2:0x{2:02X}, vtx3:0x{3:02X}".format(\
                    idx[0], idx[1], idx[2], idx[3]))
            bm.to_mesh(bl_mesh)

    bm.to_mesh(bl_mesh)
    bm.free()
    
    #break   
    continue
    
    # apply normal
    #clnors = array.array('f', [0.0] * (len(bl_mesh.loops) * 3))
    #bl_mesh.loops.foreach_get("normal", clnors)
    #bl_mesh.polygons.foreach_set("use_smooth", [True] * len(bl_mesh.polygons))
    
    #bl_mesh.use_auto_smooth = True
    #bl_mesh.normals_split_custom_set_from_vertices(normals)

    #uv
    channel_name = 'uv0'
    bl_mesh.uv_textures.new(channel_name) # 2.7
    for i, loop in enumerate(bl_mesh.loops):
        bl_mesh.uv_layers[channel_name].data[i].uv = uvs[loop.vertex_index]
