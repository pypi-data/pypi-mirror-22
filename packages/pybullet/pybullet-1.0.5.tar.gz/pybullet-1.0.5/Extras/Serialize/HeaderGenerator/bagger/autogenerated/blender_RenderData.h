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
#ifndef __BLENDER_RENDERDATA__H__
#define __BLENDER_RENDERDATA__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_BakeData.h"
#include "blender_FFMpegCodecData.h"
#include "blender_ImageFormatData.h"
#include "blender_ListBase.h"
#include "blender_QuicktimeCodecSettings.h"
#include "blender_rctf.h"
#include "blender_rcti.h"

namespace Blender {


    // ---------------------------------------------- //
    class RenderData
    {
    public:
        ImageFormatData im_format;
        AviCodecData *avicodecdata;
        QuicktimeCodecData *qtcodecdata;
        QuicktimeCodecSettings qtcodecsettings;
        FFMpegCodecData ffcodecdata;
        int cfra;
        int sfra;
        int efra;
        float subframe;
        int psfra;
        int pefra;
        int images;
        int framapto;
        short flag;
        short threads;
        float framelen;
        float blurfac;
        float edgeR;
        float edgeG;
        float edgeB;
        short fullscreen;
        short xplay;
        short yplay;
        short freqplay;
        short depth;
        short attrib;
        int frame_step;
        short stereomode;
        short dimensionspreset;
        short filtertype;
        short size;
        short maximsize;
        short pad6;
        int xsch;
        int ysch;
        short xparts;
        short yparts;
        int tilex;
        int tiley;
        short planes;
        short imtype;
        short subimtype;
        short quality;
        short displaymode;
        char use_lock_interface;
        char pad7;
        int scemode;
        int mode;
        int raytrace_options;
        short raytrace_structure;
        short pad1;
        short ocres;
        short pad4;
        short alphamode;
        short osa;
        short frs_sec;
        short edgeint;
        rctf safety;
        rctf border;
        rcti disprect;
        ListBase layers;
        short actlay;
        short mblur_samples;
        float xasp;
        float yasp;
        float frs_sec_base;
        float gauss;
        int color_mgt_flag;
        float postgamma;
        float posthue;
        float postsat;
        float dither_intensity;
        short bake_osa;
        short bake_filter;
        short bake_mode;
        short bake_flag;
        short bake_normal_space;
        short bake_quad_split;
        float bake_maxdist;
        float bake_biasdist;
        short bake_samples;
        short bake_pad;
        float bake_user_scale;
        float bake_pad1;
        char pic[1024];
        int stamp;
        short stamp_font_id;
        short pad3;
        char stamp_udata[768];
        vec4f fg_stamp;
        vec4f bg_stamp;
        char seq_prev_type;
        char seq_rend_type;
        char seq_flag;
        char pad5[5];
        int simplify_flag;
        short simplify_subsurf;
        short simplify_subsurf_render;
        short simplify_shadowsamples;
        short pad9;
        float simplify_particles;
        float simplify_particles_render;
        float simplify_aosss;
        short cineonwhite;
        short cineonblack;
        float cineongamma;
        short jp2_preset;
        short jp2_depth;
        int rpad3;
        short domeres;
        short domemode;
        short domeangle;
        short dometilt;
        float domeresbuf;
        float pad2;
        Text *dometext;
        int line_thickness_mode;
        float unit_line_thickness;
        char engine[32];
        BakeData bake;
        int preview_start_resolution;
        int pad;
        ListBase views;
        short actview;
        short views_format;
        short pad8[2];
    };
}


#endif//__BLENDER_RENDERDATA__H__
