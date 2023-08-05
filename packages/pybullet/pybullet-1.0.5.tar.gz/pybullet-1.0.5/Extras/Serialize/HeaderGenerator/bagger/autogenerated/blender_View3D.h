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
#ifndef __BLENDER_VIEW3D__H__
#define __BLENDER_VIEW3D__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_GPUFXSettings.h"
#include "blender_ListBase.h"
#include "blender_rctf.h"

namespace Blender {


    // ---------------------------------------------- //
    class View3D
    {
    public:
        SpaceLink *next;
        SpaceLink *prev;
        ListBase regionbase;
        int spacetype;
        float blockscale;
        short blockhandler[8];
        vec4f viewquat;
        float dist;
        float bundle_size;
        char bundle_drawtype;
        char pad[3];
        int lay_prev;
        int lay_used;
        short persp;
        short view;
        Object *camera;
        Object *ob_centre;
        rctf render_border;
        ListBase bgpicbase;
        BGpic *bgpic;
        View3D *localvd;
        char ob_centre_bone[64];
        int lay;
        int layact;
        short drawtype;
        short ob_centre_cursor;
        short scenelock;
        short around;
        short flag;
        short flag2;
        float lens;
        float grid;
        float near;
        float far;
        vec3f ofs;
        vec3f cursor;
        short matcap_icon;
        short gridlines;
        short gridsubdiv;
        char gridflag;
        char twtype;
        char twmode;
        char twflag;
        short flag3;
        ListBase afterdraw_transp;
        ListBase afterdraw_xray;
        ListBase afterdraw_xraytransp;
        char zbuf;
        char transp;
        char xray;
        char multiview_eye;
        char pad3[4];
        GPUFXSettings fx_settings;
        void *properties_storage;
        Material *defmaterial;
        bGPdata *gpd;
        short stereo3d_flag;
        char stereo3d_camera;
        char pad4;
        float stereo3d_convergence_factor;
        float stereo3d_volume_alpha;
        float stereo3d_convergence_alpha;
    };
}


#endif//__BLENDER_VIEW3D__H__
