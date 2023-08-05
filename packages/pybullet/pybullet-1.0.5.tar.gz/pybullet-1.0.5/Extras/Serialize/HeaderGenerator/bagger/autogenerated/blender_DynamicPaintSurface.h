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
#ifndef __BLENDER_DYNAMICPAINTSURFACE__H__
#define __BLENDER_DYNAMICPAINTSURFACE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class DynamicPaintSurface
    {
    public:
        DynamicPaintSurface *next;
        DynamicPaintSurface *prev;
        DynamicPaintCanvasSettings *canvas;
        bInvalidHandle *data;
        Group *brush_group;
        EffectorWeights *effector_weights;
        PointCache *pointcache;
        ListBase ptcaches;
        int current_frame;
        char name[64];
        short format;
        short type;
        short disp_type;
        short image_fileformat;
        short effect_ui;
        short preview_id;
        short init_color_type;
        short pad_s;
        int flags;
        int effect;
        int image_resolution;
        int substeps;
        int start_frame;
        int end_frame;
        int pad;
        vec4f init_color;
        Tex *init_texture;
        char init_layername[64];
        int dry_speed;
        int diss_speed;
        float color_dry_threshold;
        float depth_clamp;
        float disp_factor;
        float spread_speed;
        float color_spread_speed;
        float shrink_speed;
        float drip_vel;
        float drip_acc;
        float influence_scale;
        float radius_scale;
        float wave_damping;
        float wave_speed;
        float wave_timescale;
        float wave_spring;
        float wave_smoothness;
        int pad2;
        char uvlayer_name[64];
        char image_output_path[1024];
        char output_name[64];
        char output_name2[64];
    };
}


#endif//__BLENDER_DYNAMICPAINTSURFACE__H__
