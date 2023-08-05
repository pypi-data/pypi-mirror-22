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
#ifndef __BLENDER_SMOKEDOMAINSETTINGS__H__
#define __BLENDER_SMOKEDOMAINSETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class SmokeDomainSettings
    {
    public:
        SmokeModifierData *smd;
        bInvalidHandle *fluid;
        void *fluid_mutex;
        Group *fluid_group;
        Group *eff_group;
        Group *coll_group;
        bInvalidHandle *wt;
        bInvalidHandle *tex;
        bInvalidHandle *tex_wt;
        bInvalidHandle *tex_shadow;
        bInvalidHandle *tex_flame;
        float *shadow;
        vec3f p0;
        vec3f p1;
        vec3f dp0;
        vec3f cell_size;
        vec3f global_size;
        vec3f prev_loc;
        int shift[3];
        vec3f shift_f;
        vec3f obj_shift_f;
        float imat[4][4];
        float obmat[4][4];
        int base_res[3];
        int res_min[3];
        int res_max[3];
        int res[3];
        int total_cells;
        float dx;
        float scale;
        int adapt_margin;
        int adapt_res;
        float adapt_threshold;
        float alpha;
        float beta;
        int amplify;
        int maxres;
        int flags;
        int viewsettings;
        short noise;
        short diss_percent;
        int diss_speed;
        float strength;
        int res_wt[3];
        float dx_wt;
        int cache_comp;
        int cache_high_comp;
        PointCache *point_cache[2];
        ListBase ptcaches[2];
        EffectorWeights *effector_weights;
        int border_collisions;
        float time_scale;
        float vorticity;
        int active_fields;
        vec3f active_color;
        int highres_sampling;
        float burning_rate;
        float flame_smoke;
        float flame_vorticity;
        float flame_ignition;
        float flame_max_temp;
        vec3f flame_smoke_color;
    };
}


#endif//__BLENDER_SMOKEDOMAINSETTINGS__H__
