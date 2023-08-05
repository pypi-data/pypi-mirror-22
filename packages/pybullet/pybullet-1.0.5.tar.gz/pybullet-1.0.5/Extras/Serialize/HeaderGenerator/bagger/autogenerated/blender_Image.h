/* Copyright (C) 2006 Charlie C
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
*
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
*
* 1. The origin of this software must not be misrepresented; you must not
*    claim that you wrote the original software. If you use this software
*    in a product, an acknowledgment in the product documentation would be
*    appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
*    misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/
// Auto generated from makesdna dna.c
#ifndef __BLENDER_IMAGE__H__
#define __BLENDER_IMAGE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ColorManagedColorspaceSettings.h"
#include "blender_ID.h"
#include "blender_ListBase.h"
#include "blender_RenderSlot.h"

namespace Blender {


    // ---------------------------------------------- //
    class Image
    {
    public:
        ID id;
        char name[1024];
        bInvalidHandle *cache;
        bInvalidHandle *gputexture;
        ListBase anims;
        bInvalidHandle *rr;
        bInvalidHandle *renders[8];
        short render_slot;
        short last_render_slot;
        int flag;
        short source;
        short type;
        int lastframe;
        short tpageflag;
        short totbind;
        short xrep;
        short yrep;
        short twsta;
        short twend;
        int bindcode;
        int *repbind;
        PackedFile *packedfile;
        ListBase packedfiles;
        PreviewImage *preview;
        float lastupdate;
        int lastused;
        short animspeed;
        short ok;
        int gen_x;
        int gen_y;
        char gen_type;
        char gen_flag;
        short gen_depth;
        vec4f gen_color;
        float aspx;
        float aspy;
        ColorManagedColorspaceSettings colorspace_settings;
        char alpha_mode;
        char pad[5];
        char eye;
        char views_format;
        ListBase views;
        Stereo3dFormat *stereo3d_format;
        RenderSlot render_slots[8];
    };
}


#endif//__BLENDER_IMAGE__H__
