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
#ifndef __BLENDER_REGIONVIEW3D__H__
#define __BLENDER_REGIONVIEW3D__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class RegionView3D
    {
    public:
        float winmat[4][4];
        float viewmat[4][4];
        float viewinv[4][4];
        float persmat[4][4];
        float persinv[4][4];
        vec4f viewcamtexcofac;
        float viewmatob[4][4];
        float persmatob[4][4];
        float clip[6][4];
        float clip_local[6][4];
        BoundBox *clipbb;
        RegionView3D *localvd;
        bInvalidHandle *render_engine;
        bInvalidHandle *depths;
        void *gpuoffscreen;
        bInvalidHandle *sms;
        bInvalidHandle *smooth_timer;
        float twmat[4][4];
        vec4f viewquat;
        float dist;
        float camdx;
        float camdy;
        float pixsize;
        vec3f ofs;
        float camzoom;
        char is_persp;
        char persp;
        char view;
        char viewlock;
        char viewlock_quad;
        char pad[3];
        float ofs_lock[2];
        short twdrawflag;
        short rflag;
        vec4f lviewquat;
        short lpersp;
        short lview;
        float gridview;
        vec3f tw_idot;
        float rot_angle;
        vec3f rot_axis;
        bInvalidHandle *compositor;
    };
}


#endif//__BLENDER_REGIONVIEW3D__H__
