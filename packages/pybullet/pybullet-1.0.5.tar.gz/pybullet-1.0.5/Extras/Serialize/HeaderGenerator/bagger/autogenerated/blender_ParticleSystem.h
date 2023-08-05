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
#ifndef __BLENDER_PARTICLESYSTEM__H__
#define __BLENDER_PARTICLESYSTEM__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class ParticleSystem
    {
    public:
        ParticleSystem *next;
        ParticleSystem *prev;
        ParticleSettings *part;
        ParticleData *particles;
        ChildParticle *child;
        bInvalidHandle *edit;
        void (*free_edit)();
        bInvalidHandle **pathcache;
        bInvalidHandle **childcache;
        ListBase pathcachebufs;
        ListBase childcachebufs;
        ClothModifierData *clmd;
        bInvalidHandle *hair_in_dm;
        bInvalidHandle *hair_out_dm;
        Object *target_ob;
        bInvalidHandle *lattice_deform_data;
        Object *parent;
        ListBase targets;
        char name[64];
        float imat[4][4];
        float cfra;
        float tree_frame;
        float bvhtree_frame;
        int seed;
        int child_seed;
        int flag;
        int totpart;
        int totunexist;
        int totchild;
        int totcached;
        int totchildcache;
        short recalc;
        short target_psys;
        short totkeyed;
        short bakespace;
        char bb_uvname[3][64];
        short vgroup[12];
        short vg_neg;
        short rt3;
        bInvalidHandle *renderdata;
        PointCache *pointcache;
        ListBase ptcaches;
        ListBase *effectors;
        ParticleSpring *fluid_springs;
        int tot_fluidsprings;
        int alloc_fluidsprings;
        bInvalidHandle *tree;
        bInvalidHandle *bvhtree;
        bInvalidHandle *pdd;
        float dt_frac;
        float _pad;
    };
}


#endif//__BLENDER_PARTICLESYSTEM__H__
