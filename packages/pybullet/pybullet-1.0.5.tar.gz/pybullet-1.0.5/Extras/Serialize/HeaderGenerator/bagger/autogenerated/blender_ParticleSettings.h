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
#ifndef __BLENDER_PARTICLESETTINGS__H__
#define __BLENDER_PARTICLESETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ID.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class ParticleSettings
    {
    public:
        ID id;
        AnimData *adt;
        BoidSettings *boids;
        SPHFluidSettings *fluid;
        EffectorWeights *effector_weights;
        int flag;
        int rt;
        short type;
        short from;
        short distr;
        short texact;
        short phystype;
        short rotmode;
        short avemode;
        short reactevent;
        int draw;
        int pad1;
        short draw_as;
        short draw_size;
        short childtype;
        short pad2;
        short ren_as;
        short subframes;
        short draw_col;
        short draw_step;
        short ren_step;
        short hair_step;
        short keys_step;
        short adapt_angle;
        short adapt_pix;
        short disp;
        short omat;
        short interpolation;
        short integrator;
        short rotfrom;
        short kink;
        short kink_axis;
        short bb_align;
        short bb_uv_split;
        short bb_anim;
        short bb_split_offset;
        float bb_tilt;
        float bb_rand_tilt;
        float bb_offset[2];
        float bb_size[2];
        float bb_vel_head;
        float bb_vel_tail;
        float color_vec_max;
        short simplify_flag;
        short simplify_refsize;
        float simplify_rate;
        float simplify_transition;
        float simplify_viewport;
        float sta;
        float end;
        float lifetime;
        float randlife;
        float timetweak;
        float courant_target;
        float jitfac;
        float eff_hair;
        float grid_rand;
        float ps_offset[1];
        int totpart;
        int userjit;
        int grid_res;
        int effector_amount;
        short time_flag;
        short time_pad[3];
        float normfac;
        float obfac;
        float randfac;
        float partfac;
        float tanfac;
        float tanphase;
        float reactfac;
        vec3f ob_vel;
        float avefac;
        float phasefac;
        float randrotfac;
        float randphasefac;
        float mass;
        float size;
        float randsize;
        vec3f acc;
        float dragfac;
        float brownfac;
        float dampfac;
        float randlength;
        int child_flag;
        int pad3;
        int child_nbr;
        int ren_child_nbr;
        float parents;
        float childsize;
        float childrandsize;
        float childrad;
        float childflat;
        float clumpfac;
        float clumppow;
        float kink_amp;
        float kink_freq;
        float kink_shape;
        float kink_flat;
        float kink_amp_clump;
        int kink_extra_steps;
        int pad4;
        float kink_axis_random;
        float kink_amp_random;
        float rough1;
        float rough1_size;
        float rough2;
        float rough2_size;
        float rough2_thres;
        float rough_end;
        float rough_end_shape;
        float clength;
        float clength_thres;
        float parting_fac;
        float parting_min;
        float parting_max;
        float branch_thres;
        float draw_line[2];
        float path_start;
        float path_end;
        int trail_count;
        int keyed_loops;
        CurveMapping *clumpcurve;
        CurveMapping *roughcurve;
        float clump_noise_size;
        float bending_random;
        MTex *mtex[18];
        Group *dup_group;
        ListBase dupliweights;
        Group *eff_group;
        Object *dup_ob;
        Object *bb_ob;
        Ipo *ipo;
        PartDeflect *pd;
        PartDeflect *pd2;
        short use_modifier_stack;
        short pad5[3];
    };
}


#endif//__BLENDER_PARTICLESETTINGS__H__
