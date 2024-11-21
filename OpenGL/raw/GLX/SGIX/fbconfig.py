'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_SGIX_fbconfig'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_SGIX_fbconfig',error_checker=_errors._error_checker)
GLX_COLOR_INDEX_BIT_SGIX=_C('GLX_COLOR_INDEX_BIT_SGIX',0x00000002)
GLX_COLOR_INDEX_TYPE_SGIX=_C('GLX_COLOR_INDEX_TYPE_SGIX',0x8015)
GLX_DRAWABLE_TYPE_SGIX=_C('GLX_DRAWABLE_TYPE_SGIX',0x8010)
GLX_FBCONFIG_ID_SGIX=_C('GLX_FBCONFIG_ID_SGIX',0x8013)
GLX_PIXMAP_BIT_SGIX=_C('GLX_PIXMAP_BIT_SGIX',0x00000002)
GLX_RENDER_TYPE_SGIX=_C('GLX_RENDER_TYPE_SGIX',0x8011)
GLX_RGBA_BIT_SGIX=_C('GLX_RGBA_BIT_SGIX',0x00000001)
GLX_RGBA_TYPE_SGIX=_C('GLX_RGBA_TYPE_SGIX',0x8014)
GLX_SCREEN_EXT=_C('GLX_SCREEN_EXT',0x800C)
GLX_WINDOW_BIT_SGIX=_C('GLX_WINDOW_BIT_SGIX',0x00000001)
GLX_X_RENDERABLE_SGIX=_C('GLX_X_RENDERABLE_SGIX',0x8012)
@_f
@_p.types(ctypes.POINTER(_cs.GLXFBConfigSGIX),ctypes.POINTER(_cs.Display),_cs.c_int,ctypes.POINTER(_cs.c_int),ctypes.POINTER(_cs.c_int))
def glXChooseFBConfigSGIX(dpy,screen,attrib_list,nelements):pass
@_f
@_p.types(_cs.GLXContext,ctypes.POINTER(_cs.Display),_cs.GLXFBConfigSGIX,_cs.c_int,_cs.GLXContext,_cs.Bool)
def glXCreateContextWithConfigSGIX(dpy,config,render_type,share_list,direct):pass
@_f
@_p.types(_cs.GLXPixmap,ctypes.POINTER(_cs.Display),_cs.GLXFBConfigSGIX,_cs.Pixmap)
def glXCreateGLXPixmapWithConfigSGIX(dpy,config,pixmap):pass
@_f
@_p.types(_cs.c_int,ctypes.POINTER(_cs.Display),_cs.GLXFBConfigSGIX,_cs.c_int,ctypes.POINTER(_cs.c_int))
def glXGetFBConfigAttribSGIX(dpy,config,attribute,value):pass
@_f
@_p.types(_cs.GLXFBConfigSGIX,ctypes.POINTER(_cs.Display),ctypes.POINTER(_cs.XVisualInfo))
def glXGetFBConfigFromVisualSGIX(dpy,vis):pass
@_f
@_p.types(ctypes.POINTER(_cs.XVisualInfo),ctypes.POINTER(_cs.Display),_cs.GLXFBConfigSGIX)
def glXGetVisualFromFBConfigSGIX(dpy,config):pass